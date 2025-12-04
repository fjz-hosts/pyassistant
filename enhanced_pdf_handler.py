# enhanced_pdf_handler.py
import os
import re
import json
import base64
import hashlib
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Set
import logging
import fitz  # PyMuPDF - 更好的PDF处理
from PIL import Image
import numpy as np
from pathlib import Path
import pickle

logger = logging.getLogger(__name__)

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
            self.content = "PDF文件加载失败"
    
    def _extract_content(self):
        """提取PDF文本内容并建立结构"""
        all_text = ""
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text("text")
            self.text_cache[page_num] = text
            all_text += f"\n--- 第{page_num + 1}页 ---\n{text}"
            
            # 提取章节标题
            if page_num == 0:
                self._parse_sections_from_text(text)
        
        self.content = all_text
        self._build_section_index()
    
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
    
    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
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
            # 创建图片存储目录
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
    
    def search_with_images(self, query: str, max_results: int = 5) -> Dict:
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
    
    def _fuzzy_search(self, query: str) -> Dict:
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
    
    def get_relevant_images(self, topic: str, limit: int = 3) -> List[Dict]:
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
    
    def get_page_images(self, page_num: int) -> List[Dict]:
        """获取指定页面的所有图片"""
        images = []
        
        for key, img in self.images_cache.items():
            if img['page'] == page_num:
                images.append(img)
        
        return images
    
    def search_exact_content(self, exact_phrase: str) -> List[Dict]:
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