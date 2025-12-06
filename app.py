# app.py
from flask import Flask, render_template, request, jsonify, session, Response, redirect, url_for
from datetime import datetime
import json
from python_agent import PythonProgrammingAgent
import markdown
import html
import time
import os
import subprocess
import re
import base64
from io import BytesIO
import threading
import hashlib
from urllib.parse import urlencode
import logging
import tempfile
import pymysql
from functools import wraps
import uuid
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
from pathlib import Path
import hmac

# 延迟导入websocket，避免启动时错误
try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    websocket = None

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

# 配置文件上传
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
UPLOAD_FOLDER = 'static/uploads'
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_IMAGE_SIZE

# 创建上传目录
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/images/handbook', exist_ok=True)

def allowed_file(filename):
    """检查文件扩展名"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

# 添加自定义Jinja2过滤器：HTML实体解码
@app.template_filter('unescape')
def unescape_filter(s):
    """解码HTML实体"""
    if not s:
        return s
    return html.unescape(str(s))

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 数据库连接池
db_connection = None

def get_db_connection():
    """获取数据库连接"""
    global db_connection
    try:
        # 检查连接是否存在且有效
        if db_connection is None:
            db_connection = pymysql.connect(**DB_CONFIG)
        else:
            # 尝试ping来检查连接是否有效
            try:
                db_connection.ping(reconnect=True)
            except:
                # 如果ping失败，重新连接
                db_connection.close()
                db_connection = pymysql.connect(**DB_CONFIG)
        return db_connection
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        # 尝试重新连接一次
        try:
            db_connection = pymysql.connect(**DB_CONFIG)
            return db_connection
        except:
            raise

def init_database():
    """初始化数据库表结构"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 创建用户表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_username (username)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)

            # 创建对话表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(255) DEFAULT '新对话',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_updated_at (updated_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)

            # 创建消息表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    conversation_id INT NOT NULL,
                    role ENUM('user', 'assistant', 'system') NOT NULL,
                    content TEXT NOT NULL,
                    message_type VARCHAR(20) DEFAULT 'text',
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
                    INDEX idx_conversation_id (conversation_id),
                    INDEX idx_timestamp (timestamp)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)

            conn.commit()
            logger.info("数据库表初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise

def require_login(f):
    """登录装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function

# 初始化智能体
python_agent = None

def initialize_agent():
    """初始化Python编程助手"""
    global python_agent
    try:
        python_agent = PythonProgrammingAgent()
        print("✅ Python编程助手初始化成功")
        return True
    except Exception as e:
        print(f"❌ Python编程助手初始化失败: {e}")

        # 创建一个基本的回退类
        class FallbackAgent:
            def __init__(self):
                self.name = "Python编程助手（基础模式）"
                self.enhanced_handbook = None

            def ask_question(self, question: str) -> str:
                return f"⚠️ 系统初始化失败，当前运行在基础模式。\n\n您的问题是：{question}\n\n请检查：\n1. API密钥配置\n2. 网络连接\n3. 依赖包安装"

            def syntax_checker(self, code: str) -> str:
                return "语法检查功能在当前模式下不可用，请检查系统初始化状态"

            def code_executor(self, code: str) -> str:
                return "代码执行功能在当前模式下不可用，请检查系统初始化状态"

            def code_analyzer(self, code: str) -> str:
                return "代码分析功能在当前模式下不可用，请检查系统初始化状态"

            def enhanced_handbook_search(self, query: str) -> str:
                return "增强手册搜索功能在当前模式下不可用"

        python_agent = FallbackAgent()
        return False

# Markdown处理器类
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
                                'path': str(img_path),
                                'url': img_url,
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
    
    def _resolve_image_path(self, img_url: str, md_path: Path):
        """解析图片相对路径"""
        try:
            # 解码URL编码
            import urllib.parse
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
    
    def _extract_keywords(self, text: str, max_keywords: int = 10):
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
    
    def _get_context(self, text: str, keyword: str, context_size: int = 200):
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
    
    def search_with_images(self, query: str, max_results: int = 5):
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
    
    def _fuzzy_search(self, query: str):
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
    
    def get_relevant_images(self, topic: str, limit: int = 3):
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
    
    def get_page_images(self, page_num: int):
        """获取指定页面的所有图片（为兼容性保留）"""
        images = []
        return images
    
    def search_exact_content(self, exact_phrase: str):
        """精确短语搜索"""
        results = []
        
        for file_key, text in self.text_cache.items():
            positions = [m.start() for m in re.finditer(re.escape(exact_phrase), text, re.IGNORECASE)]
            
            for pos in positions[:3]:  # 最多3个匹配
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
    
    def generate_citation(self, content: str, max_length: int = 500):
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
    
    def get_file_content(self, file_path: str):
        """获取指定文件的内容"""
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                return full_path.read_text(encoding='utf-8', errors='ignore')
        except:
            pass
        return None

# 初始化Markdown处理器
enhanced_handbook = None

def initialize_markdown_handbook():
    """初始化Markdown文档处理器"""
    global enhanced_handbook
    try:
        base_path = os.path.join(os.path.dirname(__file__), 'static', 'Python-100-Days-master')
        enhanced_handbook = MarkdownHandbook(base_path)
        print("✅ Markdown文档处理器初始化成功")
        print(f"   加载了 {len(enhanced_handbook.md_files)} 个Markdown文件")
        print(f"   索引了 {len(enhanced_handbook.images_cache)} 张图片")
        return True
    except Exception as e:
        print(f"❌ Markdown文档处理器初始化失败: {e}")
        enhanced_handbook = None
        return False

def save_uploaded_image(file):
    """保存上传的图片并返回路径和base64"""
    try:
        if file and allowed_file(file.filename):
            # 生成唯一文件名
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # 读取文件内容
            image_data = file.read()
            
            # 检查文件大小
            if len(image_data) > MAX_IMAGE_SIZE:
                raise ValueError(f"图片大小不能超过{MAX_IMAGE_SIZE // 1024 // 1024}MB")
            
            # 保存文件
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            # 转换为base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            mime_type = file.content_type or 'image/jpeg'
            
            return {
                'success': True,
                'filename': unique_filename,
                'filepath': filepath,
                'url': f'/static/uploads/{unique_filename}',
                'base64': f'data:{mime_type};base64,{image_base64}',
                'size': len(image_data)
            }
        else:
            return {
                'success': False,
                'error': '不支持的文件格式'
            }
    except Exception as e:
        logger.error(f"保存图片失败: {e}")
        return {
            'success': False,
            'error': str(e)
        }

# 启动时初始化
try:
    init_database()
    logger.info("✅ 数据库连接成功")
except Exception as e:
    logger.error(f"❌ 数据库初始化失败: {e}")

initialize_agent()
initialize_markdown_handbook()

# 工具函数：删除空白对话
def delete_empty_conversations(user_id: int):
    """删除指定用户的空白对话（没有任何消息的对话）"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM conversations
                WHERE user_id = %s
                AND NOT EXISTS (
                    SELECT 1 FROM messages WHERE messages.conversation_id = conversations.id
                )
            """, (user_id,))
            conn.commit()
    except Exception as e:
        logger.error(f"删除空白对话失败: {e}")

# 存储对话历史（数据库版本）
def get_current_conversation_id():
    """获取当前对话ID，如果不存在则创建新对话"""
    if 'user_id' not in session:
        return None

    if 'conversation_id' not in session:
        # 创建新对话
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO conversations (user_id, title) VALUES (%s, %s)",
                    (session['user_id'], '新对话')
                )
                conn.commit()
                conversation_id = cursor.lastrowid
                session['conversation_id'] = conversation_id
                session.modified = True
                return conversation_id
        except Exception as e:
            logger.error(f"创建对话失败: {e}")
            return None

    return session.get('conversation_id')

def get_chat_history():
    """从数据库获取对话历史"""
    conversation_id = get_current_conversation_id()
    if not conversation_id:
        return []

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT role, content as message, message_type as type, "
                "DATE_FORMAT(timestamp, '%%H:%%i:%%S') as timestamp "
                "FROM messages WHERE conversation_id = %s ORDER BY timestamp ASC",
                (conversation_id,)
            )
            messages = cursor.fetchall()
            # 解码HTML实体，确保特殊字符正常显示
            result = []
            for msg in messages:
                msg_dict = dict(msg)
                # 如果消息内容包含HTML实体，需要解码
                # 注意：这里不直接解码，让前端处理，因为HTML类型的内容可能需要保持原样
                result.append(msg_dict)
            return result
    except Exception as e:
        logger.error(f"获取对话历史失败: {e}")
        return []

def add_to_chat_history(role, message, message_type="text"):
    """添加消息到数据库"""
    conversation_id = get_current_conversation_id()
    if not conversation_id:
        return

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO messages (conversation_id, role, content, message_type) VALUES (%s, %s, %s, %s)",
                (conversation_id, role, message, message_type)
            )
            # 更新对话标题（如果是第一条用户消息）
            if role == 'user':
                cursor.execute(
                    "SELECT COUNT(*) as count FROM messages WHERE conversation_id = %s AND role = 'user'",
                    (conversation_id,)
                )
                result = cursor.fetchone()
                if result and result['count'] == 1:
                    # 第一条用户消息，使用前30个字符作为标题
                    title = message[:30] if len(message) <= 30 else message[:27] + '...'
                    cursor.execute(
                        "UPDATE conversations SET title = %s WHERE id = %s",
                        (title, conversation_id)
                    )
            conn.commit()
    except Exception as e:
        logger.error(f"保存消息失败: {e}")

def process_ai_response(response_text):
    """
    处理AI响应，提取并显示图像
    """
    # 正则表达式匹配图像标记
    image_pattern = r'\[IMAGE:([^\]]+)\](.*?)\[/IMAGE\]'

    # 查找所有图像
    images = re.findall(image_pattern, response_text, re.DOTALL)

    # 移除原始图像标记
    clean_text = re.sub(image_pattern, '', response_text)

    try:
        # 将Markdown转换为HTML
        escaped_text = html.escape(clean_text)
        html_content = markdown.markdown(
            escaped_text,
            extensions=['fenced_code', 'codehilite', 'tables']
        )
    except Exception as e:
        print(f"Markdown转换错误: {e}")
        html_content = f"<pre>{html.escape(clean_text)}</pre>"

    # 添加图像
    for img_name, img_data in images:
        # 清理图像数据（移除可能的换行符和空格）
        img_data_clean = img_data.strip().replace('\n', '').replace('\r', '')

        html_content += f'''
        <div class="result-image">
            <div class="image-title">{img_name.replace("_", " ").title()}</div>
            <img src="data:image/png;base64,{img_data_clean}" alt="{img_name}" />
        </div>
        '''

    return html_content

class XunfeiVoiceRecognition:
    def __init__(self):
        self.app_id = os.getenv('XF_APP_ID')
        self.api_key = os.getenv('XF_API_KEY')
        self.api_secret = os.getenv('XF_API_SECRET')
        self.ws_url = "wss://iat-api.xfyun.cn/v2/iat"
        self.result_text = ""
        self.is_finished = False
        self.error_message = None

    def create_url(self):
        """创建WebSocket连接URL"""
        from datetime import datetime
        now = datetime.now()
        date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

        signature_origin = f"host: iat-api.xfyun.cn\ndate: {date}\nGET /v2/iat HTTP/1.1"
        signature_sha = base64.b64encode(
            hmac.new(
                self.api_secret.encode('utf-8'),
                signature_origin.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest()
        ).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 修复这里的字符串格式化问题
        params = {
            'authorization': authorization,
            'date': date,
            'host': 'iat-api.xfyun.cn'
        }
        query_string = urlencode(params)
        url = f"{self.ws_url}?{query_string}"

        return url

    def on_message(self, ws, message):
        """处理WebSocket消息"""
        try:
            data = json.loads(message)
            logger.info(f"收到讯飞消息: {data}")

            code = data.get("code")
            if code is not None and code != 0:
                error_msg = data.get('message', f'错误代码: {code}')
                logger.error(f"讯飞API错误: {error_msg}")
                self.error_message = f"讯飞API错误: {error_msg}"
                self.is_finished = True
                ws.close()
                return

            data_section = data.get("data")
            if data_section:
                # 处理识别结果
                result = data_section.get("result", {})
                if result and result.get("ws"):
                    for ws_data in result["ws"]:
                        if "cw" in ws_data:
                            for cw in ws_data["cw"]:
                                if "w" in cw:
                                    word = cw["w"]
                                    self.result_text += word
                                    logger.debug(f"识别到文字: {word}")

                # 检查是否结束
                status = data_section.get("status")
                if status == 2:
                    logger.info(f"识别完成，结果: {self.result_text}")
                    self.is_finished = True
                    ws.close()
                elif status == 1:
                    logger.debug("识别进行中...")
            else:
                logger.debug(f"收到消息但无data字段: {data}")

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}, 消息内容: {message[:200]}")
            self.error_message = f"消息解析错误: {str(e)}"
            self.is_finished = True
            ws.close()
        except Exception as e:
            logger.error(f"处理讯飞消息错误: {e}", exc_info=True)
            self.error_message = f"处理识别结果错误: {str(e)}"
            self.is_finished = True
            ws.close()

    def on_error(self, ws, error):
        """处理WebSocket错误"""
        logger.error(f"WebSocket错误: {error}")
        self.error_message = f"连接错误: {str(error)}"
        self.is_finished = True

    def on_close(self, ws, close_status_code, close_msg):
        """WebSocket关闭回调"""
        logger.info("WebSocket连接关闭")

    def on_open(self, ws):
        """WebSocket打开回调"""
        logger.info("WebSocket连接已建立")

        # 发送开始帧
        frame_data = {
            "common": {
                "app_id": self.app_id
            },
            "business": {
                "language": "zh_cn",
                "domain": "iat",
                "accent": "mandarin",
                "vad_eos": 10000
            },
            "data": {
                "status": 0,
                "format": "audio/L16;rate=16000",
                "audio": "",
                "encoding": "raw"
            }
        }
        ws.send(json.dumps(frame_data))

    def recognize_audio(self, audio_data):
        """识别音频数据"""
        if not WEBSOCKET_AVAILABLE:
            return {
                'success': False,
                'text': '',
                'error': 'websocket-client未安装，请运行: pip install websocket-client'
            }

        try:
            # 重置状态
            self.result_text = ""
            self.is_finished = False
            self.error_message = None

            # 创建WebSocket连接
            url = self.create_url()
            logger.info(f"连接讯飞语音识别，音频数据大小: {len(audio_data)} 字节")

            ws = websocket.WebSocketApp(
                url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open
            )

            # 使用线程锁确保连接状态同步
            connection_ready = threading.Event()
            ws_connected = [False]  # 使用列表以便在闭包中修改

            def on_open_wrapper(ws_app):
                """包装on_open，设置连接就绪标志"""
                self.on_open(ws_app)
                ws_connected[0] = True
                connection_ready.set()

            ws.on_open = on_open_wrapper

            # 在单独的线程中运行WebSocket
            def run_ws():
                try:
                    ws.run_forever()
                except Exception as e:
                    logger.error(f"WebSocket运行异常: {e}")
                    self.error_message = f"WebSocket运行异常: {str(e)}"
                    self.is_finished = True
                    connection_ready.set()

            ws_thread = threading.Thread(target=run_ws)
            ws_thread.daemon = True
            ws_thread.start()

            # 等待连接建立（最多等待5秒）
            if not connection_ready.wait(timeout=5):
                logger.error("WebSocket连接超时")
                ws.close()
                return {
                    'success': False,
                    'text': '',
                    'error': 'WebSocket连接超时，请检查网络连接'
                }

            if not ws_connected[0] or not (ws.sock and ws.sock.connected):
                logger.error("WebSocket连接失败")
                return {
                    'success': False,
                    'text': '',
                    'error': 'WebSocket连接失败'
                }

            logger.info("WebSocket连接已建立，开始发送音频数据")

            # 将音频数据分帧发送
            frame_size = 1280  # 40ms的帧 (16kHz * 2字节 * 0.04秒 = 1280字节)
            total_frames = (len(audio_data) + frame_size - 1) // frame_size
            logger.info(f"准备发送 {total_frames} 帧音频数据")

            frames_sent = 0
            for i in range(0, len(audio_data), frame_size):
                if not (ws.sock and ws.sock.connected):
                    logger.warning("WebSocket连接已断开，停止发送")
                    break

                chunk = audio_data[i:i + frame_size]
                if chunk:
                    # 发送音频帧
                    frame = {
                        "data": {
                            "status": 1,
                            "format": "audio/L16;rate=16000",
                            "audio": base64.b64encode(chunk).decode('utf-8'),
                            "encoding": "raw"
                        }
                    }
                    try:
                        ws.send(json.dumps(frame))
                        frames_sent += 1
                        if frames_sent % 10 == 0:
                            logger.debug(f"已发送 {frames_sent}/{total_frames} 帧")
                    except Exception as e:
                        logger.error(f"发送音频帧失败: {e}")
                        break
                    time.sleep(0.04)  # 模拟实时音频流

            logger.info(f"音频数据发送完成，共发送 {frames_sent} 帧")

            # 发送结束帧
            if ws.sock and ws.sock.connected:
                end_frame = {
                    "data": {
                        "status": 2,
                        "format": "audio/L16;rate=16000",
                        "audio": "",
                        "encoding": "raw"
                    }
                }
                try:
                    ws.send(json.dumps(end_frame))
                    logger.info("已发送结束帧")
                except Exception as e:
                    logger.error(f"发送结束帧失败: {e}")

            # 等待识别完成（增加超时时间到15秒）
            timeout = 15
            start_time = time.time()
            while not self.is_finished and time.time() - start_time < timeout:
                if not (ws.sock and ws.sock.connected):
                    logger.warning("WebSocket连接已断开")
                    break
                time.sleep(0.1)

            if not self.is_finished:
                if self.error_message:
                    logger.error(f"识别失败: {self.error_message}")
                else:
                    logger.warning("识别超时，但未收到错误信息")
                    self.error_message = "识别超时，可能音频数据有问题或网络连接不稳定"
                ws.close()

            # 等待WebSocket线程结束
            ws_thread.join(timeout=2)

            result_text = self.result_text.strip()
            logger.info(f"识别完成，结果: '{result_text}', 成功: {self.is_finished and not self.error_message}")

            return {
                'success': self.is_finished and not self.error_message,
                'text': result_text,
                'error': self.error_message
            }

        except Exception as e:
            logger.error(f"语音识别异常: {e}", exc_info=True)
            return {
                'success': False,
                'text': '',
                'error': f'识别异常: {str(e)}'
            }

def convert_audio_to_pcm(audio_data):
    """将音频转换为PCM格式（优先使用pydub在内存中转换）"""
    # 首先尝试使用pydub（完全在内存中，无需临时文件）
    try:
        from pydub import AudioSegment

        logger.info("使用pydub在内存中转换音频...")

        # 将音频数据从内存中读取（无需临时文件）
        audio_segment = AudioSegment.from_file(BytesIO(audio_data), format="webm")

        logger.info(
            f"原始音频: {audio_segment.channels}声道, {audio_segment.frame_rate}Hz, 时长: {len(audio_segment)}ms")

        # 转换为单声道、16kHz采样率、16位深度
        audio_segment = audio_segment.set_channels(1)  # 单声道
        audio_segment = audio_segment.set_frame_rate(16000)  # 16kHz采样率
        audio_segment = audio_segment.set_sample_width(2)  # 16位 = 2字节

        logger.info(
            f"转换后音频: {audio_segment.channels}声道, {audio_segment.frame_rate}Hz, 时长: {len(audio_segment)}ms")

        # 导出为原始PCM数据（无WAV头，纯PCM数据）
        pcm_data = audio_segment.raw_data

        if len(pcm_data) == 0:
            raise Exception("pydub转换后数据为空")

        logger.info(f"✅ 使用pydub转换成功，PCM数据大小: {len(pcm_data)} 字节")
        return pcm_data

    except ImportError:
        logger.warning("pydub未安装，将使用ffmpeg（需要临时文件）")
        logger.info("建议安装pydub以在内存中转换: pip install pydub")
    except Exception as e:
        logger.warning(f"pydub转换失败: {e}，将尝试使用ffmpeg...")
        logger.debug(f"pydub错误详情: {e}", exc_info=True)

    # 如果pydub不可用或失败，使用ffmpeg（需要临时文件）
    temp_input = None
    temp_output = None
    try:
        # 使用系统临时目录，避免权限问题
        temp_dir = tempfile.gettempdir()
        logger.info(f"使用ffmpeg转换，临时目录: {temp_dir}")

        # 检查临时目录权限
        if not os.access(temp_dir, os.W_OK):
            raise Exception(f"临时目录无写权限: {temp_dir}。建议安装pydub以在内存中转换: pip install pydub")

        # 创建临时文件（使用系统临时目录）
        timestamp = int(time.time() * 1000000)  # 使用微秒提高唯一性
        process_id = os.getpid()
        temp_input = os.path.join(temp_dir, f"pyassistant_input_{process_id}_{timestamp}.webm")
        temp_output = os.path.join(temp_dir, f"pyassistant_output_{process_id}_{timestamp}.pcm")

        logger.info(f"保存临时输入文件: {temp_input}, 大小: {len(audio_data)} 字节")

        # 尝试创建文件，捕获权限错误
        try:
            with open(temp_input, 'wb') as f:
                f.write(audio_data)
            # 验证文件是否成功创建
            if not os.path.exists(temp_input):
                raise Exception(f"临时文件创建失败: {temp_input}")
            logger.info(f"临时文件创建成功: {temp_input}")
        except PermissionError as e:
            raise Exception(f"无权限创建临时文件: {temp_input}, 错误: {str(e)}。建议安装pydub: pip install pydub")
        except OSError as e:
            raise Exception(f"创建临时文件失败: {temp_input}, 错误: {str(e)}。建议安装pydub: pip install pydub")

        # 检查ffmpeg是否可用
        try:
            # 检查ffmpeg命令
            check_cmd = ['ffmpeg', '-version']
            check_result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=5)
            if check_result.returncode != 0:
                logger.error("ffmpeg命令执行失败，可能未正确安装")
                raise Exception("ffmpeg未正确安装或不在PATH中。建议安装pydub: pip install pydub")
        except FileNotFoundError:
            logger.error("ffmpeg未找到，请确保已安装ffmpeg并添加到系统PATH")
            raise Exception(
                "ffmpeg未找到。请安装ffmpeg (https://ffmpeg.org/download.html) 或安装pydub: pip install pydub")
        except subprocess.TimeoutExpired:
            logger.error("ffmpeg检查超时")
            raise Exception("ffmpeg检查超时")

        # 使用ffmpeg转换音频格式为原始PCM
        # 注意：输出为原始PCM数据（无WAV头）
        cmd = [
            'ffmpeg', '-i', temp_input,
            '-acodec', 'pcm_s16le',  # 16位小端PCM编码
            '-ac', '1',  # 单声道
            '-ar', '16000',  # 采样率16kHz
            '-f', 's16le',  # 输出格式为16位小端原始PCM
            '-y',  # 覆盖输出文件
            temp_output
        ]

        logger.info(f"执行ffmpeg命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            if not os.path.exists(temp_output):
                logger.error(f"输出文件不存在: {temp_output}")
                # 检查是否有权限读取
                if os.path.exists(temp_input):
                    try:
                        os.remove(temp_input)
                    except:
                        pass
                return None

            # 检查输出文件权限
            if not os.access(temp_output, os.R_OK):
                logger.error(f"输出文件无读权限: {temp_output}")
                return None

            try:
                with open(temp_output, 'rb') as f:
                    pcm_data = f.read()
            except PermissionError as e:
                logger.error(f"无权限读取输出文件: {temp_output}, 错误: {str(e)}")
                return None
            except Exception as e:
                logger.error(f"读取输出文件失败: {temp_output}, 错误: {str(e)}")
                return None

            if len(pcm_data) == 0:
                logger.error("转换后的PCM数据为空")
                return None

            logger.info(f"音频转换成功，PCM数据大小: {len(pcm_data)} 字节")

            # 清理临时文件
            try:
                if os.path.exists(temp_input):
                    os.remove(temp_input)
                    logger.debug(f"已删除临时输入文件: {temp_input}")
                if os.path.exists(temp_output):
                    os.remove(temp_output)
                    logger.debug(f"已删除临时输出文件: {temp_output}")
            except PermissionError as e:
                logger.warning(f"无权限删除临时文件: {e}")
            except Exception as cleanup_error:
                logger.warning(f"清理临时文件失败: {cleanup_error}")

            return pcm_data
        else:
            error_msg = result.stderr or result.stdout or "未知错误"
            logger.error(f"ffmpeg转换失败 (返回码: {result.returncode}): {error_msg}")
            # 返回详细错误信息
            raise Exception(f"ffmpeg转换失败: {error_msg[:200]}")  # 限制错误信息长度

    except subprocess.TimeoutExpired:
        logger.error("ffmpeg转换超时")
        raise Exception("音频转换超时，请重试。建议安装pydub以在内存中转换: pip install pydub")
    except FileNotFoundError as e:
        logger.error(f"文件未找到: {e}")
        raise Exception("ffmpeg未找到，请安装ffmpeg并添加到系统PATH，或安装pydub以在内存中转换: pip install pydub")
    except PermissionError as e:
        logger.error(f"文件权限错误: {e}", exc_info=True)
        raise Exception(f"文件权限错误: {str(e)}。建议安装pydub以在内存中转换（无需临时文件）: pip install pydub")
    except OSError as e:
        logger.error(f"操作系统错误: {e}", exc_info=True)
        raise Exception(f"文件操作失败: {str(e)}。建议安装pydub以在内存中转换（无需临时文件）: pip install pydub")
    except Exception as e:
        logger.error(f"音频转换异常: {e}", exc_info=True)
        error_msg = str(e)
        if "pydub" not in error_msg.lower():
            error_msg += "。建议安装pydub以在内存中转换: pip install pydub"
        raise Exception(f"音频格式转换失败: {error_msg}")
    finally:
        # 确保清理临时文件
        try:
            if temp_input and os.path.exists(temp_input):
                try:
                    os.remove(temp_input)
                    logger.debug(f"已清理临时输入文件: {temp_input}")
                except PermissionError:
                    logger.warning(f"无权限删除临时文件: {temp_input}")
                except Exception as e:
                    logger.warning(f"删除临时输入文件失败: {temp_input}, 错误: {e}")
            if temp_output and os.path.exists(temp_output):
                try:
                    os.remove(temp_output)
                    logger.debug(f"已清理临时输出文件: {temp_output}")
                except PermissionError:
                    logger.warning(f"无权限删除临时文件: {temp_output}")
                except Exception as e:
                    logger.warning(f"删除临时输出文件失败: {temp_output}, 错误: {e}")
        except Exception as e:
            logger.warning(f"清理临时文件时发生异常: {e}")

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/pyassistant')
def index():
    # 检查是否已登录
    if 'user_id' not in session:
        return render_template('index.html', chat_history=[], logged_in=False)

    # 获取当前对话的历史记录
    history = get_chat_history()
    return render_template('index.html', chat_history=history, logged_in=True)

@app.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400

        if len(username) < 3 or len(username) > 50:
            return jsonify({'error': '用户名长度必须在3-50个字符之间'}), 400

        if len(password) < 6:
            return jsonify({'error': '密码长度至少6个字符'}), 400

        # 密码加密（使用SHA256）
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # 检查用户名是否已存在
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    return jsonify({'error': '用户名已存在'}), 400

                # 创建新用户
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, password_hash)
                )
                conn.commit()
                user_id = cursor.lastrowid

                # 设置session
                session['user_id'] = user_id
                session['username'] = username
                session.modified = True

                return jsonify({
                    'success': True,
                    'message': '注册成功',
                    'user_id': user_id,
                    'username': username
                })
        except pymysql.IntegrityError:
            return jsonify({'error': '用户名已存在'}), 400
        except Exception as e:
            logger.error(f"注册失败: {e}")
            return jsonify({'error': f'注册失败: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"注册异常: {e}")
        return jsonify({'error': f'注册失败: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400

        # 密码加密
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username FROM users WHERE username = %s AND password = %s",
                    (username, password_hash)
                )
                user = cursor.fetchone()

                if not user:
                    return jsonify({'error': '用户名或密码错误'}), 401

                # 设置session
                session['user_id'] = user['id']
                session['username'] = user['username']
                session.pop('conversation_id', None)
                session.modified = True

                # 删除空白对话，确保每次登录后创建新的对话
                delete_empty_conversations(user['id'])

                return jsonify({
                    'success': True,
                    'message': '登录成功',
                    'user_id': user['id'],
                    'username': user['username']
                })
        except Exception as e:
            logger.error(f"登录失败: {e}")
            return jsonify({'error': f'登录失败: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"登录异常: {e}")
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

@app.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return jsonify({'success': True, 'message': '已登出'})

@app.route('/check_login', methods=['GET'])
def check_login():
    """检查登录状态"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session.get('user_id'),
            'username': session.get('username')
        })
    return jsonify({'logged_in': False})

@app.route('/search_handbook', methods=['POST'])
@require_login
def search_handbook():
    """搜索Python-100-Days手册"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()

        if not query:
            return jsonify({'error': '搜索查询不能为空'})

        # 检查智能体是否正常初始化
        if python_agent is None:
            return jsonify({'error': '智能体未正确初始化'})

        # 使用增强版手册搜索
        if hasattr(python_agent, 'enhanced_handbook_search'):
            result = python_agent.enhanced_handbook_search(query)
        elif hasattr(python_agent, 'handbook_search'):
            result = python_agent.handbook_search(query)
        else:
            return jsonify({'error': '手册搜索功能不可用'})

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({'error': f'搜索手册时出现错误: {str(e)}'})

@app.route('/enhanced_search', methods=['POST'])
@require_login
def enhanced_search():
    """增强搜索，包含图片"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': '搜索查询不能为空'})
        
        if enhanced_handbook is None:
            return jsonify({'error': 'Markdown文档处理器未初始化'})
        
        # 执行增强搜索
        results = enhanced_handbook.search_with_images(query)
        
        # 格式化结果
        formatted_results = []
        
        # 处理文本结果
        for result in results.get('text_results', []):
            citation = enhanced_handbook.generate_citation(result['content'])
            formatted_results.append({
                'type': 'text',
                'content': citation,
                'file': result.get('file', ''),
                'relevance': result.get('relevance', 'medium')
            })
        
        # 处理章节结果
        for section in results.get('sections', []):
            formatted_results.append({
                'type': 'section',
                'title': section['title'],
                'file': section['file'],
                'content': section['content'],
                'full_content': section.get('full_content', '')
            })
        
        # 处理图片结果
        image_results = []
        for img in results.get('image_results', []):
            image_info = {
                'caption': img['caption'],
                'file': img['file'],
                'type': img['type']
            }
            
            # 根据图片类型返回不同的数据
            if img['type'] == 'local' and img.get('base64'):
                image_info['base64'] = img['base64']
                image_info['url'] = img.get('url', '')
            elif img['type'] == 'web':
                image_info['url'] = img.get('url', '')
            
            image_results.append(image_info)
        
        return jsonify({
            'success': True,
            'text_results': formatted_results,
            'image_results': image_results,
            'total_found': len(formatted_results) + len(image_results)
        })
        
    except Exception as e:
        logger.error(f"增强搜索失败: {e}")
        return jsonify({'error': f'搜索失败: {str(e)}'})

@app.route('/upload_image', methods=['POST'])
@require_login
def upload_image():
    """上传图片"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': '没有上传图片'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': '没有选择文件'})
        
        result = save_uploaded_image(file)
        
        if result['success']:
            return jsonify({
                'success': True,
                'image_url': result.get('url', ''),
                'image_base64': result.get('base64', ''),
                'message': '图片上传成功'
            })
        else:
            return jsonify({'success': False, 'error': result.get('error', '上传失败')})
            
    except Exception as e:
        logger.error(f"上传图片失败: {e}")
        return jsonify({'success': False, 'error': f'上传图片失败: {str(e)}'})

@app.route('/ask_with_image', methods=['POST'])
@require_login
def ask_with_image():
    """带图片的提问"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        image_base64 = data.get('image', '').strip()
        
        if not question and not image_base64:
            return jsonify({'error': '问题和图片不能同时为空'})
        
        # 如果有图片，先搜索相关的手册内容
        related_content = ""
        if question and enhanced_handbook:
            results = enhanced_handbook.search_with_images(question)
            if results['text_results'] or results['sections']:
                # 构建相关内容的提示
                related_content = "\n\n根据《Python-100-Days》相关内容：\n"
                for result in results.get('text_results', [])[:3]:
                    related_content += f"- {result.get('content', '')[:200]}...\n"
        
        # 构建完整的提问
        full_question = question
        if related_content:
            full_question = question + related_content
        
        # 如果有上传的图片，添加到提示中
        if image_base64:
            full_question += "\n\n用户上传了相关图片，请结合图片内容进行回答。"
        
        # 调用智能体
        answer = python_agent.ask_question(full_question)
        
        # 如果有相关图片，添加到回答中
        if enhanced_handbook and question:
            images = enhanced_handbook.get_relevant_images(question, limit=2)
            if images:
                for img in images:
                    answer += f"\n\n[IMAGE:{img['caption']}]\n{img['base64']}\n[/IMAGE]"
        
        # 处理回答
        answer_html = process_ai_response(answer)
        
        # 添加到历史
        add_to_chat_history('user', question + (" (含图片)" if image_base64 else ""), "text")
        add_to_chat_history('assistant', answer_html, "html")
        
        return jsonify({
            'success': True,
            'answer': answer_html,
            'has_images': len(images) > 0 if 'images' in locals() else False,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
    except Exception as e:
        logger.error(f"带图片提问失败: {e}")
        return jsonify({'error': f'处理失败: {str(e)}'})

@app.route('/get_pdf_images', methods=['POST'])
@require_login
def get_pdf_images():
    """获取PDF中的相关图片"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({'error': '主题不能为空'})
        
        if enhanced_handbook is None:
            return jsonify({'error': 'Markdown文档处理器未初始化'})
        
        images = enhanced_handbook.get_relevant_images(topic)
        
        return jsonify({
            'success': True,
            'images': images,
            'count': len(images)
        })
        
    except Exception as e:
        logger.error(f"获取图片失败: {e}")
        return jsonify({'error': f'获取图片失败: {str(e)}'})

@app.route('/new_conversation', methods=['POST'])
@require_login
def new_conversation():
    """创建新对话"""
    try:
        # 清除当前对话ID
        if 'conversation_id' in session:
            del session['conversation_id']
        session.modified = True

        # 创建新对话
        conversation_id = get_current_conversation_id()

        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'message': '新对话已创建'
        })
    except Exception as e:
        logger.error(f"创建新对话失败: {e}")
        return jsonify({'error': f'创建新对话失败: {str(e)}'}), 500

@app.route('/get_conversations', methods=['GET'])
@require_login
def get_conversations():
    """获取用户的所有对话列表"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, c.title, c.created_at, c.updated_at,
                       (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as message_count
                FROM conversations c
                WHERE c.user_id = %s
                ORDER BY c.updated_at DESC
                LIMIT 50
            """, (session['user_id'],))
            conversations = cursor.fetchall()

            # 格式化日期
            for conv in conversations:
                conv['created_at'] = conv['created_at'].strftime('%Y-%m-%d %H:%M:%S') if conv['created_at'] else None
                conv['updated_at'] = conv['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if conv['updated_at'] else None

            return jsonify({
                'success': True,
                'conversations': conversations
            })
    except Exception as e:
        logger.error(f"获取对话列表失败: {e}")
        return jsonify({'error': f'获取对话列表失败: {str(e)}'}), 500

@app.route('/load_conversation/<int:conversation_id>', methods=['POST'])
@require_login
def load_conversation(conversation_id):
    """加载指定对话"""
    try:
        # 验证对话属于当前用户
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM conversations WHERE id = %s AND user_id = %s",
                (conversation_id, session['user_id'])
            )
            if not cursor.fetchone():
                return jsonify({'error': '对话不存在或无权限访问'}), 403

            # 设置当前对话ID
            session['conversation_id'] = conversation_id
            session.modified = True

            # 获取对话历史
            history = get_chat_history()

            return jsonify({
                'success': True,
                'conversation_id': conversation_id,
                'history': history
            })
    except Exception as e:
        logger.error(f"加载对话失败: {e}")
        return jsonify({'error': f'加载对话失败: {str(e)}'}), 500

@app.route('/delete_conversation/<int:conversation_id>', methods=['POST'])
@require_login
def delete_conversation(conversation_id):
    """删除指定对话"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 验证对话属于当前用户
            cursor.execute(
                "SELECT id FROM conversations WHERE id = %s AND user_id = %s",
                (conversation_id, session['user_id'])
            )
            if not cursor.fetchone():
                return jsonify({'error': '对话不存在或无权限访问'}), 403

            # 删除对话（级联删除消息）
            cursor.execute("DELETE FROM conversations WHERE id = %s", (conversation_id,))
            conn.commit()

            # 如果删除的是当前对话，清除session中的对话ID
            if session.get('conversation_id') == conversation_id:
                if 'conversation_id' in session:
                    del session['conversation_id']
                session.modified = True

            return jsonify({
                'success': True,
                'message': '对话已删除'
            })
    except Exception as e:
        logger.error(f"删除对话失败: {e}")
        return jsonify({'error': f'删除对话失败: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
@require_login
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()

        if not question:
            return jsonify({'error': '问题不能为空'})

        # 添加用户问题到历史
        add_to_chat_history('user', question)

        # 检查智能体是否正常初始化
        if python_agent is None:
            error_msg = "智能体未正确初始化，请刷新页面重试"
            add_to_chat_history('assistant', error_msg, "text")
            return jsonify({'error': error_msg})

        # 获取智能体回答
        try:
            answer = python_agent.ask_question(question)
        except Exception as e:
            error_msg = f"获取回答时出错: {str(e)}"
            add_to_chat_history('assistant', error_msg, "text")
            return jsonify({'error': error_msg})

        # 处理图像标记并转换为HTML
        try:
            answer_html = process_ai_response(answer)
        except Exception as e:
            print(f"响应处理错误: {e}")
            # 如果处理失败，回退到基本Markdown转换
            try:
                escaped_answer = html.escape(answer)
                answer_html = markdown.markdown(
                    escaped_answer,
                    extensions=['fenced_code', 'codehilite', 'tables']
                )
            except:
                answer_html = f"<pre>{html.escape(answer)}</pre>"

        # 添加智能体回答到历史
        add_to_chat_history('assistant', answer_html, "html")

        return jsonify({
            'success': True,
            'answer': answer_html,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })

    except Exception as e:
        error_msg = f'处理问题时出现错误: {str(e)}'
        add_to_chat_history('system', error_msg, "text")
        return jsonify({'error': error_msg})

@app.route('/ask_stream', methods=['POST'])
def ask_question_stream():
    """流式输出回答"""

    def generate():
        try:
            data = request.get_json()
            question = data.get('question', '').strip()

            if not question:
                yield f"data: {json.dumps({'error': '问题不能为空'})}\n\n"
                return

            # 检查智能体是否正常初始化
            if python_agent is None:
                error_msg = "智能体未正确初始化，请刷新页面重试"
                yield f"data: {json.dumps({'error': error_msg})}\n\n"
                return

            # 获取智能体回答
            try:
                answer = python_agent.ask_question(question)
            except Exception as e:
                error_msg = f"获取回答时出错: {str(e)}"
                yield f"data: {json.dumps({'error': error_msg})}\n\n"
                return

            # 处理图像标记
            processed_answer = process_ai_response(answer)

            # 模拟逐行输出
            lines = processed_answer.split('\n')
            full_answer = ""

            for i, line in enumerate(lines):
                if line.strip():  # 跳过空行
                    full_answer += line + '\n'

                    # 发送当前进度
                    chunk_data = json.dumps({
                        'chunk': full_answer,
                        'finished': False
                    })
                    yield f"data: {chunk_data}\n\n"

                    # 模拟打字延迟
                    time.sleep(0.05)

            # 发送完成信号
            finish_data = json.dumps({
                'chunk': '',
                'finished': True,
                'full_answer': full_answer,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            yield f"data: {finish_data}\n\n"

        except Exception as e:
            error_data = json.dumps({'error': f'处理问题时出现错误: {str(e)}'})
            yield f"data: {error_data}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/clear', methods=['POST'])
@require_login
def clear_chat():
    """清空当前对话"""
    conversation_id = get_current_conversation_id()
    if conversation_id:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM messages WHERE conversation_id = %s", (conversation_id,))
                conn.commit()
        except Exception as e:
            logger.error(f"清空对话失败: {e}")
            return jsonify({'error': f'清空对话失败: {str(e)}'}), 500

    return jsonify({'success': True})

@app.route('/syntax_check', methods=['POST'])
@require_login
def syntax_check():
    try:
        data = request.get_json()
        code = data.get('code', '').strip()

        if not code:
            return jsonify({'error': '代码不能为空'})

        # 检查智能体是否正常初始化且具有语法检查功能
        if python_agent is None:
            return jsonify({'error': '智能体未正确初始化'})

        if not hasattr(python_agent, 'syntax_checker'):
            return jsonify({'error': '语法检查功能不可用'})

        # 使用智能体的语法检查工具
        result = python_agent.syntax_checker(code)

        add_to_chat_history('system', f"语法检查结果:\n{result}", "text")

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({'error': f'语法检查时出现错误: {str(e)}'})

@app.route('/execute_code', methods=['POST'])
@require_login
def execute_code():
    """执行Python代码"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()

        if not code:
            return jsonify({'error': '代码不能为空'})

        # 检查智能体是否正常初始化且具有代码执行功能
        if python_agent is None:
            return jsonify({'error': '智能体未正确初始化'})

        if not hasattr(python_agent, 'code_executor'):
            return jsonify({'error': '代码执行功能不可用'})

        # 使用智能体的代码执行工具
        result = python_agent.code_executor(code)

        add_to_chat_history('system', f"代码执行结果:\n{result}", "text")

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({'error': f'代码执行时出现错误: {str(e)}'})

@app.route('/analyze_code', methods=['POST'])
@require_login
def analyze_code():
    """分析代码质量"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()

        if not code:
            return jsonify({'error': '代码不能为空'})

        # 检查智能体是否正常初始化且具有代码分析功能
        if python_agent is None:
            return jsonify({'error': '智能体未正确初始化'})

        if not hasattr(python_agent, 'code_analyzer'):
            return jsonify({'error': '代码分析功能不可用'})

        # 使用智能体的代码分析工具
        result = python_agent.code_analyzer(code)

        add_to_chat_history('system', f"代码分析结果:\n{result}", "text")

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({'error': f'代码分析时出现错误: {str(e)}'})

@app.route('/get_markdown_files', methods=['GET'])
@require_login
def get_markdown_files():
    """获取所有Markdown文件列表"""
    try:
        if enhanced_handbook is None:
            return jsonify({'error': '文档处理器未初始化'})
        
        # 获取所有Markdown文件的相对路径和基本信息
        files = []
        for md_file in enhanced_handbook.md_files:
            rel_path = str(md_file.relative_to(enhanced_handbook.base_path))
            file_key = rel_path.replace('\\', '/')
            
            # 获取文件大小和修改时间
            stat = md_file.stat()
            files.append({
                'path': file_key,
                'name': md_file.name,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'has_images': bool([k for k, v in enhanced_handbook.images_cache.items() if v.get('file') == file_key])
            })
        
        # 按路径排序
        files.sort(key=lambda x: x['path'])
        
        return jsonify({
            'success': True,
            'files': files,
            'total_files': len(files),
            'total_images': len(enhanced_handbook.images_cache)
        })
        
    except Exception as e:
        logger.error(f"获取Markdown文件列表失败: {e}")
        return jsonify({'error': f'获取文件列表失败: {str(e)}'})

@app.route('/get_markdown_content/<path:file_path>', methods=['GET'])
@require_login
def get_markdown_content(file_path):
    """获取指定Markdown文件的内容"""
    try:
        if enhanced_handbook is None:
            return jsonify({'error': '文档处理器未初始化'})
        
        # 获取文件内容
        content = enhanced_handbook.get_file_content(file_path)
        if content is None:
            return jsonify({'error': '文件不存在或无法读取'})
        
        # 获取文件相关的图片
        related_images = []
        for key, img in enhanced_handbook.images_cache.items():
            if img.get('file') == file_path.replace('\\', '/'):
                related_images.append(img)
        
        return jsonify({
            'success': True,
            'content': content,
            'path': file_path,
            'images': related_images,
            'image_count': len(related_images)
        })
        
    except Exception as e:
        logger.error(f"获取Markdown内容失败: {e}")
        return jsonify({'error': f'获取内容失败: {str(e)}'})

@app.route('/search_markdown', methods=['POST'])
@require_login
def search_markdown():
    """搜索Markdown内容"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': '搜索关键词不能为空'})
        
        if enhanced_handbook is None:
            return jsonify({'error': '文档处理器未初始化'})
        
        results = []
        
        # 在所有文件中搜索
        for file_key, content in enhanced_handbook.text_cache.items():
            # 不区分大小写搜索
            if query.lower() in content.lower():
                # 提取匹配的上下文
                pattern = re.compile(re.escape(query), re.IGNORECASE)
                matches = list(pattern.finditer(content))
                
                for match in matches[:3]:  # 每个文件最多取3个匹配
                    start = max(0, match.start() - 100)
                    end = min(len(content), match.end() + 100)
                    context = content[start:end]
                    
                    # 高亮显示搜索词
                    highlighted = re.sub(
                        f'({re.escape(query)})',
                        '<mark>\\1</mark>',
                        context,
                        flags=re.IGNORECASE
                    )
                    
                    results.append({
                        'file': file_key,
                        'context': highlighted,
                        'position': match.start(),
                        'score': len(query) / len(context)  # 简单评分
                    })
        
        # 按评分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'success': True,
            'results': results[:50],  # 最多返回50个结果
            'total_matches': len(results)
        })
        
    except Exception as e:
        logger.error(f"搜索Markdown失败: {e}")
        return jsonify({'error': f'搜索失败: {str(e)}'})

@app.route('/upload_markdown_image', methods=['POST'])
@require_login
def upload_markdown_image():
    """上传文档中的图片"""
    try:
        data = request.get_json()
        image_path = data.get('path', '').strip()
        
        if not image_path:
            return jsonify({'error': '图片路径不能为空'})
        
        if enhanced_handbook is None:
            return jsonify({'error': '文档处理器未初始化'})
        
        # 查找图片
        for key, img in enhanced_handbook.images_cache.items():
            if img.get('path') == image_path:
                return jsonify({
                    'success': True,
                    'image': img
                })
        
        return jsonify({'error': '图片未找到'})
        
    except Exception as e:
        logger.error(f"上传文档图片失败: {e}")
        return jsonify({'error': f'获取图片失败: {str(e)}'})

@app.route('/web_crawler', methods=['POST'])
@require_login
def web_crawler():
    """网页爬虫功能，使用用户提供的Firecrawl API代码模板"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()

        if not url:
            return jsonify({'error': '网址不能为空'})

        # 验证URL格式
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return jsonify({'error': '请输入有效的网址格式'})
        except:
            return jsonify({'error': '请输入有效的网址格式'})

        # 使用用户提供的代码模板，替换URL部分
        crawler_code = f'''
import requests 
import json 

url = "https://api.firecrawl.dev/v2/scrape" 

payload = {{ 
  "url": "{url}", 
  "onlyMainContent": False, 
  "maxAge": 172800000, 
  "parsers": ["pdf"], 
  "formats": ["markdown"] 
}} 

headers = {{ 
    "Authorization": "Bearer fc-6cb8afb6f01f4c22a345715bf37787c9", 
    "Content-Type": "application/json" 
}} 

response = requests.post(url, json=payload, headers=headers) 
data = response.json() 

if data["success"]: 
    # 直接打印 markdown 内容，\\n 会正常显示为换行 
    print("=== 网页内容 ===") 
    print(data["data"]["markdown"]) 
    print("================")
else:
    print(f"爬取失败: {{data.get('error', '未知错误')}}")
'''

        # 使用智能体的代码执行功能来运行爬虫代码
        if python_agent is None:
            return jsonify({'error': '智能体未正确初始化'})

        if not hasattr(python_agent, 'code_executor'):
            return jsonify({'error': '代码执行功能不可用'})

        # 执行爬虫代码
        result = python_agent.code_executor(crawler_code)

        # 添加到对话历史
        add_to_chat_history('system', f"网页爬取结果（网址：{url}）:\n{result}", "text")

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({'error': f'网页爬取时出现错误: {str(e)}'})

@app.route('/voice_recognition', methods=['POST'])
@require_login
def voice_recognition():
    """处理语音识别请求 - 真实可用的版本"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': '没有上传音频文件'})

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': '没有选择文件'})

        # 检查文件类型
        if not audio_file.filename.lower().endswith(('.wav', '.webm', '.pcm')):
            return jsonify({'error': '只支持WAV、WEBM或PCM格式的音频文件'})

        # 读取音频数据
        audio_data = audio_file.read()

        if len(audio_data) == 0:
            return jsonify({'error': '音频文件为空'})

        logger.info(f"收到音频文件，大小: {len(audio_data)} 字节")

        # 创建语音识别实例
        voice_recog = XunfeiVoiceRecognition()

        # 如果是webm格式，转换为PCM
        if audio_file.filename.lower().endswith('.webm'):
            logger.info("检测到WEBM格式，转换为PCM...")
            try:
                pcm_data = convert_audio_to_pcm(audio_data)
                if pcm_data is None:
                    return jsonify({'error': '音频格式转换失败: 转换后数据为空'})
                if len(pcm_data) == 0:
                    return jsonify({'error': '音频格式转换失败: 转换后数据长度为0'})
                # 验证PCM数据大小（应该是16位，即2字节每样本）
                if len(pcm_data) % 2 != 0:
                    logger.warning(f"PCM数据大小不是2的倍数: {len(pcm_data)}，可能有问题")
                audio_data = pcm_data
                logger.info(f"音频转换完成，PCM数据大小: {len(audio_data)} 字节")
            except Exception as e:
                error_detail = str(e)
                logger.error(f"音频格式转换异常: {error_detail}", exc_info=True)
                return jsonify({'error': f'音频格式转换失败: {error_detail}'})

        # 验证音频数据
        if len(audio_data) < 1000:  # 至少需要一些数据
            logger.warning(f"音频数据太小: {len(audio_data)} 字节，可能无法识别")

        # 进行语音识别
        logger.info(f"开始语音识别，音频数据大小: {len(audio_data)} 字节")
        result = voice_recog.recognize_audio(audio_data)

        if result['success']:
            recognition_text = result['text']
            if not recognition_text:
                recognition_text = "未能识别到有效语音内容"

            logger.info(f"语音识别成功: {recognition_text}")

            return jsonify({
                'success': True,
                'text': recognition_text,
                'message': '语音识别完成'
            })
        else:
            error_msg = result.get('error', '识别失败')
            logger.error(f"语音识别失败: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg
            })

    except Exception as e:
        logger.error(f"语音识别异常: {e}")
        return jsonify({'error': f'语音识别失败: {str(e)}'})

@app.route('/voice_config')
def get_voice_config():
    """获取语音识别配置"""
    voice_recog = XunfeiVoiceRecognition()

    return jsonify({
        'app_id': voice_recog.app_id,
        'api_key': voice_recog.api_key,
        'api_secret': voice_recog.api_secret,
        'ws_url': voice_recog.ws_url
    })
    
@app.route('/health')
def health_check():
    """健康检查端点"""
    status = "healthy" if python_agent is not None else "degraded"
    agent_type = type(python_agent).__name__ if python_agent else "None"
    
    pdf_status = "loaded" if enhanced_handbook is not None else "not_loaded"
    pdf_images = len(enhanced_handbook.images_cache) if enhanced_handbook else 0

    return jsonify({
        'status': status,
        'agent_type': agent_type,
        'pdf_status': pdf_status,
        'pdf_images': pdf_images,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/reinitialize', methods=['POST'])
def reinitialize_agent():
    """重新初始化智能体"""
    global python_agent
    try:
        success = initialize_agent()
        return jsonify({
            'success': success,
            'message': '智能体重新初始化成功' if success else '智能体重新初始化失败，使用基础模式'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'重新初始化失败: {str(e)}'
        })

@app.route('/robots.txt')
def robots_txt():
    """提供同目录下的robots.txt文件"""
    try:
        # 读取当前目录下的robots.txt文件
        with open('robots.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return Response(content, mimetype='text/plain')
    except FileNotFoundError:
        logger.warning("robots.txt文件未找到")
        return Response("File not found", status=404, mimetype='text/plain')
    except Exception as e:
        logger.error(f"读取robots.txt失败: {e}")
        return Response("Server error", status=500, mimetype='text/plain')

@app.route('/res/<path:filename>')
def serve_res_files(filename):
    """将/res/路径映射到/static/res/文件夹"""
    try:
        # 直接发送static/res文件夹中的文件
        return send_from_directory('static/res', filename)
    except Exception as e:
        logger.error(f"访问文件失败: {filename}, 错误: {e}")
        return jsonify({'error': '文件不存在'}), 404
        
if __name__ == '__main__':
    # 确保临时目录存在
    os.makedirs('static/temp', exist_ok=True)

    # 检查数据库连接
    try:
        test_conn = get_db_connection()
        test_conn.close()
        print("✅ 数据库连接测试成功")
    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
        print("   请确保MySQL服务已启动，并且数据库pyassistant已创建")
        print("   创建数据库命令: CREATE DATABASE pyassistant CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

    # 检查系统临时目录权限
    temp_dir = tempfile.gettempdir()
    if os.access(temp_dir, os.W_OK):
        print(f"✅ 临时目录可写: {temp_dir}")
    else:
        print(f"⚠️  警告: 临时目录无写权限: {temp_dir}")
        print("   这可能导致语音识别功能失败")
        print("   解决方法: 确保应用有权限访问临时目录，或安装pydub使用内存转换")

    # 检查依赖
    if WEBSOCKET_AVAILABLE:
        print("✅ websocket-client 已安装")
    else:
        print("❌ 请安装依赖: pip install websocket-client")
    
    # 检查PyMuPDF（虽然不需要了，但保持代码完整性）
    try:
        import fitz
        print("✅ PyMuPDF 已安装")
    except ImportError:
        print("❌ PyMuPDF 未安装，请运行: pip install PyMuPDF")
        print("   这是PDF图片提取功能所必需的")

    # 检查音频处理依赖
    has_pydub = False
    has_ffmpeg = False

    # 检查pydub（优先使用，完全在内存中转换，无需临时文件）
    try:
        import pydub
        has_pydub = True
        print("✅ pydub 已安装（推荐：在内存中转换音频，无需临时文件，避免权限问题）")
    except ImportError:
        print("⚠️  pydub 未安装，建议安装: pip install pydub")
        print("   pydub可以在内存中转换音频，避免文件权限问题")

    # 检查ffmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            has_ffmpeg = True
            print("✅ ffmpeg 已安装")
        else:
            print("⚠️  ffmpeg 未正确安装，WEBM格式转换可能失败")
    except FileNotFoundError:
        print("⚠️  ffmpeg 未安装，WEBM格式转换可能失败")
        print("   安装方法: https://ffmpeg.org/download.html")
    except:
        print("⚠️  ffmpeg 检查失败，WEBM格式转换可能失败")

    if not has_pydub and not has_ffmpeg:
        print("❌ 警告: 未检测到音频处理工具，语音输入功能可能无法使用")
        print("   建议安装: pip install pydub")

    print("\n=== 系统状态 ===")
    print(f"Python编程助手: {'✅ 已初始化' if python_agent else '❌ 未初始化'}")
    print(f"Markdown文档处理器: {'✅ 已初始化' if enhanced_handbook else '❌ 未初始化'}")
    if enhanced_handbook:
        print(f"Markdown文件数量: {len(enhanced_handbook.md_files)}")
        print(f"索引图片数量: {len(enhanced_handbook.images_cache)}")
    
    app.run(host='0.0.0.0', port=5007, debug=True)
