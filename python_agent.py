# python_agent.py
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import ast
import subprocess
import sys
import re
import os
import PyPDF2
from typing import Optional, List, Dict, Set
import logging
from itertools import chain
import base64
import hashlib
from pathlib import Path
import fitz  # PyMuPDF
import numpy as np

CODE_FENCE_BLOCK = re.compile(r'```(?:python)?\s*([\s\S]+?)\s*```', re.IGNORECASE)
BUILTIN_SYMBOLS = set(dir(__builtins__)) | {"self", "cls"}

def _extract_code_snippet(code: str) -> str:
    """Normalize incoming code by stripping Markdown fences and whitespace."""
    if not code:
        return ""

    stripped = code.strip()
    fence_match = CODE_FENCE_BLOCK.search(stripped)
    if fence_match:
        return fence_match.group(1).strip()

    return stripped

def _safe_unparse(node: Optional[ast.AST]) -> str:
    """Safely convert AST nodes back to source-like text."""
    if node is None:
        return ""
    try:
        return ast.unparse(node)  # type: ignore[attr-defined]
    except Exception:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{_safe_unparse(node.value)}.{node.attr}"
        if isinstance(node, ast.Constant):
            return repr(node.value)
        return node.__class__.__name__

def _format_error_context(lines: List[str], lineno: Optional[int], col: Optional[int]) -> str:
    """Generate a short excerpt around a syntax error with a caret pointer."""
    if not lineno or lineno < 1 or lineno > len(lines):
        return ""

    start = max(0, lineno - 2)
    end = min(len(lines), lineno + 1)
    excerpt = []
    for idx in range(start, end):
        marker = ">" if (idx + 1) == lineno else " "
        prefix = f"{marker} 第{idx + 1}行: "
        line_content = lines[idx].replace('\t', '    ')
        excerpt.append(f"{prefix}{line_content}")
        if (idx + 1) == lineno and col and col > 0:
            caret_padding = " " * (len(prefix) + col - 1)
            excerpt.append(f"{caret_padding}^")

    return "\n".join(excerpt)

def _collect_code_structure(tree: ast.AST) -> Dict:
    """Gather high-level information such as imports, classes, and functions."""
    structure = {
        "imports": [],
        "functions": [],
        "classes": [],
        "async_functions": [],
        "type_hint_total": 0,
        "type_hint_annotated": 0
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                alias_repr = alias.name if not alias.asname else f"{alias.name} as {alias.asname}"
                structure["imports"].append(alias_repr)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                alias_repr = alias.name if not alias.asname else f"{alias.name} as {alias.asname}"
                structure["imports"].append(f"from {module} import {alias_repr}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = []

            def _register_arg(arg_node: ast.arg, prefix: str = ""):
                structure["type_hint_total"] += 1
                annotated = bool(arg_node.annotation)
                if annotated:
                    structure["type_hint_annotated"] += 1
                annotation = f": {_safe_unparse(arg_node.annotation)}" if annotated else ""
                args.append(f"{prefix}{arg_node.arg}{annotation}")

            for arg in chain(node.args.posonlyargs, node.args.args):
                _register_arg(arg)

            if node.args.vararg:
                _register_arg(node.args.vararg, prefix="*")

            if node.args.kwonlyargs:
                if not node.args.vararg:
                    args.append("*")
                for arg in node.args.kwonlyargs:
                    _register_arg(arg)

            if node.args.kwarg:
                _register_arg(node.args.kwarg, prefix="**")

            returns = _safe_unparse(getattr(node, 'returns', None))
            fn_info = {
                "name": node.name,
                "args": args,
                "returns": returns,
                "lineno": node.lineno,
                "end_lineno": getattr(node, 'end_lineno', node.lineno),
                "is_async": isinstance(node, ast.AsyncFunctionDef)
            }
            if isinstance(node, ast.AsyncFunctionDef):
                structure["async_functions"].append(fn_info)
            else:
                structure["functions"].append(fn_info)
        elif isinstance(node, ast.ClassDef):
            bases = [_safe_unparse(base) for base in node.bases] or ["object"]
            methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            structure["classes"].append({
                "name": node.name,
                "bases": bases,
                "methods": methods,
                "lineno": node.lineno,
                "end_lineno": getattr(node, 'end_lineno', node.lineno)
            })

    return structure

def _docstring_gaps(tree: ast.AST) -> List[str]:
    """Identify missing docstrings at module/class/function level."""
    issues = []
    if ast.get_docstring(tree) is None:
        issues.append("模块缺少顶层 docstring")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node) is None:
                issues.append(f"函数 `{node.name}` 缺少 docstring")
        elif isinstance(node, ast.ClassDef):
            if ast.get_docstring(node) is None:
                issues.append(f"类 `{node.name}` 缺少 docstring")

    return issues

def _basic_style_checks(lines: List[str]) -> List[str]:
    """Perform lightweight style linting."""
    issues = []
    for idx, line in enumerate(lines, 1):
        raw_line = line.rstrip("\n")
        if len(raw_line) > 100:
            issues.append(f"第{idx}行长度为{len(raw_line)}字符，建议不超过100字符")
        if raw_line.rstrip() != raw_line:
            issues.append(f"第{idx}行存在尾随空格")
        if raw_line.startswith('\t'):
            issues.append(f"第{idx}行使用了制表符缩进，建议使用4个空格")
        leading = len(raw_line) - len(raw_line.lstrip(' '))
        if raw_line and (raw_line[0] == ' ' or raw_line[0] == '\t'):
            if raw_line.startswith(' ') and (leading % 4) != 0:
                issues.append(f"第{idx}行缩进不是4的倍数")

    return issues

def _cyclomatic_complexity(node: ast.AST) -> int:
    """Compute a rough cyclomatic complexity for a function node."""
    complexity = 1
    decision_points = (
        ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith,
        ast.BoolOp, ast.IfExp, ast.Compare, ast.comprehension, ast.ExceptHandler
    )
    for child in ast.walk(node):
        if isinstance(child, decision_points):
            complexity += 1
    return complexity

def _max_nesting_depth(node: ast.AST, depth: int = 0) -> int:
    """Approximate nesting depth for control-flow statements."""
    control_nodes = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        child_depth = depth + 1 if isinstance(child, control_nodes) else depth
        max_depth = max(max_depth, _max_nesting_depth(child, child_depth))
    return max_depth

def _extract_target_names(target: ast.AST) -> Set[str]:
    """Collect variable names introduced by assignment targets."""
    names: Set[str] = set()
    if isinstance(target, ast.Name):
        names.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            names.update(_extract_target_names(elt))
    elif isinstance(target, ast.Starred):
        names.update(_extract_target_names(target.value))
    return names

def _collect_defined_names(tree: ast.AST) -> Set[str]:
    """Collect names that are defined within the AST (assignments, defs, imports, etc.)."""
    defined: Set[str] = set(BUILTIN_SYMBOLS)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defined.add(node.name)

            def _register_args(args: ast.arguments):
                for arg in chain(args.posonlyargs, args.args, args.kwonlyargs):
                    defined.add(arg.arg)
                if args.vararg:
                    defined.add(args.vararg.arg)
                if args.kwarg:
                    defined.add(args.kwarg.arg)

            _register_args(node.args)
        elif isinstance(node, ast.Lambda):
            for arg in node.args.args + node.args.kwonlyargs:
                defined.add(arg.arg)
            if node.args.vararg:
                defined.add(node.args.vararg.arg)
            if node.args.kwarg:
                defined.add(node.args.kwarg.arg)
        elif isinstance(node, ast.ClassDef):
            defined.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                defined.update(_extract_target_names(target))
        elif isinstance(node, ast.AnnAssign):
            defined.update(_extract_target_names(node.target))
        elif isinstance(node, ast.AugAssign):
            defined.update(_extract_target_names(node.target))
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            defined.update(_extract_target_names(node.target))
        elif isinstance(node, ast.comprehension):
            defined.update(_extract_target_names(node.target))
        elif isinstance(node, ast.With):
            for item in node.items:
                if item.optional_vars:
                    defined.update(_extract_target_names(item.optional_vars))
        elif isinstance(node, ast.AsyncWith):
            for item in node.items:
                if item.optional_vars:
                    defined.update(_extract_target_names(item.optional_vars))
        elif isinstance(node, ast.NamedExpr):
            defined.update(_extract_target_names(node.target))
        elif isinstance(node, ast.ExceptHandler):
            if isinstance(node.name, str):
                defined.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                defined.add(alias.asname or alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == '*':
                    continue
                defined.add(alias.asname or alias.name)

    return defined

def _detect_name_issues(tree: ast.AST) -> Dict[str, List[int]]:
    """Find names that are referenced but never defined/imported."""
    defined = _collect_defined_names(tree)
    issues: Dict[str, set] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in defined:
                issues.setdefault(node.id, set()).add(getattr(node, "lineno", 0) or 0)

    return {name: sorted(lines) for name, lines in issues.items() if lines}

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class EnhancedPDFHandbook:
    """增强版PDF处理器，支持精确内容提取、图片识别和检索"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = None
        self.content_index = {}  # 关键词到位置的索引
        self.image_index = {}    # 图片到内容的映射
        self.sections = {}       # 章节结构
        self.text_cache = {}     # 页面文本缓存
        self.images_cache = {}   # 图片缓存
        self.load_pdf()
        
    def load_pdf(self):
        """加载并索引PDF内容"""
        try:
            if not os.path.exists(self.pdf_path):
                logger.warning(f"PDF文件不存在: {self.pdf_path}")
                return
            
            self.doc = fitz.open(self.pdf_path)
            self._extract_content()
            self._build_index()
            self._extract_and_save_images()
            logger.info(f"PDF加载成功: {len(self.doc)}页, 图片{len(self.images_cache)}张")
            
        except Exception as e:
            logger.error(f"加载PDF失败: {e}")
    
    def _extract_content(self):
        """提取PDF文本内容并建立结构"""
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text("text")
            self.text_cache[page_num] = text
            
            # 提取章节标题
            if page_num == 0:
                self._parse_sections_from_text(text)
    
    def _parse_sections_from_text(self, text: str):
        """从文本中解析章节结构"""
        lines = text.split('\n')
        current_section = "简介"
        section_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 改进的章节检测
            if self._is_section_title(line):
                if section_lines:
                    self.sections[current_section] = '\n'.join(section_lines)
                current_section = line
                section_lines = []
            else:
                section_lines.append(line)
        
        if section_lines:
            self.sections[current_section] = '\n'.join(section_lines)
    
    def _is_section_title(self, text: str) -> bool:
        """判断是否为章节标题"""
        patterns = [
            r'^第[一二三四五六七八九十\d]+[章节条]',
            r'^[一二三四五六七八九十]+、',
            r'^\d+\.\d+',
            r'^[A-Z][A-Z\s]+$',
            r'^#+ ',
            r'^[【\[](.*?)[】\]]$'
        ]
        
        for pattern in patterns:
            if re.match(pattern, text):
                return True
        
        # 长度和内容判断
        if len(text) < 50 and any(keyword in text.lower() for keyword in 
                                 ['概述', '简介', '基础', '进阶', '高级', '总结', '附录']):
            return True
        
        return False
    
    def _build_section_index(self):
        """建立章节索引"""
        for section, content in self.sections.items():
            # 提取关键词
            keywords = self._extract_keywords(content)
            for keyword in keywords:
                if keyword not in self.content_index:
                    self.content_index[keyword] = []
                self.content_index[keyword].append({
                    'section': section,
                    'content': content[:500],  # 截取前500字符
                    'relevance': 'high'
                })
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> list:
        """从文本中提取关键词"""
        # 移除停用词
        stop_words = {'的', '了', '和', '是', '在', '有', '就', '都', '而', '及', '与', '或', '等'}
        
        # 提取名词性短语
        words = re.findall(r'[\u4e00-\u9fff]{2,5}', text) + re.findall(r'\b[a-zA-Z]{3,}\b', text)
        
        # 统计词频
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 按频率排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def _build_index(self):
        """构建全文索引"""
        python_keywords = {
            '语法', '函数', '类', '对象', '模块', '包', '异常', '装饰器',
            '生成器', '迭代器', '列表', '字典', '集合', '元组', '字符串',
            '文件', '输入输出', '多线程', '异步', '网络', '数据库',
            '测试', '调试', '性能', '优化', '算法', '数据结构'
        }
        
        for page_num, text in self.text_cache.items():
            # 为每个关键词建立索引
            for keyword in python_keywords:
                if keyword in text:
                    if keyword not in self.content_index:
                        self.content_index[keyword] = []
                    
                    # 提取上下文
                    context = self._get_context(text, keyword, 200)
                    self.content_index[keyword].append({
                        'page': page_num + 1,
                        'context': context,
                        'type': 'keyword_match'
                    })
    
    def _get_context(self, text: str, keyword: str, context_size: int = 200) -> str:
        """获取关键词上下文"""
        pos = text.find(keyword)
        if pos == -1:
            return ""
        
        start = max(0, pos - context_size // 2)
        end = min(len(text), pos + len(keyword) + context_size // 2)
        return text[start:end]
    
    def _extract_and_save_images(self):
        """提取PDF中的图片并缓存"""
        try:
            images_dir = Path("static/images/handbook")
            images_dir.mkdir(parents=True, exist_ok=True)
            
            image_count = 0
            for page_num in range(len(self.doc)):
                page = self.doc[page_num]
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = self.doc.extract_image(xref)
                    
                    if base_image:
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        # 生成唯一文件名
                        image_hash = hashlib.md5(image_bytes).hexdigest()[:8]
                        image_filename = f"page_{page_num+1}_img_{img_index}_{image_hash}.{image_ext}"
                        image_path = images_dir / image_filename
                        
                        # 保存图片
                        with open(image_path, "wb") as f:
                            f.write(image_bytes)
                        
                        # 缓存图片信息
                        image_key = f"page_{page_num+1}_img_{img_index}"
                        self.images_cache[image_key] = {
                            'path': str(image_path),
                            'page': page_num + 1,
                            'index': img_index,
                            'base64': self._image_to_base64(image_bytes, image_ext),
                            'caption': self._generate_image_caption(page_num, img_index)
                        }
                        
                        # 关联图片和附近文本
                        self._link_image_to_text(page_num, img_index)
                        
                        image_count += 1
            
            logger.info(f"提取了 {image_count} 张图片")
            
        except Exception as e:
            logger.error(f"提取图片失败: {e}")
    
    def _image_to_base64(self, image_bytes: bytes, image_ext: str) -> str:
        """将图片转换为base64"""
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def _generate_image_caption(self, page_num: int, img_index: int) -> str:
        """生成图片标题"""
        page_text = self.text_cache.get(page_num, "")
        
        # 在图片附近找相关文本作为标题
        lines = page_text.split('\n')
        if lines and len(lines) > 0:
            # 简单返回页面第一行作为标题
            return lines[0][:50] + "..."
        
        return f"第{page_num+1}页 图片{img_index+1}"
    
    def _link_image_to_text(self, page_num: int, img_index: int):
        """将图片与附近文本关联"""
        page_text = self.text_cache.get(page_num, "")
        if page_text:
            # 提取页面中的关键词
            keywords = self._extract_keywords(page_text, 5)
            image_key = f"page_{page_num+1}_img_{img_index}"
            
            for keyword in keywords:
                if keyword not in self.image_index:
                    self.image_index[keyword] = []
                self.image_index[keyword].append(image_key)
    
    def search_with_images(self, query: str, max_results: int = 5) -> dict:
        """搜索内容并返回相关图片"""
        results = {
            'text_results': [],
            'image_results': [],
            'sections': []
        }
        
        query_lower = query.lower()
        
        # 1. 搜索章节
        for section, content in self.sections.items():
            if query_lower in section.lower() or query_lower in content.lower():
                # 提取相关段落
                paragraphs = content.split('\n')
                relevant_content = []
                
                for para in paragraphs:
                    if query_lower in para.lower():
                        clean_para = re.sub(r'\s+', ' ', para).strip()
                        if len(clean_para) > 30:
                            relevant_content.append(clean_para)
                
                if relevant_content:
                    results['sections'].append({
                        'title': section,
                        'content': ' '.join(relevant_content[:2]),
                        'full_content': content[:1000]
                    })
        
        # 2. 搜索关键词索引
        for keyword in query_lower.split():
            if keyword in self.content_index:
                for item in self.content_index[keyword][:max_results]:
                    results['text_results'].append({
                        'type': 'keyword',
                        'keyword': keyword,
                        'content': item.get('context', item.get('content', '')),
                        'page': item.get('page', 1),
                        'relevance': item.get('relevance', 'medium')
                    })
        
        # 3. 搜索相关图片
        for keyword in query_lower.split():
            if keyword in self.image_index:
                for image_key in self.image_index[keyword][:3]:  # 最多3张图片
                    if image_key in self.images_cache:
                        image_info = self.images_cache[image_key]
                        results['image_results'].append({
                            'key': image_key,
                            'caption': image_info['caption'],
                            'base64': image_info['base64'],
                            'page': image_info['page'],
                            'related_keyword': keyword
                        })
        
        # 如果没有直接结果，尝试模糊匹配
        if not results['text_results'] and not results['image_results']:
            results = self._fuzzy_search(query)
        
        return results
    
    def _fuzzy_search(self, query: str) -> dict:
        """模糊搜索"""
        results = {
            'text_results': [],
            'image_results': [],
            'sections': []
        }
        
        # 在所有文本中搜索
        for page_num, text in self.text_cache.items():
            if query in text.lower():
                context = self._get_context(text, query, 300)
                results['text_results'].append({
                    'type': 'full_text',
                    'content': context,
                    'page': page_num + 1,
                    'relevance': 'medium'
                })
        
        return results
    
    def get_relevant_images(self, topic: str, limit: int = 3) -> list:
        """获取特定主题的相关图片"""
        images = []
        
        # 从图片索引中查找
        for keyword in topic.lower().split():
            if keyword in self.image_index:
                for image_key in self.image_index[keyword][:limit]:
                    if image_key in self.images_cache:
                        images.append(self.images_cache[image_key])
        
        # 如果没有找到，返回第一页的图片
        if not images:
            for key, img in self.images_cache.items():
                if img['page'] == 1:
                    images.append(img)
                    if len(images) >= limit:
                        break
        
        return images
    
    def get_page_images(self, page_num: int) -> list:
        """获取指定页面的所有图片"""
        images = []
        
        for key, img in self.images_cache.items():
            if img['page'] == page_num:
                images.append(img)
        
        return images
    
    def search_exact_content(self, exact_phrase: str) -> list:
        """精确短语搜索"""
        results = []
        
        for page_num, text in self.text_cache.items():
            positions = [m.start() for m in re.finditer(re.escape(exact_phrase), text, re.IGNORECASE)]
            
            for pos in positions[:3]:  # 最多3个匹配
                start = max(0, pos - 100)
                end = min(len(text), pos + len(exact_phrase) + 100)
                context = text[start:end]
                
                results.append({
                    'page': page_num + 1,
                    'position': pos,
                    'context': context,
                    'exact_match': exact_phrase
                })
        
        return results
    
    def generate_citation(self, content: str, max_length: int = 500) -> str:
        """生成引用格式的内容"""
        if not content:
            return ""
        
        # 查找内容在PDF中的位置
        for page_num, text in self.text_cache.items():
            if content[:100] in text:
                start_pos = text.find(content[:100])
                if start_pos != -1:
                    return f"《Python背记手册》第{page_num+1}页: {content[:max_length]}..."
        
        # 如果没找到，返回原始内容
        return content[:max_length] + "..."

class PythonProgrammingAgent:
    def __init__(self):
        self.tools = {
            "code_executor": self.code_executor,
            "syntax_checker": self.syntax_checker,
            "python_documentation": self.python_documentation,
            "code_analyzer": self.code_analyzer,
            "handbook_search": self.handbook_search,
            "enhanced_handbook_search": self.enhanced_handbook_search
        }

        # 初始化PDF手册
        pdf_path = os.path.join(os.path.dirname(__file__), 'static', 'Python背记手册.pdf')
        self.enhanced_handbook = EnhancedPDFHandbook(pdf_path)
        self.handbook = self.enhanced_handbook  # 保持向后兼容

        # 初始化模型
        self.llm = None
        try:
            self.llm = ChatOpenAI(
                model="deepseek-chat",
                base_url="https://api.deepseek.com/v1",
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                temperature=0.1
            )
            print("✅ 使用 DeepSeek 模型")
        except Exception as e:
            print(f"❌ DeepSeek 初始化失败: {e}")
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    api_key=os.getenv("OPENAI_API_KEY"),
                    temperature=0.1
                )
                print("✅ 使用 OpenAI 模型")
            except Exception as e2:
                print(f"❌ OpenAI 初始化失败: {e2}")
                print("⚠️ 使用简化模式（无API）")

        self.system_prompt = """你是一个专业的Python编程助手，专门解答Python相关的技术问题。你的职责包括：
1. 准确回答Python语法、库函数、最佳实践等问题
2. 提供可执行的代码示例
3. 解释代码逻辑和原理
4. 帮助调试和优化代码
5. 提供Python最新特性的信息
6. 当回答涉及《Python背记手册》的内容时，优先引用手册中的权威解释
7. 如果手册中有相关图表或示例图片，请在回答中明确指出并引用图片内容
8. 当用户上传代码或图表图片时，仔细分析图片内容并给出专业建议
9. 对于复杂概念，结合手册中的图示进行解释

请遵循以下原则：
- 确保代码示例是正确且可运行的
- 解释要清晰易懂，适合不同水平的开发者
- 提供实际应用场景
- 指出潜在的陷阱和注意事项
- 保持回答的专业性和准确性
- 使用Markdown格式美化回答，特别是代码块要用```python标记
- 如果从手册中找到相关信息，请注明"根据《Python背记手册》第X页..."
- 如果手册中有相关图表，请说明"手册中的图表展示了..."
- 对于复杂概念，建议用户查看手册中的图示"""

    def enhanced_handbook_search(self, query: str) -> str:
        """增强版手册搜索，包含图片"""
        try:
            results = self.enhanced_handbook.search_with_images(query)
            
            if not results['text_results'] and not results['image_results']:
                return f"在《Python背记手册》中未找到与'{query}'直接相关的内容。"
            
            response = "## 📚 《Python背记手册》相关内容\n\n"
            
            # 文本内容
            if results.get('text_results'):
                response += "### 📖 相关文本内容\n\n"
                for i, result in enumerate(results['text_results'][:3], 1):
                    citation = self.enhanced_handbook.generate_citation(result['content'])
                    response += f"{i}. **第{result.get('page', '?')}页** - {citation}\n\n"
            
            # 章节内容
            if results.get('sections'):
                response += "### 📑 相关章节\n\n"
                for i, section in enumerate(results['sections'][:2], 1):
                    response += f"{i}. **{section['title']}**\n"
                    response += f"   {section['content'][:200]}...\n\n"
            
            # 相关图片
            if results.get('image_results'):
                response += "### 🖼️ 相关图表和示例\n\n"
                response += "手册中包含以下相关图示：\n\n"
                for img in results['image_results'][:2]:
                    response += f"- **{img['caption']}** (第{img['page']}页)\n"
                    # 在响应中标记图片位置，由前端处理显示
                    response += f"[IMAGE:{img['caption']}]\n{img['base64']}\n[/IMAGE]\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"增强手册搜索失败: {e}")
            return f"搜索手册时出现错误: {str(e)}"

    def handbook_search(self, query: str) -> str:
        """从Python背记手册中搜索相关信息"""
        try:
            # 使用增强版搜索
            return self.enhanced_handbook_search(query)
            
        except Exception as e:
            logger.error(f"手册搜索失败: {e}")
            return f"搜索手册时出现错误: {str(e)}"

    def code_executor(self, code: str) -> str:
        """执行Python代码并返回结果。用于测试代码片段是否正确运行。"""
        try:
            dangerous_patterns = [
                r'__import__\s*\(', r'eval\s*\(', r'exec\s*\(', r'open\s*\(',
                r'os\.', r'subprocess\.', r'import\s+os', r'import\s+subprocess',
                r'import\s+sys', r'sys\.', r'__builtins__', r'globals\(\)',
                r'locals\(\)', r'rm\s+-', r'del\s+', r'format\s*\(.*\)\.__globals__'
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    return "错误：检测到可能不安全的代码，无法执行"

            # 额外的安全检查
            if any(keyword in code for keyword in ['__', 'breakpoint', 'compile', 'memoryview']):
                return "错误：代码包含受限关键字"

            cleaned_code = self._clean_python_code(code)
            if not cleaned_code:
                return "错误：代码为空或无法处理"

            # 使用subprocess执行代码
            result = subprocess.run(
                [sys.executable, "-c", cleaned_code],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                return f"✅ 执行成功:\n{output}" if output else "✅ 代码执行成功（无输出）"
            else:
                error_msg = result.stderr.strip()
                return f"❌ 执行错误:\n{error_msg}"

        except subprocess.TimeoutExpired:
            return "⏰ 错误：代码执行超时，可能存在无限循环"
        except Exception as e:
            return f"⚠️ 执行异常: {str(e)}"

    def syntax_checker(self, code: str) -> str:
        """检查Python代码的语法正确性。"""
        cleaned_code = _extract_code_snippet(code)
        if not cleaned_code:
            return "❌ 错误：代码为空"

        lines = cleaned_code.splitlines()
        try:
            tree = ast.parse(cleaned_code)
        except SyntaxError as e:
            context = _format_error_context(lines, e.lineno, e.offset)
            error_details = [
                "❌ 语法错误",
                f"- 类型: {e.msg}",
                f"- 位置: 第{e.lineno}行, 第{e.offset}列" if e.lineno and e.offset else "",
            ]
            if context:
                error_details.append("\n代码上下文：")
                error_details.append(context)
            error_details.append("\n建议：检查缩进、遗漏的冒号、括号或引号是否匹配。")
            return "\n".join([line for line in error_details if line])
        except Exception as e:
            return f"⚠️ 语法检查异常: {str(e)}"

        structure = _collect_code_structure(tree)
        docstring_issues = _docstring_gaps(tree)
        style_notes = _basic_style_checks(lines)
        name_issues = _detect_name_issues(tree)
        type_total = structure["type_hint_total"] or 1  # 避免除0
        type_ratio = structure["type_hint_annotated"] / type_total * 100

        report = [
            "✅ 语法检查通过：未发现语法错误",
            "",
            "结构概览:",
            f"• 总行数: {len(lines)}",
            f"• 函数数量: {len(structure['functions']) + len(structure['async_functions'])}",
            f"• 类数量: {len(structure['classes'])}",
            f"• 引入模块: {', '.join(structure['imports']) or '（无）'}",
        ]

        if structure["async_functions"]:
            async_names = ", ".join(fn["name"] for fn in structure["async_functions"])
            report.append(f"- 异步函数: {async_names}")

        report.extend([
            "",
            "类型注解覆盖率:",
            f"• 参数注解: {type_ratio:.0f}% ({structure['type_hint_annotated']}/{structure['type_hint_total']})"
            if structure["type_hint_total"]
            else "• 未检测到可统计的函数参数"
        ])

        if docstring_issues:
            report.extend([
                "",
                "文档提示:",
            ])
            for issue in docstring_issues[:5]:
                report.append(f"• {issue}")
            if len(docstring_issues) > 5:
                report.append("• ...")

        if name_issues:
            report.extend([
                "",
                "可能的名称或作用域问题:",
            ])
            suggestions = {
                "printf": "检测到 printf，Python 中请使用 print()。",
                "scanf": "检测到 scanf，Python 中可使用 input()。",
                "system": "请确认是否需要 import os 后使用 os.system。",
            }
            for name in sorted(name_issues.keys())[:6]:
                lines_info = ", ".join(f"第{ln}行" for ln in name_issues[name][:5])
                extra = suggestions.get(name.lower(), "")
                extra_text = f" {extra}" if extra else ""
                report.append(f"• {name}: {lines_info}{extra_text}")
            if len(name_issues) > 6:
                report.append("• ...")

        if style_notes:
            report.extend([
                "",
                "风格建议（节选）:",
            ])
            for note in style_notes[:5]:
                report.append(f"• {note}")
            if len(style_notes) > 5:
                report.append("• 更多风格问题请查看完整分析结果")

        return "\n".join(report)

    def python_documentation(self, topic: str) -> str:
        """提供Python官方文档中的相关信息。"""
        docs = {
            "列表推导式": {
                "description": "列表推导式提供了创建列表的简洁方式",
                "syntax": "[expression for item in iterable if condition]",
                "examples": [
                    "squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]",
                    "even_squares = [x**2 for x in range(10) if x % 2 == 0]  # [0, 4, 16, 36, 64]",
                    "pairs = [(x, y) for x in range(3) for y in range(3)]  # 嵌套循环"
                ]
            },
            "装饰器": {
                "description": "装饰器用于修改函数/类的行为",
                "syntax": "@decorator",
                "examples": [
                    "import time\ndef timer_decorator(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f'运行时间: {time.time()-start:.2f}秒')\n        return result\n    return wrapper\n\n@timer_decorator\ndef slow_func():\n    time.sleep(1)\n    return '完成'"
                ]
            },
            "生成器": {
                "description": "生成器是节省内存的迭代器，使用yield关键字",
                "syntax": "def generator_func(): yield value",
                "examples": [
                    "def number_gen(n):\n    for i in range(n):\n        yield i",
                    "squares = (x**2 for x in range(5))  # 生成器表达式"
                ]
            },
            "上下文管理器": {
                "description": "用于管理资源（文件/连接），使用with语句",
                "syntax": "with context_manager as var:",
                "examples": [
                    "with open('file.txt', 'w') as f:\n    f.write('Hello')",
                    "class Timer:\n    def __enter__(self):\n        self.start = time.time()\n        return self\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        print(f'耗时: {time.time()-self.start:.2f}秒')"
                ]
            },
            "异常处理": {
                "description": "捕获运行时错误",
                "syntax": "try-except-else-finally",
                "examples": [
                    "try:\n    result = 10 / 2\nexcept ZeroDivisionError:\n    print('不能除以零')\nelse:\n    print(f'结果: {result}')\nfinally:\n    print('清理完成')"
                ]
            },
            "面向对象": {
                "description": "支持类/对象/继承",
                "syntax": "class ClassName:",
                "examples": [
                    "class Person:\n    species = '人类'\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    def introduce(self):\n        return f'我叫{self.name}，{self.age}岁'\n    @classmethod\n    def get_species(cls):\n        return cls.species"
                ]
            }
        }

        topic_lower = topic.lower().strip()
        for key in docs:
            if topic_lower in key.lower():
                doc = docs[key]
                response = f"## {key}\n\n**描述**: {doc['description']}\n\n**语法**: `{doc['syntax']}`\n\n**示例**:\n"
                for example in doc['examples']:
                    response += f"```python\n{example}\n```\n"
                
                # 尝试从手册中搜索相关内容
                try:
                    handbook_results = self.enhanced_handbook_search(topic)
                    if "未找到" not in handbook_results:
                        response += f"\n## 📚 手册相关内容\n{handbook_results}"
                except:
                    pass
                
                return response

        # 如果在预定义文档中没找到，尝试从手册中搜索
        handbook_result = self.enhanced_handbook_search(topic)
        if "未找到" not in handbook_result:
            return handbook_result

        available_topics = "\n".join([f"- {t}" for t in docs.keys()])
        return f"未找到'{topic}'的文档。可用主题：\n{available_topics}"

    def code_analyzer(self, code: str) -> str:
        """分析Python代码，提供改进建议和最佳实践。"""
        cleaned_code = _extract_code_snippet(code)
        if not cleaned_code:
            return "❌ 错误：代码为空"

        lines = cleaned_code.splitlines()
        try:
            tree = ast.parse(cleaned_code)
        except SyntaxError as e:
            context = _format_error_context(lines, e.lineno, e.offset)
            details = [
                "❌ 检测到语法错误，无法继续分析。",
                f"- 错误: {e.msg}",
                f"- 位置: 第{e.lineno}行, 第{e.offset}列" if e.lineno and e.offset else "",
            ]
            if context:
                details.append("\n代码上下文：")
                details.append(context)
            details.append("\n请先修复语法问题后再次运行分析。")
            return "\n".join([line for line in details if line])

        structure = _collect_code_structure(tree)
        docstring_issues = _docstring_gaps(tree)
        style_notes = _basic_style_checks(lines)

        snake_case = re.compile(r'^[a-z_][a-z0-9_]*$')
        pascal_case = re.compile(r'^[A-Z][A-Za-z0-9]+$')

        complexity_notes = []
        maintainability_notes = []
        risk_notes = []
        naming_notes = []

        signature_lookup = {}
        for fn in structure["functions"] + structure["async_functions"]:
            signature_lookup[(fn["name"], fn["lineno"])] = fn

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                signature_meta = signature_lookup.get((node.name, node.lineno))
                args_repr = ", ".join(signature_meta["args"]) if signature_meta else "..."
                signature = f"{'async ' if isinstance(node, ast.AsyncFunctionDef) else ''}{node.name}({args_repr})"
                if signature_meta and signature_meta["returns"]:
                    signature += f" -> {signature_meta['returns']}"

                length = (getattr(node, 'end_lineno', node.lineno) or node.lineno) - node.lineno + 1
                complexity = _cyclomatic_complexity(node)
                depth = _max_nesting_depth(node)

                if complexity >= 12:
                    complexity_notes.append(f"- `{signature}` 的圈复杂度为 {complexity}，建议拆解逻辑或提取子函数")
                elif complexity >= 8:
                    complexity_notes.append(f"- `{signature}` 的圈复杂度为 {complexity}，接近上限，注意控制条件分支")

                if length > 80:
                    maintainability_notes.append(f"- `{signature}` 长度为 {length} 行，建议拆分为更小的函数")
                elif length > 40:
                    maintainability_notes.append(f"- `{signature}` 长度为 {length} 行，可考虑提取公共逻辑")

                if depth > 4:
                    maintainability_notes.append(f"- `{signature}` 的嵌套深度达到 {depth} 层，建议降低嵌套")

                # 可变默认参数
                mutable_nodes = (ast.List, ast.Dict, ast.Set)
                defaults = list(node.args.defaults) + [d for d in node.args.kw_defaults if d]
                if any(isinstance(default, mutable_nodes) for default in defaults):
                    risk_notes.append(f"- `{signature}` 使用可变对象作为默认参数，可能引发共享状态问题")

                # 命名规范
                if not snake_case.match(node.name):
                    naming_notes.append(f"- 函数 `{node.name}` 建议使用 snake_case 命名")

            elif isinstance(node, ast.ClassDef):
                if not pascal_case.match(node.name):
                    naming_notes.append(f"- 类 `{node.name}` 建议使用帕斯卡命名（如 `MyClass`）")

            elif isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    risk_notes.append("- 检测到裸 `except:`，请捕获具体异常类型")
                elif isinstance(node.type, ast.Name) and node.type.id in ("Exception", "BaseException"):
                    risk_notes.append("- 捕获了过于宽泛的异常 `Exception/BaseException`，建议更精确")

            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    risk_notes.append(f"- 使用 `{node.func.id}` 可能带来安全风险")
                elif isinstance(node.func, ast.Attribute):
                    attr = node.func.attr
                    owner = getattr(node.func.value, 'id', None)
                    if owner == 'os' and attr in {'system', 'popen'}:
                        risk_notes.append(f"- 调用 `os.{attr}` 可能执行系统命令，请确认安全性")
                    if owner == 'subprocess' and attr in {'Popen', 'call', 'run'}:
                        risk_notes.append("- 使用 `subprocess` 执行外部命令，请确保参数安全")

            elif isinstance(node, ast.Global):
                risk_notes.append(f"- 在第{node.lineno}行使用 `global` ，建议通过参数或返回值传递数据")

        todo_lines = [idx for idx, line in enumerate(lines, 1) if 'TODO' in line or 'FIXME' in line]
        if todo_lines:
            maintainability_notes.append(f"- 检测到未完成标记（TODO/FIXME）位于行: {', '.join(map(str, todo_lines[:5]))}")

        pattern_checks = [
            (r'from\s+\w+\s+import\s+\*', "- 避免 `from module import *`，可能污染命名空间"),
            (r'while\s+True\s*:', "- `while True` 请确保存在退出条件"),
        ]
        for pattern, message in pattern_checks:
            if re.search(pattern, cleaned_code):
                risk_notes.append(message)

        report = ["代码分析结果（专业增强版）"]
        report.extend([
            "",
            "结构概览:",
            f"• 行数: {len(lines)}",
            f"• 函数/异步函数: {len(structure['functions']) + len(structure['async_functions'])}",
            f"• 类: {len(structure['classes'])}",
            f"• 导入: {', '.join(structure['imports']) or '（无）'}",
        ])

        if structure["type_hint_total"]:
            ratio = structure["type_hint_annotated"] / structure["type_hint_total"] * 100
            report.append(
                f"• 参数类型注解覆盖率: {ratio:.0f}% ({structure['type_hint_annotated']}/{structure['type_hint_total']})")

        if complexity_notes:
            report.extend([
                "",
                "复杂度与可维护性:",
                *complexity_notes[:6]
            ])
        if maintainability_notes:
            if "复杂度与可维护性:" not in report:
                report.extend(["", "复杂度与可维护性:"])
            for note in maintainability_notes[:6]:
                report.append(note)

        if docstring_issues:
            report.extend([
                "",
                "文档与可读性:",
            ])
            for issue in docstring_issues[:6]:
                report.append(f"• {issue}")

        if naming_notes:
            report.extend([
                "",
                "命名规范:",
            ])
            for note in naming_notes[:5]:
                report.append(f"• {note}")

        if style_notes:
            report.extend([
                "",
                "风格建议（节选）:",
            ])
            for note in style_notes[:6]:
                report.append(f"• {note}")

        if risk_notes:
            report.extend([
                "",
                "潜在风险:",
            ])
            for note in risk_notes[:6]:
                report.append(f"• {note}")

        if not any([complexity_notes, maintainability_notes, docstring_issues, naming_notes, style_notes, risk_notes]):
            report.extend([
                "",
                "✅ 未发现明显的风格或质量问题，代码整体良好。"
            ])

        # 添加手册相关内容
        try:
            # 从代码中提取关键词
            keywords = self._extract_code_keywords(cleaned_code)
            if keywords:
                handbook_content = ""
                for keyword in keywords[:2]:  # 取前2个关键词
                    handbook_result = self.enhanced_handbook_search(keyword)
                    if "未找到" not in handbook_result:
                        handbook_content += f"\n\n关于 **{keyword}** 的手册参考：\n{handbook_result}"
                
                if handbook_content:
                    report.append("\n" + "="*50)
                    report.append("📚 相关手册内容")
                    report.append(handbook_content)
        except Exception as e:
            logger.error(f"添加手册内容失败: {e}")

        return "\n".join(report)

    def _clean_python_code(self, code: str) -> str:
        """清理要执行的Python代码"""
        code = re.sub(r'```python\s*|\s*```', '', code).strip()
        if not code:
            return ""

        lines = code.split('\n')
        last_line = lines[-1].strip()

        # 对孤立表达式添加print（仅在安全的情况下）
        if (last_line and not last_line.startswith(
                (' ', '\t', 'def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ', 'with ', '#', 'print(',
                 'return', 'yield', 'raise', 'try', 'except', 'finally'))
                and '=' not in last_line
                and not last_line.endswith((':', ';'))
                and not any(keyword in last_line for keyword in ['lambda', 'async', 'await'])):
            lines[-1] = f"print({last_line})"

        return '\n'.join(lines)

    def _extract_code_keywords(self, code: str) -> List[str]:
        """从代码中提取关键词"""
        # 常见的Python关键字和库
        python_keywords = {
            'def', 'class', 'import', 'from', 'as', 'try', 'except', 'finally',
            'with', 'async', 'await', 'yield', 'lambda', 'global', 'nonlocal'
        }
        
        # 常见的库名
        common_libs = {
            'numpy', 'pandas', 'matplotlib', 'requests', 'flask', 'django',
            'tensorflow', 'pytorch', 'sklearn', 'sqlalchemy', 'json', 'csv'
        }
        
        keywords = set()
        
        # 提取导入的库
        import_lines = re.findall(r'^(?:import|from)\s+([a-zA-Z0-9_\.]+)', code, re.MULTILINE)
        for lib in import_lines:
            lib_name = lib.split('.')[0]
            if lib_name in common_libs:
                keywords.add(lib_name)
        
        # 提取函数和类名
        func_names = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
        class_names = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:\(|:)', code)
        
        keywords.update(func_names)
        keywords.update(class_names)
        
        # 添加代码中出现的Python关键字
        for keyword in python_keywords:
            if keyword in code:
                keywords.add(keyword)
        
        return list(keywords)

    def _detect_tool_usage(self, question: str) -> dict:
        """检测用户问题是否需要使用工具"""
        question_lower = question.lower()

        tool_usage = {
            "use_tool": False,
            "tool_name": None,
            "tool_input": None
        }

        # 检测基础概念问题，优先使用手册搜索
        basic_concepts = ['是什么', '什么是', '定义', '概念', '介绍', '讲解', '说明', '含义']
        if any(concept in question_lower for concept in basic_concepts):
            # 提取关键词
            words = question_lower.split()
            keywords = [word for word in words if len(word) > 2 and word not in ['python', '什么', '如何', '怎样']]
            if keywords:
                tool_usage.update({
                    "use_tool": True,
                    "tool_name": "enhanced_handbook_search",
                    "tool_input": ' '.join(keywords[:3])  # 使用前3个关键词
                })

        # 检测代码执行
        elif any(word in question_lower for word in ['执行', '运行', '运行代码', '执行代码', 'test', 'run']):
            code_match = re.search(r'```python\s*(.*?)\s*```', question, re.DOTALL)
            if code_match:
                tool_usage.update({
                    "use_tool": True,
                    "tool_name": "code_executor",
                    "tool_input": code_match.group(1)
                })

        # 检测语法检查
        elif any(word in question_lower for word in ['语法', '语法检查', '语法错误', 'syntax']):
            code_match = re.search(r'```python\s*(.*?)\s*```', question, re.DOTALL)
            if code_match:
                tool_usage.update({
                    "use_tool": True,
                    "tool_name": "syntax_checker",
                    "tool_input": code_match.group(1)
                })

        # 检测代码分析
        elif any(word in question_lower for word in ['分析', '优化', '改进', '代码分析', 'analyze']):
            code_match = re.search(r'```python\s*(.*?)\s*```', question, re.DOTALL)
            if code_match:
                tool_usage.update({
                    "use_tool": True,
                    "tool_name": "code_analyzer",
                    "tool_input": code_match.group(1)
                })

        # 检测文档查询
        elif any(word in question_lower for word in ['文档', '说明', '介绍', '什么是', 'documentation']):
            for topic in ['列表推导式', '装饰器', '生成器', '上下文管理器', '异常处理', '面向对象', '异步编程',
                          '类型注解']:
                if topic in question:
                    tool_usage.update({
                        "use_tool": True,
                        "tool_name": "python_documentation",
                        "tool_input": topic
                    })
                    break

        return tool_usage

    def _should_search_handbook(self, question: str) -> bool:
        """判断问题是否需要搜索手册"""
        question_lower = question.lower()
        
        # 基础概念问题
        basic_concepts = [
            '是什么', '什么是', '定义', '概念', '介绍', '讲解', '说明', '含义',
            '怎么理解', '如何理解', '什么意思', '有什么区别', '有什么不同',
            '优点', '缺点', '特点', '特征', '特性'
        ]
        
        # 具体技术问题
        technical_terms = [
            '装饰器', '生成器', '迭代器', '上下文管理器', '元类', '描述符',
            'GIL', '垃圾回收', '内存管理', '多线程', '多进程', '协程',
            '异步', 'await', 'async', '列表推导', '字典推导', '集合推导',
            'lambda', '闭包', '作用域', '命名空间', '模块', '包'
        ]
        
        # 检查是否是基础概念问题
        for concept in basic_concepts:
            if concept in question_lower:
                return True
        
        # 检查是否包含具体技术术语
        for term in technical_terms:
            if term in question_lower:
                return True
        
        return False

    def _get_relevant_handbook_content(self, question: str) -> Optional[str]:
        """获取相关的手册内容"""
        try:
            # 提取问题中的关键词
            keywords = re.findall(r'[\u4e00-\u9fff]{2,5}|[a-zA-Z]{3,}', question)
            
            for keyword in keywords:
                if len(keyword) >= 2:  # 至少2个字符
                    result = self.enhanced_handbook_search(keyword)
                    if "未找到" not in result:
                        return result
            
            return None
        except:
            return None

    def _integrate_handbook_content(self, base_answer: str, handbook_content: str) -> str:
        """将手册内容整合到回答中"""
        # 简单的整合：在回答开头添加手册内容
        integration = f"""
## 🔍 手册参考

{handbook_content}

---

## 💡 我的解答

{base_answer}

> 📚 以上回答参考了《Python背记手册》中的相关内容，确保了解释的准确性和权威性。
"""
        return integration

    def ask_question(self, question: str) -> str:
        """向智能体提问关于Python编程的问题"""
        try:
            # 检测是否为需要手册引用的问题
            should_search_handbook = self._should_search_handbook(question)
            
            # 先获取手册内容（如果需要）
            handbook_content = None
            if should_search_handbook and self.enhanced_handbook:
                handbook_content = self._get_relevant_handbook_content(question)
            
            # 准备提问内容
            enhanced_question = question
            if handbook_content:
                # 将手册内容作为上下文添加到问题中
                enhanced_question = f"""
用户问题: {question}

根据《Python背记手册》相关内容:
{handbook_content}

请基于以上信息回答用户问题，确保回答准确且引用手册中的权威解释。
"""
            
            # 检测是否需要使用工具
            tool_info = self._detect_tool_usage(question)

            if tool_info["use_tool"]:
                tool_name = tool_info["tool_name"]
                tool_input = tool_info["tool_input"]

                if tool_name in self.tools:
                    print(f"🔧 使用工具: {tool_name}")
                    tool_result = self.tools[tool_name](tool_input)

                    # 如果有LLM，让LLM来解释工具结果
                    if self.llm:
                        enhanced_prompt = f"""用户的问题: {question}

工具执行结果:
{tool_result}

请基于工具执行结果，给用户一个完整、专业的回答。用中文回答，使用Markdown格式。如果可能，引用《Python背记手册》中的相关内容。"""

                        messages = [
                            SystemMessage(
                                content="你是一个Python编程助手，请基于工具执行结果和《Python背记手册》给用户提供专业、完整的回答。"),
                            HumanMessage(content=enhanced_prompt)
                        ]
                        response = self.llm.invoke(messages)
                        return response.content
                    else:
                        # 无LLM时直接返回工具结果
                        return f"**工具执行结果**:\n\n{tool_result}"

            # 如果没有使用工具或者工具使用失败，直接使用LLM
            if self.llm:
                messages = [
                    SystemMessage(content=self.system_prompt),
                    HumanMessage(content=enhanced_question)
                ]
                response = self.llm.invoke(messages)
                answer = response.content
                
                # 如果手册有相关内容且没包含在回答中，添加引用
                if handbook_content and "《Python背记手册》" not in answer:
                    answer = self._integrate_handbook_content(answer, handbook_content)
                
                return answer
            else:
                return self._local_answer(question)

        except Exception as e:
            error_msg = f"提问错误: {str(e)}"
            print(f"Error: {error_msg}")
            return f"⚠️ {error_msg}\n请检查API密钥或网络连接"

    def _local_answer(self, question: str) -> str:
        """无API时的本地回答"""
        q = question.lower()

        # 尝试使用工具
        tool_info = self._detect_tool_usage(question)
        if tool_info["use_tool"] and tool_info["tool_name"] in self.tools:
            return self.tools[tool_info["tool_name"]](tool_info["tool_input"])

        # 尝试从手册中搜索
        try:
            words = q.split()
            keywords = [word for word in words if len(word) > 2]
            if keywords:
                handbook_result = self.enhanced_handbook_search(' '.join(keywords[:2]))
                if "未找到" not in handbook_result:
                    return handbook_result
        except:
            pass

        # 本地知识库
        if any(w in q for w in ['列表推导', 'list comprehension']):
            return self.python_documentation("列表推导式")
        elif any(w in q for w in ['装饰器', 'decorator']):
            return self.python_documentation("装饰器")
        elif any(w in q for w in ['生成器', 'generator']):
            return self.python_documentation("生成器")
        elif any(w in q for w in ['上下文管理', 'context manager', 'with']):
            return self.python_documentation("上下文管理器")
        elif any(w in q for w in ['异常', 'exception', 'try', 'except']):
            return self.python_documentation("异常处理")
        elif any(w in q for w in ['类', 'class', '对象', 'object', '面向对象']):
            return self.python_documentation("面向对象")
        elif any(w in q for w in ['语法', 'syntax', '检查']):
            return "请提供Python代码，我将检查语法正确性（示例：\n```python\ndef add(a,b): return a+b\n```）"
        elif any(w in q for w in ['执行', '运行', 'test', 'run']):
            return "请提供Python代码，我将执行并返回结果（示例：\n```python\nprint([i for i in range(5)])\n```）"
        elif any(w in q for w in ['分析', '优化', '改进']):
            return "请提供Python代码，我将分析并给出改进建议（示例：\n```python\ndef calc():\n    total=0\n    for i in range(10): total+=i\n    print(total)\n```）"
        else:
            return "⚠️ 本地模式仅支持以下主题：\n- 列表推导式、装饰器、生成器\n- 上下文管理器、异常处理、面向对象\n- 代码语法检查、执行、分析优化\n如需更多回答，请配置DeepSeek/OpenAI API密钥"
