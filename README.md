# PyAssistant - Python编程智能助手

## 项目概述

### 项目简介
PyAssistant 是一个基于 Web 的 Python 编程智能助手，集成了 AI 对话、代码工具、语音识别和网页爬虫等功能，为 Python 开发者提供全方位的编程辅助。

### 核心价值
- 🤖 智能编程助手 - AI 驱动的代码分析和建议
- 🛠️ 一体化工具 - 代码执行、语法检查、文档查询
- 🎙️ 多模态交互 - 支持文本和语音输入
- 📱 跨平台访问 - 响应式设计，支持多设备
- 💾 数据持久化 - 用户系统和对话历史

### 适用场景
- Python 学习和教学
- 代码调试和优化
- 技术文档查询
- 网页数据采集
- 编程问题解答

## 项目结构

```
PyAssistant/
├── app.py                 # Flask应用主文件
├── python_agent.py        # AI智能代理
├── requirements.txt       # Python依赖列表
├── .env.example          # 环境变量示例文件
├── README.md             # 项目说明文档（本文件）
├── Pyassistant_help.html # 详细帮助文档
├── Pyassistant_source_code.html # 源代码查看器
├── templates/
│   └── index.html        # 主页面HTML模板
└── static/
    ├── style.css         # 前端样式文件
    ├── script.js         # 前端逻辑脚本
    ├── pyassistant.png   # 应用图标
    └── temp/             # 临时文件目录
```

## 功能特性

### 对话助手
- **AI 对话**: 智能问答系统，支持上下文理解
- **历史管理**: 对话记录保存，支持标题自动生成
- **消息格式**: 富文本显示，支持代码高亮、表格
- **实时交互**: 流式输出，打字机效果

### 代码工具集
- **语法检查**: 检查 Python 代码语法错误，提供详细错误报告和改进建议
- **代码执行**: 安全执行 Python 代码片段，实时返回执行结果或错误信息
- **代码分析**: 分析代码质量，提供结构概览和优化建议
- **文档查询**: 快速查询 Python 官方文档，获取详细函数和模块说明

### Python 爬虫
- **网页抓取**: 获取网页内容（使用 Firecrawl API）
- **格式转换**: 自动转换为 Markdown 格式
- **结果预览**: 内容预览，代码高亮
- **内容导出**: 支持复制/发送到对话，多种格式

### 语音识别
- **语音输入**: 录音转文字（使用讯飞语音识别）
- **实时反馈**: 录音状态显示，可视化指示
- **格式支持**: 支持 WebM, WAV, PCM 格式
- **自动转换**: 音频格式处理（使用 PyDub/FFmpeg）

### 用户系统
- **用户注册**: 新用户注册，用户名密码验证
- **用户登录**: 身份验证，Session 管理
- **对话隔离**: 用户数据隔离，多用户支持
- **安全退出**: 会话清理，自动跳转

### UI/UX 特性
- **主题切换**: 深色/浅色主题，实时切换，保护视力
- **响应式设计**: 移动端适配，多屏幕支持，优化触控体验
- **代码高亮**: 语法高亮显示（使用 Highlight.js），提升代码可读性
- **动画效果**: 平滑过渡，CSS 动画，提升用户体验

## 技术架构

### 前端架构
```
Frontend (Browser)
├── HTML5
│   ├── 语义化结构
│   ├── 模态对话框
│   └── 表单验证
├── CSS3
│   ├── CSS变量（主题）
│   ├── Flexbox/Grid布局
│   ├── 媒体查询（响应式）
│   └── 动画过渡
└── JavaScript
    ├── 原生JS + Fetch API
    ├── 事件管理
    ├── 状态管理
    └── 语音录制
```

### 后端架构
```
Backend (Flask)
├── Web框架
│   ├── Flask核心
│   ├── 路由管理
│   ├── 会话管理
│   └── 模板渲染
├── 数据层
│   ├── MySQL数据库
│   ├── PyMySQL驱动
│   └── 连接池管理
├── AI服务层
│   ├── LangChain集成
│   ├── DeepSeek/OpenAI
│   └── 工具调用系统
└── 工具服务
    ├── 语音识别
    ├── 代码执行
    ├── 网页爬虫
    └── 文件处理
```

### 系统组件图
```
用户界面 → Flask路由 → 业务逻辑 → 数据存储
    ↓          ↓           ↓         ↓
前端交互   URL路由    AI代理工具   MySQL数据库
    ↓          ↓           ↓         ↓
语音输入  会话管理   代码执行器   用户表
    ↓          ↓           ↓         ↓
主题切换  认证中间件  语法检查器   对话表
    ↓          ↓           ↓         ↓
实时通信  错误处理   文档查询器   消息表
```

## 安装部署

### 环境要求

**系统要求:**
- 操作系统: Windows 10+/macOS 10.14+/Linux Ubuntu 18.04+
- Python: 3.8 或更高版本
- 内存: 最低 2GB，推荐 4GB+
- 磁盘空间: 至少 500MB 可用空间

**Python 依赖:**
```bash
# 核心框架
Flask==2.3.3
langchain==0.0.346
langchain-openai==0.0.2

# 数据库
pymysql==1.1.0

# 语音处理
websocket-client==1.6.3
pydub==0.25.1

# 文档处理
PyPDF2==3.0.1

# 环境管理
python-dotenv==1.0.0

# 其他工具
requests==2.31.0
```

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd PyAssistant
```

2. **创建虚拟环境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **数据库设置**
```sql
-- 创建数据库
CREATE DATABASE pyassistant CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（可选）
CREATE USER 'pyassistant'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON pyassistant.* TO 'pyassistant'@'localhost';
FLUSH PRIVILEGES;
```

5. **环境配置**
创建 `.env` 文件：
```env
# 数据库配置
DB_HOST=localhost
DB_USER=pyassistant
DB_PASSWORD=your_password
DB_NAME=pyassistant

# AI API 配置
DEEPSEEK_API_KEY=your_deepseek_key
OPENAI_API_KEY=your_openai_key

# 语音识别配置
XF_APP_ID=your_xf_app_id
XF_API_KEY=your_xf_api_key
XF_API_SECRET=your_xf_api_secret

# 爬虫配置
FIRECRAWL_API_KEY=your_firecrawl_key
```

6. **初始化数据库**
```bash
python app.py
# 首次运行会自动创建数据表
```

7. **启动应用**
```bash
python app.py
```
访问: http://localhost:5007/pyassistant

## 配置说明

### 数据库配置
```python
DB_CONFIG = {
    'host': 'localhost',      # 数据库主机
    'user': 'pyassistant',    # 数据库用户
    'password': 'password',   # 数据库密码
    'database': 'pyassistant', # 数据库名
    'charset': 'utf8mb4',     # 字符编码
    'cursorclass': pymysql.cursors.DictCursor
}
```

### AI 模型配置
```python
# DeepSeek 配置
self.llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.1
)

# OpenAI 备用配置
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)
```

### 语音识别配置
```python
class XunfeiVoiceRecognition:
    def __init__(self):
        self.app_id = os.getenv('XF_APP_ID')
        self.api_key = os.getenv('XF_API_KEY') 
        self.api_secret = os.getenv('XF_API_SECRET')
        self.ws_url = "wss://iat-api.xfyun.cn/v2/iat"
```

### 安全配置
```python
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 生产环境请更改

# 代码执行安全限制
dangerous_patterns = [
    r'__import__\s*\(', r'eval\s*\(', r'exec\s*\(',
    r'open\s*\(', r'os\.', r'subprocess\.'
]
```

## 使用指南

### 首次使用

1. **用户注册**
   - 访问应用首页
   - 点击"登录"按钮
   - 切换到"注册"标签
   - 输入用户名和密码（最少6位）
   - 完成注册并自动登录

2. **开始对话**
   - 在输入框中输入 Python 相关问题
   - 点击发送或按 Ctrl+Enter
   - 查看 AI 回复，支持代码高亮
   - 使用复制按钮保存答案

### 核心功能使用

**代码语法检查示例：**
```python
# 输入示例：
def calculate_sum(a, b)
    return a + b

# 输出结果：
✅ 语法检查通过：未发现语法错误

结构概览:
• 总行数: 2
• 函数数量: 1
• 类数量: 0
• 引入模块: （无）

风格建议（节选）:
• 第1行缺少冒号
• 建议添加函数文档字符串
```

**代码执行示例：**
```python
# 输入示例：
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"平方数: {squares}")

# 输出结果：
✅ 执行成功:
平方数: [1, 4, 9, 16, 25]
```

### 语音输入
1. 点击麦克风按钮开始录音
2. 说话内容实时转文字
3. 点击停止结束录音
4. 识别结果自动填入输入框

### 网页爬虫
1. 切换到"Python爬虫"标签
2. 输入目标网址（如: https://example.com）
3. 点击"开始爬取"
4. 查看 Markdown 格式结果
5. 复制内容或发送到对话

### 快捷键
- **Ctrl + Enter**: 发送消息
- **Ctrl + N**: 新建对话
- **Ctrl + T**: 切换主题
- **Ctrl + M**: 语音输入
- **Ctrl + /**: 帮助提示

### 移动端使用
- 底部导航: 对话、工具、爬虫快速切换
- 手势操作: 左滑显示侧边栏
- 语音优化: 移动端专用语音按钮
- 触摸友好: 加大点击区域

## API接口

### 认证相关

**用户注册**
```http
POST /register
Content-Type: application/json

{
  "username": "newuser",
  "password": "password123"
}

响应:
{
  "success": true,
  "user_id": 1,
  "username": "newuser"
}
```

**用户登录**
```http
POST /login
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}

响应:
{
  "success": true,
  "user_id": 1,
  "username": "user"
}
```

### 对话相关

**发送问题**
```http
POST /ask
Content-Type: application/json
Headers: {Cookie: session}

{
  "question": "Python装饰器是什么？"
}

响应:
{
  "success": true,
  "answer": "装饰器是Python中...",
  "timestamp": "14:30:25"
}
```

**获取对话历史**
```http
GET /get_conversations
Headers: {Cookie: session}

响应:
{
  "success": true,
  "conversations": [
    {
      "id": 1,
      "title": "Python装饰器问题",
      "message_count": 5,
      "updated_at": "2024-01-15 14:30:25"
    }
  ]
}
```

### 工具相关

**代码执行**
```http
POST /execute_code
Content-Type: application/json

{
  "code": "print('Hello, World!')"
}

响应:
{
  "success": true,
  "result": "Hello, World!"
}
```

**语法检查**
```http
POST /syntax_check
Content-Type: application/json

{
  "code": "def hello()\n    print('hello')"
}

响应:
{
  "success": true,
  "result": "❌ 语法错误: 第1行缺少冒号"
}
```

**语音识别**
```http
POST /voice_recognition
Content-Type: multipart/form-data

FormData:
  audio: [音频文件]

响应:
{
  "success": true,
  "text": "识别到的语音内容"
}
```

### 错误码说明
| 状态码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | 正常处理 |
| 400 | 请求错误 | 检查参数格式 |
| 401 | 未授权 | 重新登录 |
| 500 | 服务器错误 | 查看服务日志 |

## 数据库设计

### 数据表结构

**users 用户表**
| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | INT | 主键 | AUTO_INCREMENT |
| username | VARCHAR(50) | 用户名 | UNIQUE, NOT NULL |
| password | VARCHAR(255) | 密码哈希 | NOT NULL |
| created_at | TIMESTAMP | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | 更新时间 | ON UPDATE CURRENT_TIMESTAMP |

**conversations 对话表**
| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | INT | 主键 | AUTO_INCREMENT |
| user_id | INT | 用户ID | FOREIGN KEY |
| title | VARCHAR(255) | 对话标题 | DEFAULT '新对话' |
| created_at | TIMESTAMP | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | 更新时间 | ON UPDATE CURRENT_TIMESTAMP |

**messages 消息表**
| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| id | INT | 主键 | AUTO_INCREMENT |
| conversation_id | INT | 对话ID | FOREIGN KEY |
| role | ENUM | 消息角色 | ('user','assistant','system') |
| content | TEXT | 消息内容 | NOT NULL |
| message_type | VARCHAR(20) | 消息类型 | DEFAULT 'text' |
| timestamp | TIMESTAMP | 时间戳 | DEFAULT CURRENT_TIMESTAMP |

### 索引设计
```sql
-- 用户表索引
CREATE INDEX idx_username ON users(username);

-- 对话表索引  
CREATE INDEX idx_user_id ON conversations(user_id);
CREATE INDEX idx_updated_at ON conversations(updated_at);

-- 消息表索引
CREATE INDEX idx_conversation_id ON messages(conversation_id);
CREATE INDEX idx_timestamp ON messages(timestamp);
```

### 关系图
```
users
  │
  ├── conversations (1:N)
  │     │
  │     └── messages (1:N)
  │
  └── sessions (1:1)
```

## 开发指南

### 项目结构
```
PyAssistant/
├── app.py                 # Flask应用主文件
├── python_agent.py        # AI智能代理
├── requirements.txt       # 依赖列表
├── .env.example          # 环境变量示例
├── templates/
│   └── index.html        # 主页面模板
└── static/
    ├── style.css         # 样式文件
    ├── script.js         # 前端逻辑
    ├── pyassistant.png   # 应用图标
    └── temp/             # 临时文件目录
```

### 代码规范

**Python 代码规范**
```python
def function_name(parameter: type) -> return_type:
    """函数文档字符串
    
    Args:
        parameter: 参数说明
        
    Returns:
        返回值说明
        
    Raises:
        ExceptionType: 异常说明
    """
    # 代码逻辑
    pass
```

**JavaScript 代码规范**
```javascript
/**
 * 函数描述
 * @param {string} parameter - 参数说明
 * @returns {string} 返回值说明
 */
function functionName(parameter) {
    // 代码逻辑
    return result;
}
```

### 添加新功能

**1. 添加新的工具**
```python
# 在 python_agent.py 中添加
def new_tool(self, input_data: str) -> str:
    """新工具的功能描述"""
    try:
        # 工具逻辑
        result = process_input(input_data)
        return result
    except Exception as e:
        return f"工具执行错误: {str(e)}"

# 注册到工具集
self.tools["new_tool"] = self.new_tool
```

**2. 添加前端页面**
```html
<!-- 在 index.html 中添加 -->
<div class="new-container" id="newTab" style="display: none;">
    <div class="new-header">
        <h2>新功能页面</h2>
    </div>
    <!-- 页面内容 -->
</div>
```

```javascript
// 在 script.js 中添加事件处理
const newToolBtn = document.getElementById('newToolBtn');
newToolBtn.addEventListener('click', function() {
    // 功能逻辑
});
```

**3. 添加后端路由**
```python
@app.route('/new_tool', methods=['POST'])
@require_login
def new_tool():
    """新工具的路由处理"""
    try:
        data = request.get_json()
        # 处理逻辑
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 测试指南

**单元测试**
```python
import unittest
from app import app, get_db_connection

class TestPyAssistant(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_syntax_check(self):
        response = self.app.post('/syntax_check', 
                               json={'code': 'print("hello")'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_json())
```

**集成测试**
```bash
# 启动测试服务器
python app.py

# 测试各项功能
curl -X POST http://localhost:5007/syntax_check \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"test\")"}'
```

## 故障排除

### 常见问题

**1. 应用启动失败**
```
问题: Address already in use
解决方案:
# 查找占用端口的进程
lsof -i :5007
# 终止进程
kill -9 <PID>
# 或更换端口
python app.py --port 5008
```

**2. 数据库连接错误**
```
问题: pymysql.err.OperationalError
解决方案:
# 检查MySQL服务
sudo systemctl status mysql
# 启动服务
sudo systemctl start mysql
# 检查用户权限
mysql -u root -p -e "SHOW GRANTS FOR 'pyassistant'@'localhost';"
```

**3. 语音识别失败**
```
问题: 音频转换错误
解决方案:
# 安装 FFmpeg
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg
# macOS
brew install ffmpeg
# 或安装 pydub（推荐）
pip install pydub
```

**4. AI 服务不可用**
```
问题: API 密钥错误
解决方案:
# 检查环境变量
echo $DEEPSEEK_API_KEY
# 重新配置 .env 文件
cp .env.example .env
# 编辑 .env 文件填入正确的 API 密钥
```

**5. 内存不足**
```python
# 解决方案：增加内存限制
@app.route('/process_file', methods=['POST'])
def process_file():
    # 设置文件大小限制 (50MB)
    if request.content_length > 50 * 1024 * 1024:
        return jsonify({'error': '文件过大'}), 400
```

### 日志分析

**查看应用日志**
```python
# 在 app.py 中配置日志
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pyassistant.log'),
        logging.StreamHandler()
    ]
)
```

**常见错误日志**
```plaintext
# 数据库连接错误
ERROR: pymysql.err.OperationalError: (1045, "Access denied for user...")

# API 密钥错误
ERROR: openai.AuthenticationError: Incorrect API key provided

# 内存不足
ERROR: MemoryError: Unable to allocate 256. MiB for an array...
```

### 性能优化

**数据库优化**
```sql
-- 添加索引
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at);

-- 定期清理
DELETE FROM messages WHERE timestamp < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

**缓存优化**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_documentation(topic: str) -> str:
    """缓存文档查询结果"""
    return self.python_documentation(topic)
```

## 技术支持

- 查看日志文件
- 检查系统状态
- 重新初始化AI
- GitHub Issues
- 文档更新
- 版本更新

**版本信息:**
- PyAssistant: v1.0.0
- Flask版本: 2.3.3
- Python版本: 3.8+
- 最后更新: 2025年12月
