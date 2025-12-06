# markdown_handbook.py
import re
import base64
import hashlib
from typing import Dict, List, Optional, Tuple, Set
import logging
from pathlib import Path
import shutil
import urllib.parse

logger = logging.getLogger(__name__)

class MarkdownHandbook:
    """Markdown文档处理器，支持搜索Python-100-Days文件夹中的Markdown文件"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.md_files = []  # 所有Markdown文件路径
        self.content_index = {}  # 关键词到位置的索引
        self.image_index = {}    # 图片到内容的映射
        self.sections = {}       # 文件章节结构
        self.text_cache = {}     # 文件文本缓存
        self.images_cache = {}   # 图片缓存（本地图片）
        self.image_mapping = {}  # 图片路径映射
        self.load_markdown_files()
        
    def load_markdown_files(self):
        """加载所有Markdown文件"""
        try:
            # 遍历文件夹，找到所有.md文件
            for md_file in self.base_path.rglob("*.md"):
                self.md_files.append(md_file)
                self._index_file(md_file)
            
            logger.info(f"加载了 {len(self.md_files)} 个Markdown文件")
            self._build_global_index()
            
        except Exception as e:
            logger.error(f"加载Markdown文件失败: {e}")
    
    def _index_file(self, md_path: Path):
        """索引单个Markdown文件"""
        try:
            # 读取Markdown文件内容
            content = md_path.read_text(encoding='utf-8', errors='ignore')
            
            # 相对路径作为键
            rel_path = str(md_path.relative_to(self.base_path))
            file_key = rel_path.replace('\\', '/')
            
            # 缓存文本内容
            self.text_cache[file_key] = content
            
            # 提取章节结构
            self._parse_sections(file_key, content)
            
            # 提取图片信息
            self._extract_images(file_key, content, md_path)
            
            # 提取关键词
            keywords = self._extract_keywords(content)
            for keyword in keywords:
                if keyword not in self.content_index:
                    self.content_index[keyword] = []
                self.content_index[keyword].append({
                    'file': file_key,
                    'content': content[:500],  # 截取前500字符
                    'relevance': 'high'
                })
                
        except Exception as e:
            logger.error(f"索引文件 {md_path} 失败: {e}")
    
    def _parse_sections(self, file_key: str, content: str):
        """解析Markdown文件的章节结构"""
        lines = content.split('\n')
        current_section = "简介"
        section_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测Markdown标题（# 到 ######）
            if line.startswith('#'):
                # 保存上一个章节
                if section_lines:
                    section_key = f"{file_key}#{current_section}"
                    self.sections[section_key] = '\n'.join(section_lines)
                
                # 提取新章节标题
                # 移除#号和空格
                current_section = line.lstrip('#').strip()
                section_lines = []
            else:
                section_lines.append(line)
        
        # 保存最后一个章节
        if section_lines:
            section_key = f"{file_key}#{current_section}"
            self.sections[section_key] = '\n'.join(section_lines)
    
    def _extract_images(self, file_key: str, content: str, md_path: Path):
        """提取Markdown中的图片信息"""
        try:
            # 使用正则表达式匹配Markdown图片语法
            # ![alt text](image_url "title")
            img_pattern = r'!\[(.*?)\]\((.*?)(?:\s+"(.*?)")?\)'
            
            for match in re.finditer(img_pattern, content, re.IGNORECASE):
                alt_text = match.group(1) or "图片"
                img_url = match.group(2)
                title = match.group(3) or alt_text
                
                # 处理图片路径
                if img_url.startswith('http'):
                    # 网络图片，直接使用URL
                    img_key = f"web_{hashlib.md5(img_url.encode()).hexdigest()[:8]}"
                    self.images_cache[img_key] = {
                        'type': 'web',
                        'url': img_url,
                        'alt': alt_text,
                        'title': title,
                        'file': file_key,
                        'base64': None  # 网络图片不转换为base64
                    }
                else:
                    # 本地图片，需要处理相对路径
                    img_path = self._resolve_image_path(img_url, md_path)
                    if img_path and img_path.exists():
                        # 复制到静态目录
                        static_img_path = self._copy_to_static(img_path, file_key)
                        if static_img_path:
                            # 转换为base64
                            try:
                                img_bytes = img_path.read_bytes()
                                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                                
                                # 确定MIME类型
                                ext = img_path.suffix.lower()
                                mime_types = {
                                    '.png': 'image/png',
                                    '.jpg': 'image/jpeg',
                                    '.jpeg': 'image/jpeg',
                                    '.gif': 'image/gif',
                                    '.bmp': 'image/bmp',
                                    '.webp': 'image/webp'
                                }
                                mime_type = mime_types.get(ext, 'image/jpeg')
                                
                                img_key = f"local_{hashlib.md5(img_path.read_bytes()).hexdigest()[:8]}"
                                self.images_cache[img_key] = {
                                    'type': 'local',
                                    'path': str(static_img_path),
                                    'url': f'/static/images/handbook/{static_img_path.name}',
                                    'alt': alt_text,
                                    'title': title,
                                    'file': file_key,
                                    'base64': f'data:{mime_type};base64,{img_base64}'
                                }
                                
                                # 建立图片索引
                                keywords = self._extract_keywords(alt_text + ' ' + title)
                                for keyword in keywords:
                                    if keyword not in self.image_index:
                                        self.image_index[keyword] = []
                                    self.image_index[keyword].append(img_key)
                                    
                            except Exception as e:
                                logger.warning(f"无法读取图片 {img_path}: {e}")
                    
        except Exception as e:
            logger.error(f"提取图片失败: {e}")
    
    def _resolve_image_path(self, img_url: str, md_path: Path) -> Optional[Path]:
        """解析图片相对路径"""
        try:
            # 解码URL编码
            img_url = urllib.parse.unquote(img_url)
            
            # 移除可能的查询参数
            img_url = img_url.split('?')[0]
            
            # 处理不同的路径格式
            if img_url.startswith('/'):
                # 相对于项目根目录
                return self.base_path / img_url.lstrip('/')
            elif img_url.startswith('./'):
                # 相对于当前文件
                return md_path.parent / img_url[2:]
            elif img_url.startswith('../'):
                # 相对于上级目录
                return md_path.parent / img_url
            else:
                # 假设相对于当前文件
                return md_path.parent / img_url
                
        except Exception as e:
            logger.error(f"解析图片路径失败 {img_url}: {e}")
            return None
    
    def _copy_to_static(self, src_path: Path, file_key: str) -> Optional[Path]:
        """复制图片到静态目录"""
        try:
            # 创建静态图片目录
            static_dir = Path("static/images/handbook")
            static_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成唯一文件名
            file_hash = hashlib.md5(src_path.read_bytes()).hexdigest()[:8]
            ext = src_path.suffix
            filename = f"{file_key.replace('/', '_').replace('.', '_')}_{file_hash}{ext}"
            dest_path = static_dir / filename
            
            # 如果文件不存在，复制
            if not dest_path.exists():
                shutil.copy2(src_path, dest_path)
            
            return dest_path
            
        except Exception as e:
            logger.error(f"复制图片失败 {src_path}: {e}")
            return None
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """从文本中提取关键词"""
        # 移除停用词
        stop_words = {'的', '了', '和', '是', '在', '有', '就', '都', '而', '及', '与', '或', '等'}
        
        # 提取中英文单词
        words = re.findall(r'[\u4e00-\u9fff]{2,5}', text) + re.findall(r'\b[a-zA-Z]{3,}\b', text)
        
        # 统计词频
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 按频率排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def _build_global_index(self):
        """构建全局索引"""
        python_keywords = {
            'python', '语法', '函数', '类', '对象', '模块', '包', '异常', '装饰器',
            '生成器', '迭代器', '列表', '字典', '集合', '元组', '字符串',
            '文件', '输入输出', '多线程', '异步', '网络', '数据库',
            '测试', '调试', '性能', '优化', '算法', '数据结构', '爬虫',
            '数据分析', '机器学习', '深度学习', 'web开发', 'gui'
        }
        
        for file_key, content in self.text_cache.items():
            # 为每个关键词建立索引
            for keyword in python_keywords:
                if keyword.lower() in content.lower():
                    if keyword not in self.content_index:
                        self.content_index[keyword] = []
                    
                    # 提取上下文
                    context = self._get_context(content, keyword, 200)
                    self.content_index[keyword].append({
                        'file': file_key,
                        'context': context,
                        'type': 'keyword_match'
                    })
    
    def _get_context(self, text: str, keyword: str, context_size: int = 200) -> str:
        """获取关键词上下文"""
        # 不区分大小写搜索
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        match = pattern.search(text)
        if not match:
            return ""
        
        pos = match.start()
        start = max(0, pos - context_size // 2)
        end = min(len(text), pos + len(keyword) + context_size // 2)
        return text[start:end]
    
    def search_with_images(self, query: str, max_results: int = 5) -> Dict:
        """搜索内容并返回相关图片"""
        results = {
            'text_results': [],
            'image_results': [],
            'sections': []
        }
        
        query_lower = query.lower()
        
        # 1. 搜索章节
        for section_key, content in self.sections.items():
            if query_lower in section_key.lower() or query_lower in content.lower():
                # 提取文件名和章节名
                if '#' in section_key:
                    file_part, section_part = section_key.split('#', 1)
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
                            'file': file_part,
                            'title': section_part,
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
                        'file': item.get('file', ''),
                        'relevance': item.get('relevance', 'medium')
                    })
        
        # 3. 搜索相关图片
        for keyword in query_lower.split():
            if keyword in self.image_index:
                for image_key in self.image_index[keyword][:3]:
                    if image_key in self.images_cache:
                        image_info = self.images_cache[image_key]
                        results['image_results'].append({
                            'key': image_key,
                            'caption': image_info['title'],
                            'base64': image_info.get('base64'),
                            'url': image_info.get('url'),
                            'file': image_info['file'],
                            'related_keyword': keyword,
                            'type': image_info['type']
                        })
        
        # 如果没有直接结果，尝试模糊匹配
        if not results['text_results'] and not results['image_results']:
            results = self._fuzzy_search(query)
        
        return results
    
    def _fuzzy_search(self, query: str) -> Dict:
        """模糊搜索"""
        results = {
            'text_results': [],
            'image_results': [],
            'sections': []
        }
        
        # 在所有文本中搜索
        for file_key, text in self.text_cache.items():
            if query.lower() in text.lower():
                context = self._get_context(text, query, 300)
                results['text_results'].append({
                    'type': 'full_text',
                    'content': context,
                    'file': file_key,
                    'relevance': 'medium'
                })
        
        return results
    
    def get_relevant_images(self, topic: str, limit: int = 3) -> List[Dict]:
        """获取特定主题的相关图片"""
        images = []
        
        # 从图片索引中查找
        for keyword in topic.lower().split():
            if keyword in self.image_index:
                for image_key in self.image_index[keyword][:limit]:
                    if image_key in self.images_cache:
                        images.append(self.images_cache[image_key])
        
        # 如果没有找到，返回README文件中的图片
        if not images:
            for key, img in self.images_cache.items():
                if 'README' in img['file']:
                    images.append(img)
                    if len(images) >= limit:
                        break
        
        return images
    
    def search_exact_content(self, exact_phrase: str) -> List[Dict]:
        """精确短语搜索"""
        results = []
        
        for file_key, text in self.text_cache.items():
            positions = [m.start() for m in re.finditer(re.escape(exact_phrase), text, re.IGNORECASE)]
            
            for pos in positions[:3]:
                start = max(0, pos - 100)
                end = min(len(text), pos + len(exact_phrase) + 100)
                context = text[start:end]
                
                results.append({
                    'file': file_key,
                    'position': pos,
                    'context': context,
                    'exact_match': exact_phrase
                })
        
        return results
    
    def generate_citation(self, content: str, max_length: int = 500) -> str:
        """生成引用格式的内容"""
        if not content:
            return ""
        
        # 在所有文件中查找
        for file_key, text in self.text_cache.items():
            if content[:100] in text:
                start_pos = text.find(content[:100])
                if start_pos != -1:
                    return f"《Python-100-Days》{file_key}: {content[:max_length]}..."
        
        # 如果没找到，返回原始内容
        return content[:max_length] + "..."
    
    def get_file_content(self, file_path: str) -> Optional[str]:
        """获取指定文件的内容"""
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                return full_path.read_text(encoding='utf-8', errors='ignore')
        except:
            pass
        return None