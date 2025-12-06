# PyAssistant - Python编程智能助手 (v1.0.2)

## 📋 项目概述

PyAssistant是一个功能强大的基于Web的Python编程智能助手，集成了**AI对话**、**代码工具集**、**语音识别**、**Python爬虫**和**Markdown文档检索**等功能，为Python开发者提供全方位的编程辅助解决方案。

### 🎯 核心价值
- 🤖 **智能AI助手** - 基于DeepSeek/OpenAI的智能问答系统
- 🔧 **一体化工具箱** - 代码执行、语法检查、文档查询、代码分析
- 🎙️ **多模态交互** - 文本+语音+图片多输入模式
- 📚 **文档检索系统** - 强大的Markdown文档检索（v1.0.2升级）
- 🕷️ **网页爬虫** - 一键抓取网页并转为Markdown
- 📱 **响应式设计** - 完美适配桌面和移动设备
- 🔐 **用户系统** - 完整的注册登录和对话历史管理

### 🎯 核心更新 (v1.0.2) - 2025年12月重大更新
#### 文档检索全面升级
- **📄 PDF → Markdown**：文档检索从PDF全面升级为Markdown格式
- **⚡ 性能提升**：检索速度提升5-10倍，更精确、更快速
- **📁 完整项目支持**：支持整个Python-100-days-master项目的文档检索
- **🖼️ 智能图片提取**：自动提取Markdown文档中的本地和网络图片并转换为base64
- **🎯 精确搜索**：支持章节、关键词、全文等多种搜索方式
- **📊 结构化展示**：文档内容按章节结构化显示

#### 架构优化
- **📄 文档侧边栏**：将文档查询功能移至侧边栏，界面更清晰
- **⚡ 全文索引**：构建全文搜索索引，支持实时搜索
- **📋 文件管理**：新增Markdown文件列表和内容查看功能
- **🔗 图片关联**：图片与源文件智能关联，支持图片预览
- **🔙 向后兼容**：保持原有PDF接口兼容性

## 🚀 快速开始

### 环境要求
- **Python**: 3.8+
- **MySQL**: 5.7+
- **内存**: 2GB+ (推荐4GB)
- **操作系统**: Windows 10+/macOS 10.14+/Linux Ubuntu 18.04+

### 新增依赖 (v1.0.2)
```bash
# Markdown文档处理相关（v1.0.2新增）
pathlib  # Python标准库，无需单独安装
# PyMuPDF (fitz)  # 保持向后兼容
```

### 安装步骤

1. **克隆项目并准备文档** (v1.0.2更新)
```bash
git clone <repository-url>
cd PyAssistant

# 下载Python-100-Days项目（或放入static目录）
# 确保项目结构如下：
# static/
# ├── Python-100-Days-master/
# │   ├── Day01-15/
# │   ├── Day16-30/
# │   ├── Day31-45/
# │   └── README.md
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

-- 创建用户
CREATE USER 'pyassistant'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON pyassistant.* TO 'pyassistant'@'localhost';
FLUSH PRIVILEGES;
```

5. **配置环境变量**
创建 `.env` 文件：
```env
# 数据库配置
DB_HOST=localhost
DB_USER=pyassistant
DB_PASSWORD=your_password
DB_NAME=pyassistant

# AI API配置 (DeepSeek优先)
DEEPSEEK_API_KEY=your_deepseek_key_here
# 备用 OpenAI
OPENAI_API_KEY=your_openai_key_here

# 语音识别配置 (讯飞)
XF_APP_ID=your_xf_app_id
XF_API_KEY=your_xf_api_key
XF_API_SECRET=your_xf_api_secret

# 应用密钥
APP_SECRET_KEY=your_app_secret_key
```

6. **初始化数据库**
```bash
python app.py
# 首次运行会自动创建所有表结构
```

7. **启动应用**
```bash
python app.py
```
访问地址：http://localhost:5007/pyassistant

## 🎨 主要功能

### 📚 Markdown文档检索 (v1.0.2全新功能)
- **全文检索**：搜索整个Python-100-Days项目的所有Markdown文件
- **章节索引**：自动识别和索引所有章节结构
- **图片提取**：智能提取Markdown文档中的本地和网络图片
- **关联搜索**：文本内容和图片的智能关联
- **预览功能**：支持图片预览和文档内容查看
- **模糊匹配**：支持模糊搜索和精确短语搜索
- **引用生成**：自动生成标准引用格式

### 💬 对话助手
- **智能问答**：基于AI的Python编程问题解答
- **上下文理解**：保持对话连续性
- **代码高亮**：自动识别并高亮Python代码
- **Markdown渲染**：支持表格、列表、图片等格式
- **复制功能**：一键复制代码和回答内容
- **历史管理**：自动保存对话，支持标题生成

### 🔧 代码工具集
- **语法检查器**：详细语法错误检测和修复建议
- **代码执行器**：安全沙箱执行Python代码
- **代码分析器**：代码质量分析和优化建议
- **文档查询**：Python官方文档快速查询
- **类型注解检查**：参数类型覆盖率分析

### 🎙️ 语音识别
- **实时录音**：支持WebM格式录音
- **语音转文字**：使用讯飞语音识别API
- **音频处理**：自动格式转换（WebM → PCM）
- **多语言支持**：支持中文普通话识别
- **状态反馈**：实时显示录音和识别状态

### 📸 图像上传与分析 (v1.0.1新增)
- **图片上传**：支持拖拽上传和文件选择
- **多格式支持**：PNG、JPG、JPEG、GIF、BMP、WEBP
- **图片预览**：上传前预览，上传后缩略图显示
- **AI图像理解**：支持图片内容识别和分析
- **图片删除**：随时移除已上传的图片

### 🕷️ Python网页爬虫
- **一键爬取**：输入URL即可抓取网页内容
- **Markdown转换**：自动转为可读的Markdown格式
- **内容预览**：实时预览爬取结果
- **多种操作**：复制内容或发送到对话
- **安全限制**：支持URL验证和内容过滤

### 👤 用户系统
- **用户注册/登录**：完整账户系统
- **对话历史**：按用户隔离保存
- **多对话管理**：支持创建多个对话线程
- **数据安全**：密码加密存储
- **自动清理**：定期清理空白对话

## 🏗️ 技术架构

### 前端技术栈
- **HTML5**：语义化标签，响应式设计
- **CSS3**：CSS变量主题系统，Flexbox/Grid布局
- **JavaScript**：原生ES6+，模块化设计
- **Highlight.js**：代码语法高亮
- **Font Awesome**：图标库
- **Google Fonts**：Inter字体家族

### 后端技术栈
- **Flask**：轻量级Web框架
- **PyMySQL**：MySQL数据库驱动
- **LangChain**：AI代理框架
- **DeepSeek API**：主AI模型
- **OpenAI API**：备用AI模型
- **PyMuPDF**：PDF处理库（保持向后兼容）
- **Pillow**：图像处理库
- **WebSocket**：语音识别实时通信
- **pathlib**：路径处理（v1.0.2新增）

### 新增核心组件 (v1.0.2)
**MarkdownHandbook类**：
```python
# 核心功能：
1. 索引所有Markdown文件
2. 提取章节结构
3. 智能图片提取和转换
4. 构建全文搜索索引
5. 图片与内容关联
```

### 系统架构图 (v1.0.2更新)
```
用户请求 → Flask路由 → 业务逻辑 → 数据存储/外部API
    │          │           │              │
前端界面    URL分发   AI智能代理      MySQL数据库
    │          │           │              │
语音输入   会话管理   代码工具集      用户数据
    │          │           │              │
图片上传   中间件层   Markdown文档    对话历史
    │          │    处理器(v1.0.2)    消息记录
实时通信   错误处理   图片提取器     图片存储
    │          │           │              │
主题切换   认证授权   搜索引擎       静态资源
                        (全文索引)      (文档+图片)
```

## 📁 项目结构

```
PyAssistant/
├── app.py                    # Flask应用主文件（v1.0.2更新）
├── python_agent.py          # AI智能代理核心（v1.0.2更新）
├── markdown_handbook.py     # Markdown文档处理器（v1.0.2新增）
├── config.py               # 配置文件
├── requirements.txt        # Python依赖列表（v1.0.2更新）
├── robots.txt             # 爬虫协议
├── .env                   # 环境变量文件
├── .gitignore            # Git忽略文件
├── README.md             # 项目说明文档
├── templates/
│   └── index.html        # 主页面HTML模板（v1.0.2更新）
└── static/
    ├── style.css         # 主样式文件（v1.0.2更新）
    ├── script.js         # 前端JavaScript（v1.0.2更新）
    ├── pyassistant.png   # 应用图标
    ├── Python背记手册.pdf  # PDF手册文件（保持向后兼容）
    ├── uploads/          # 用户上传文件目录
    ├── temp/             # 临时文件目录
    └── images/
        ├── handbook/     # Markdown提取图片目录（v1.0.2新增）
        └── uploaded/     # 用户上传图片目录
    └── Python-100-Days-master/  # Markdown文档目录（v1.0.2新增）
        ├── Day01-15/
        ├── Day16-30/
        ├── Day31-45/
        └── README.md
```

## 🔧 详细配置

### 数据库配置 (`app.py`)
```python
DB_CONFIG = {
    'host': 'localhost',           # 数据库主机
    'user': 'pyassistant',         # 数据库用户
    'password': 'your_password',   # 数据库密码
    'database': 'pyassistant',     # 数据库名称
    'charset': 'utf8mb4',         # UTF-8编码
    'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式
}
```

### AI模型配置 (`python_agent.py`)
```python
# DeepSeek优先配置
self.llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.1  # 低随机性保证回答稳定
)

# OpenAI备用配置
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1
)
```

### Markdown文档配置 (v1.0.2新增)
```python
# app.py中的初始化配置
def initialize_markdown_handbook():
    """初始化Markdown文档处理器"""
    try:
        # 配置Markdown文档路径
        base_path = os.path.join(os.path.dirname(__file__), 'static', 'Python-100-Days-master')
        enhanced_handbook = MarkdownHandbook(base_path)
        print("✅ Markdown文档处理器初始化成功")
        print(f"   加载了 {len(enhanced_handbook.md_files)} 个Markdown文件")
        print(f"   索引了 {len(enhanced_handbook.images_cache)} 张图片")
        return True
    except Exception as e:
        print(f"❌ Markdown文档处理器初始化失败: {e}")
        return False
```

### 文件上传配置 (`app.py`)
```python
# 允许的图片格式 (v1.0.1增强)
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
# 上传目录
UPLOAD_FOLDER = 'static/uploads'
# 最大文件大小：10MB
MAX_IMAGE_SIZE = 10 * 1024 * 1024
```

## 📖 使用指南

### 首次使用流程
1. **注册账户**：点击登录按钮 → 切换到注册标签 → 输入用户名和密码
2. **开始对话**：在输入框中输入Python相关问题 → 发送
3. **探索功能**：
   - 使用右上角按钮新建对话
   - 点击示例问题快速体验
   - 试用插入代码模板功能
   - 切换深色/浅色主题

### 新功能使用流程 (v1.0.2)

#### 1. Markdown文档搜索
```
1. 点击左侧边栏的"文档搜索"图标
2. 在搜索框中输入关键词（如："装饰器"、"多线程"）
3. 查看搜索结果：
   - 文本内容：显示相关文档片段
   - 章节信息：显示文档章节结构
   - 相关图片：显示文档中的相关图片
4. 点击图片可以预览
5. 点击文档标题可以查看完整内容
```

#### 2. 图片提取和预览
```
1. 文档中的图片会自动提取并转换为base64格式
2. 网络图片会保持原URL
3. 本地图片会复制到static/images/handbook目录
4. 支持图片预览和放大查看
```

#### 3. 文档内容查看
```
1. 在搜索结果中点击"查看完整内容"
2. 或者使用"文档管理"功能浏览所有Markdown文件
3. 支持文档内的图片展示和代码高亮
```

### 核心功能使用示例

**Markdown文档搜索示例 (v1.0.2新增)：**
```
输入：Python装饰器

输出：
## 📚 《Python-100-Days》相关内容

### 📖 相关文本内容
1. **Day01-15/08.装饰器.md** - 《Python-100-Days》Day01-15/08.装饰器.md: 装饰器是Python中用于修改函数或类行为的语法糖...

### 📑 相关章节
1. **装饰器的定义** (来自: Day01-15/08.装饰器.md)
   装饰器是Python中非常重要的一个特性...

### 🖼️ 相关图表和示例
- **装饰器执行流程** (来自: Day01-15/08.装饰器.md)
  [图片预览...]
```

**语法检查：**
```python
# 输入要检查的代码
def calculate_sum(a, b)
    return a + b

# 输出结果
✅ 语法检查通过：未发现语法错误
结构概览:
• 总行数: 2
• 函数数量: 1
• 类数量: 0
• 引入模块: （无）

风格建议:
• 第1行缺少冒号
• 建议添加函数文档字符串
```

**代码执行：**
```python
# 输入代码
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"平方数: {squares}")

# 输出结果
✅ 执行成功:
平方数: [1, 4, 9, 16, 25]
```

**图像上传功能 (v1.0.1新增)：**
1. 点击"上传图片"按钮或拖拽图片到上传区域
2. 选择图片文件（支持PNG、JPG、GIF等格式）
3. 图片自动上传并显示预览缩略图
4. 可在输入框中引用图片进行分析
5. 点击"×"按钮可删除已上传图片

### 语音输入
1. 点击麦克风按钮开始录音
2. 说话内容实时转文字
3. 点击停止结束录音
4. 识别结果自动填入输入框

### 网页爬虫
1. 切换到"Python爬虫"标签页
2. 输入目标网址（如：https://example.com）
3. 点击"开始爬取"按钮
4. 查看转换后的Markdown内容
5. 可选：复制内容或发送到对话

### 快捷键
- `Ctrl + Enter` - 发送消息
- `Ctrl + N` - 新建对话
- `Ctrl + T` - 切换主题
- `Ctrl + M` - 语音输入
- `Ctrl + I` - 打开图片上传
- `Ctrl + /` - 显示帮助

### 移动端适配
- **底部导航栏**：快速切换主要功能
- **侧滑菜单**：左滑显示对话历史
- **触摸优化**：增大按钮点击区域
- **响应式布局**：自动适配屏幕尺寸
- **图片上传**：移动端相机支持

## 📊 数据库设计

### 表结构详情

**用户表 (users)**
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
);
```

**对话表 (conversations)**
```sql
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) DEFAULT '新对话',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_updated_at (updated_at)
);
```

**消息表 (messages)**
```sql
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    role ENUM('user', 'assistant', 'system') NOT NULL,
    content TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text',
    has_image BOOLEAN DEFAULT FALSE,  -- v1.0.1新增：标记是否包含图片
    image_path VARCHAR(500),          -- v1.0.1新增：图片存储路径
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_has_image (has_image)   -- v1.0.1新增：图片查询优化
);
```

**图片元数据表 (v1.0.1新增)**
```sql
CREATE TABLE image_metadata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    conversation_id INT,
    message_id INT,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL,
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE SET NULL,
    INDEX idx_user_upload (user_id, upload_time),
    INDEX idx_conversation (conversation_id)
);
```

### 数据关系
```
用户(1) → 对话(N) → 消息(N)
    │          │          │
    ↓          ↓          ↓
   会话(1)    图片元数据(N) 
```

## 🔌 API接口

### 认证接口
#### `POST /register`
- **功能**: 用户注册
- **请求体**: 
```json
{
  "username": "用户名",
  "password": "密码"
}
```
- **响应**:
```json
{
  "success": true,
  "message": "注册成功",
  "user_id": 1
}
```

#### `POST /login`
- **功能**: 用户登录
- **请求体**:
```json
{
  "username": "用户名",
  "password": "密码"
}
```
- **响应**:
```json
{
  "success": true,
  "message": "登录成功",
  "username": "用户名"
}
```

#### `POST /logout`
- **功能**: 用户登出
- **响应**:
```json
{"success": true, "message": "已登出"}
```

#### `GET /check_login`
- **功能**: 检查登录状态
- **响应**:
```json
{
  "is_logged_in": true,
  "username": "用户名"
}
```

### 对话接口
#### `POST /ask`
- **功能**: 发送问题获取AI回答
- **请求体**:
```json
{
  "question": "Python问题",
  "conversation_id": 1,
  "images": ["image1.jpg", "image2.png"]  // v1.0.1新增：支持图片数组
}
```
- **响应**:
```json
{
  "success": true,
  "answer": "AI回答内容",
  "conversation_id": 1,
  "images": ["handbook/image1.png"]  // v1.0.1新增：返回相关图片
}
```

#### `POST /new_conversation`
- **功能**: 创建新对话
- **请求体**:
```json
{"title": "对话标题"}
```
- **响应**:
```json
{
  "success": true,
  "conversation_id": 2,
  "title": "对话标题"
}
```

#### `GET /get_conversations`
- **功能**: 获取当前用户的对话列表
- **响应**:
```json
{
  "success": true,
  "conversations": [
    {
      "id": 1,
      "title": "Python学习",
      "created_at": "2024-01-15 10:30:00",
      "message_count": 5
    }
  ]
}
```

#### `POST /load_conversation/<id>`
- **功能**: 加载指定对话的所有消息
- **响应**:
```json
{
  "success": true,
  "messages": [
    {
      "role": "user",
      "content": "用户问题",
      "timestamp": "2024-01-15 10:31:00"
    }
  ],
  "images": [  // v1.0.1新增：返回对话中的图片
    "uploads/user1/image1.jpg"
  ]
}
```

#### `POST /delete_conversation/<id>`
- **功能**: 删除对话及所有相关消息和图片
- **响应**:
```json
{"success": true, "message": "对话已删除"}
```

#### `POST /clear`
- **功能**: 清空当前对话的消息历史
- **响应**:
```json
{"success": true, "message": "对话已清空"}
```

### 工具接口
#### `POST /syntax_check`
- **功能**: Python代码语法检查
- **请求体**:
```json
{"code": "def test():\n    pass"}
```
- **响应**:
```json
{
  "success": true,
  "result": "语法检查结果",
  "errors": [],
  "warnings": ["缺少文档字符串"]
}
```

#### `POST /execute_code`
- **功能**: 执行Python代码并返回结果
- **请求体**:
```json
{"code": "print('Hello, World!')"}
```
- **响应**:
```json
{
  "success": true,
  "output": "Hello, World!",
  "execution_time": 0.12
}
```

#### `POST /analyze_code`
- **功能**: 代码质量分析
- **请求体**:
```json
{"code": "def func(x): return x*2"}
```
- **响应**:
```json
{
  "success": true,
  "analysis": {
    "complexity": "低",
    "style_score": 85,
    "suggestions": ["建议添加类型注解"]
  }
}
```

#### `POST /get_documentation`
- **功能**: Python文档查询
- **请求体**:
```json
{"keyword": "decorator"}
```
- **响应**:
```json
{
  "success": true,
  "docs": [
    {
      "module": "functools",
      "function": "wraps",
      "description": "用于保留原函数元数据的装饰器"
    }
  ]
}
```

#### `POST /web_crawler`
- **功能**: 网页爬取并转换为Markdown
- **请求体**:
```json
{"url": "https://example.com"}
```
- **响应**:
```json
{
  "success": true,
  "title": "示例网站",
  "markdown": "# 标题\n\n内容...",
  "images": ["https://example.com/image.jpg"]
}
```

### 语音接口
#### `POST /voice_recognition`
- **功能**: 语音识别
- **请求格式**: `multipart/form-data`
- **参数**: `audio_file` (WebM音频文件)
- **响应**:
```json
{
  "success": true,
  "text": "识别出的文本",
  "confidence": 0.95
}
```

#### `GET /voice_config`
- **功能**: 获取语音识别配置
- **响应**:
```json
{
  "success": true,
  "config": {
    "supported_formats": ["webm", "wav"],
    "max_duration": 60,
    "language": "zh-CN"
  }
}
```

### Markdown文档接口 (v1.0.2新增)

#### `POST /enhanced_search`
- **功能**: 增强Markdown搜索（支持文本和图片检索）
- **请求体**:
```json
{
  "query": "Python装饰器"
}
```
- **响应**:
```json
{
  "success": true,
  "text_results": [
    {
      "type": "text",
      "content": "《Python-100-Days》Day01-15/08.装饰器.md: 装饰器是Python中用于修改函数或类行为的语法糖...",
      "file": "Day01-15/08.装饰器.md",
      "relevance": "high"
    }
  ],
  "image_results": [
    {
      "caption": "装饰器执行流程",
      "file": "Day01-15/08.装饰器.md",
      "type": "local",
      "base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...",
      "url": "/static/images/handbook/decorator_flow.png"
    }
  ],
  "sections": [
    {
      "title": "装饰器的定义",
      "file": "Day01-15/08.装饰器.md",
      "content": "装饰器是Python中非常重要的一个特性...",
      "full_content": "# 装饰器 (Decorator)..."
    }
  ]
}
```

#### `GET /get_markdown_files`
- **功能**: 获取所有Markdown文件列表
- **响应**:
```json
{
  "success": true,
  "files": [
    {
      "path": "Day01-15/01.基础知识.md",
      "name": "01.基础知识.md",
      "size": 20480,
      "modified": "2025-12-01T10:30:00",
      "has_images": true
    }
  ],
  "total_files": 45,
  "total_images": 120
}
```

#### `GET /get_markdown_content/<path:file_path>`
- **功能**: 获取指定Markdown文件的内容
- **参数**: file_path - 文件相对路径
- **响应**:
```json
{
  "success": true,
  "content": "# Python基础知识\n\nPython是一种解释型、面向对象...",
  "path": "Day01-15/01.基础知识.md",
  "images": [
    {
      "type": "local",
      "path": "static/images/handbook/basics_flow.png",
      "url": "/static/images/handbook/basics_flow.png",
      "alt": "Python执行流程",
      "title": "Python程序执行流程"
    }
  ],
  "image_count": 3
}
```

#### `POST /search_markdown`
- **功能**: 全文搜索Markdown内容
- **请求体**:
```json
{
  "query": "多线程编程"
}
```
- **响应**:
```json
{
  "success": true,
  "results": [
    {
      "file": "Day16-30/25.多线程编程.md",
      "context": "Python中的<mark>多线程编程</mark>可以使用threading模块...",
      "position": 125,
      "score": 0.85
    }
  ],
  "total_matches": 5
}
```

#### `POST /get_pdf_images`
- **功能**: 获取与主题相关的图片（保持向后兼容）
- **请求体**:
```json
{
  "topic": "装饰器"
}
```
- **响应**:
```json
{
  "success": true,
  "images": [
    {
      "type": "local",
      "path": "static/images/handbook/decorator_flow.png",
      "url": "/static/images/handbook/decorator_flow.png",
      "alt": "装饰器执行流程",
      "title": "装饰器工作原理",
      "base64": "data:image/png;base64,..."
    }
  ],
  "count": 2
}
```

#### `POST /upload_markdown_image`
- **功能**: 上传文档中的图片（内部使用）
- **请求体**:
```json
{
  "path": "Day01-15/images/decorator_flow.png"
}
```
- **响应**:
```json
{
  "success": true,
  "image": {
    "type": "local",
    "path": "static/images/handbook/decorator_flow.png",
    "url": "/static/images/handbook/decorator_flow.png",
    "alt": "装饰器执行流程",
    "title": "装饰器工作原理"
  }
}
```

### 增强型对话接口

#### `POST /ask_with_image`
- **功能**: 带图片和文档内容的提问
- **请求体**:
```json
{
  "question": "Python装饰器是什么？",
  "image": "base64图片数据（可选）"
}
```
- **响应**:
```json
{
  "success": true,
  "answer": "基于《Python-100-Days》和相关图片的分析结果...",
  "has_images": true,
  "timestamp": "2025-12-01 10:30:00"
}
```

## 🛠️ 开发指南

### 添加新功能模块

**1. 添加新的AI工具**
```python
# 在 python_agent.py 中添加
class PythonProgrammingAgent:
    def new_tool(self, input_data: str) -> str:
        """新工具的功能描述"""
        try:
            # 实现工具逻辑
            result = process_input(input_data)
            return result
        except Exception as e:
            return f"工具执行错误: {str(e)}"
    
    def __init__(self):
        # 注册新工具
        self.tools["new_tool"] = self.new_tool
```

**2. 添加前端页面**
```html
<!-- 在 index.html 中添加新标签页 -->
<div class="new-container" id="newTab" style="display: none;">
    <div class="new-header">
        <h2><i class="fas fa-new-icon"></i> 新功能</h2>
    </div>
    <!-- 页面内容 -->
</div>

<!-- 在导航中添加 -->
<div class="nav-item" data-tab="new">
    <i class="fas fa-new-icon"></i>
    <span>新功能</span>
</div>
```

**3. 添加后端路由**
```python
# 在 app.py 中添加
@app.route('/new_tool', methods=['POST'])
@require_login
def new_tool():
    """新工具的处理路由"""
    try:
        data = request.get_json()
        # 处理逻辑
        result = process_data(data)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 代码规范

**Python代码规范**
- 使用类型注解
- 添加详细的文档字符串
- 遵循PEP 8风格指南
- 异常处理要具体

**JavaScript代码规范**
- 使用ES6+语法
- 函数添加JSDoc注释
- 变量使用有意义的命名
- 错误处理使用try-catch

### Markdown文档处理机制 (v1.0.2新增)

**1. 文档索引流程**
```python
class MarkdownHandbook:
    def load_markdown_files(self):
        # 1. 遍历所有.md文件
        # 2. 读取文件内容
        # 3. 提取章节结构
        # 4. 提取图片信息
        # 5. 构建搜索索引
        # 6. 缓存文本内容
```

**2. 图片处理流程**
```python
def _extract_images(self, file_key: str, content: str, md_path: Path):
    # 1. 匹配Markdown图片语法
    # 2. 处理本地图片路径
    # 3. 转换为base64格式
    # 4. 复制到静态目录
    # 5. 建立图片索引
```

**3. 搜索算法**
```python
def search_with_images(self, query: str, max_results: int = 5):
    # 1. 章节搜索
    # 2. 关键词索引搜索
    # 3. 图片索引搜索
    # 4. 模糊匹配
    # 5. 结果合并和排序
```

## 🐛 故障排除

### 常见问题解决方案

**1. 应用启动失败**
```bash
# 端口被占用
lsof -i :5007
kill -9 <PID>
# 或更换端口
python app.py --port 5008
```

**2. 数据库连接错误**
```bash
# 检查MySQL服务状态
sudo systemctl status mysql
# 启动服务
sudo systemctl start mysql
# 检查连接配置
mysql -u root -p -e "SHOW GRANTS FOR 'pyassistant'@'localhost';"
```

**3. 语音识别失败**
```bash
# 安装音频处理工具
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg
# macOS
brew install ffmpeg
# Windows：下载FFmpeg并添加到PATH
```

**4. AI服务不可用**
```bash
# 检查API密钥
echo $DEEPSEEK_API_KEY
echo $OPENAI_API_KEY
# 重新配置.env文件
```

**5. PDF手册加载失败** (保持向后兼容)
```bash
# 检查PyMuPDF安装
pip install PyMuPDF
# 检查PDF文件路径
ls -la static/Python背记手册.pdf
```

**6. 图片上传失败 (v1.0.1新增)**
```bash
# 检查图片目录权限
chmod -R 755 static/uploads/
chmod -R 755 static/images/
# 检查Pillow安装
pip install Pillow
# 检查文件大小限制
# 确保MAX_IMAGE_SIZE设置足够大
```

**7. Markdown文档加载失败 (v1.0.2新增)**
```bash
# 检查文档路径
ls -la static/Python-100-Days-master/

# 检查Python-100-Days项目是否存在
# 如果不存在，需要下载项目：
git clone https://github.com/jackfrued/Python-100-Days.git static/Python-100-Days-master
```

**8. 图片提取失败 (v1.0.2新增)**
```bash
# 检查图片权限
chmod -R 755 static/images/handbook/

# 检查依赖库
pip install Pillow

# 检查临时目录权限
chmod 777 /tmp
```

**9. 搜索索引构建失败 (v1.0.2新增)**
```python
# 在app.py中查看初始化日志
# 如果索引失败，尝试手动重建：
python -c "from markdown_handbook import MarkdownHandbook; hb = MarkdownHandbook('static/Python-100-Days-master')"
```

### 性能优化建议

**数据库优化**
```sql
-- 添加复合索引
CREATE INDEX idx_conversations_user_updated 
ON conversations(user_id, updated_at DESC);

-- 为图片元数据表添加索引
CREATE INDEX idx_image_metadata_user_conversation 
ON image_metadata(user_id, conversation_id);

-- 定期清理历史数据
DELETE FROM messages 
WHERE timestamp < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- 清理孤立图片记录
DELETE FROM image_metadata 
WHERE conversation_id IS NULL 
AND upload_time < DATE_SUB(NOW(), INTERVAL 7 DAY);

-- 新增文档元数据索引 (v1.0.2新增)
CREATE INDEX idx_messages_content_search 
ON messages(content(255));
```

**缓存优化**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_handbook_content(query: str) -> str:
    """缓存手册查询结果"""
    return enhanced_handbook.search_with_images(query)

@lru_cache(maxsize=256)
def get_pdf_image_cache(page: int) -> bytes:
    """缓存PDF图片提取结果（保持向后兼容）"""
    return extract_pdf_image(page)

# Markdown文档缓存优化 (v1.0.2新增)
@lru_cache(maxsize=100)
def get_cached_markdown_content(file_path: str) -> str:
    """缓存Markdown文件内容"""
    return enhanced_handbook.get_file_content(file_path)

@lru_cache(maxsize=200)
def get_cached_search_results(query: str) -> Dict:
    """缓存搜索结果"""
    return enhanced_handbook.search_with_images(query)
```

**资源管理**
```python
# 清理临时文件和过期图片
import tempfile
import shutil
from datetime import datetime, timedelta

def cleanup_temp_files():
    """清理临时目录和过期上传"""
    temp_dir = tempfile.gettempdir()
    for file in os.listdir(temp_dir):
        if file.startswith('pyassistant_'):
            os.remove(os.path.join(temp_dir, file))
    
    # 清理超过7天的上传图片
    upload_dir = 'static/images/uploaded'
    for filename in os.listdir(upload_dir):
        filepath = os.path.join(upload_dir, filename)
        if os.path.isfile(filepath):
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if datetime.now() - mtime > timedelta(days=7):
                os.remove(filepath)
                logger.info(f"清理过期图片: {filename}")
```

**内存占用优化 (v1.0.2新增)**
```python
# 调整Markdown文档缓存大小
class MarkdownHandbook:
    def __init__(self, base_path: str, max_cache_size: int = 100):
        # 限制缓存的文件数量
        self.max_cache_size = max_cache_size

def cleanup_handbook_images():
    """清理文档图片缓存 (v1.0.2新增)"""
    import time
    handbook_dir = Path("static/images/handbook")
    cutoff_time = time.time() - 30 * 24 * 3600  # 30天前
    
    for img_file in handbook_dir.glob("*.png"):
        if img_file.stat().st_mtime < cutoff_time:
            img_file.unlink()
            logger.info(f"清理过期文档图片: {img_file.name}")
```

## 🔄 部署选项

### Docker部署 (v1.0.2更新)
```dockerfile
# Dockerfile (v1.0.2更新)
FROM python:3.9-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 下载Python-100-Days文档 (v1.0.2新增)
RUN git clone https://github.com/jackfrued/Python-100-Days.git static/Python-100-Days-master

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建必要的目录
RUN mkdir -p static/uploads static/images/handbook

EXPOSE 5007

CMD ["python", "app.py"]
```

### Nginx反向代理
```nginx
# nginx配置 (包含大文件上传支持)
server {
    listen 80;
    server_name pyassistant.yourdomain.com;
    
    # 增加上传文件大小限制
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://localhost:5007;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # 静态文件直接由nginx服务
    location /static/ {
        alias /opt/pyassistant/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Nginx配置更新 (v1.0.2)
```nginx
# nginx配置（支持大文档加载）
server {
    listen 80;
    server_name pyassistant.yourdomain.com;
    
    # 增加文件上传和文档加载大小限制
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://localhost:5007;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 增加超时设置
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # 静态文件直接由nginx服务
    location /static/ {
        alias /opt/pyassistant/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        
        # 特别处理文档目录 (v1.0.2新增)
        location ~* \.(md|markdown)$ {
            add_header Content-Type "text/markdown; charset=utf-8";
        }
    }
}
```

### 系统服务 (Systemd)
```ini
# /etc/systemd/system/pyassistant.service (v1.0.2更新)
[Unit]
Description=PyAssistant Python AI Assistant (v1.0.2)
After=network.target mysql.service
Requires=mysql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/pyassistant
Environment=PATH=/opt/pyassistant/venv/bin
EnvironmentFile=/opt/pyassistant/.env
ExecStart=/opt/pyassistant/venv/bin/python app.py
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=pyassistant

# 资源限制
LimitNOFILE=65536
LimitNPROC=4096
MemoryMax=2G

# 安全设置
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/pyassistant/static/uploads /opt/pyassistant/static/images

[Install]
WantedBy=multi-user.target
```

## 📈 监控和维护

### 健康检查接口 (v1.0.2增强)
```python
# 在app.py中添加健康检查接口
@app.route('/health')
def health_check():
    """系统健康检查"""
    health_status = {
        'status': 'healthy',
        'version': '1.0.2',
        'agent_type': 'PythonProgrammingAgent',
        'markdown_status': 'loaded' if enhanced_handbook else 'not_loaded',  # v1.0.2更新
        'markdown_files': len(enhanced_handbook.md_files) if enhanced_handbook else 0,  # v1.0.2新增
        'markdown_images': len(enhanced_handbook.images_cache) if enhanced_handbook else 0,  # v1.0.2新增
        'database': 'connected',
        'upload_dir': os.path.isdir(UPLOAD_FOLDER),
        'handbook_dir': os.path.isdir('static/images/handbook'),
        'documents_dir': os.path.isdir('static/Python-100-Days-master'),  # v1.0.2新增
        'timestamp': datetime.now().isoformat()
    }
    
    # 检查外部服务
    try:
        health_status['deepseek_api'] = 'available' if check_deepseek_api() else 'unavailable'
        health_status['speech_api'] = 'available' if check_speech_api() else 'unavailable'
    except Exception as e:
        health_status['external_services'] = f'check_error: {str(e)}'
    
    return jsonify(health_status)
```

### 日志管理 (v1.0.2增强)
```python
# 配置详细日志
import logging
from logging.handlers import RotatingFileHandler

# 创建日志目录
os.makedirs('logs', exist_ok=True)

# 主日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=10*1024*1024, backupCount=5),
        RotatingFileHandler('logs/error.log', maxBytes=5*1024*1024, backupCount=3, level=logging.ERROR),
        logging.StreamHandler()
    ]
)

# 图片上传专用日志 (v1.0.1新增)
upload_logger = logging.getLogger('image_upload')
upload_handler = RotatingFileHandler('logs/upload.log', maxBytes=5*1024*1024, backupCount=3)
upload_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
upload_logger.addHandler(upload_handler)
upload_logger.setLevel(logging.INFO)

# 文档处理专用日志 (v1.0.2新增)
document_logger = logging.getLogger('markdown_documents')
document_handler = RotatingFileHandler('logs/documents.log', maxBytes=5*1024*1024, backupCount=3)
document_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
document_logger.addHandler(document_handler)
document_logger.setLevel(logging.INFO)
```

### 定期维护任务 (v1.0.2更新)
```python
# 在app.py中添加维护函数
def perform_maintenance():
    """执行定期维护任务"""
    tasks = [
        cleanup_temp_files,           # 清理临时文件
        delete_old_conversations,     # 删除旧对话
        reindex_markdown_documents,   # v1.0.2新增：重新索引Markdown文档
        backup_database,              # 备份数据库
        cleanup_orphaned_images,      # v1.0.1新增：清理孤立图片
        optimize_database_tables,     # 优化数据库表
        validate_document_links,      # v1.0.2新增：验证文档链接
        compress_document_images      # v1.0.2新增：压缩文档图片
    ]
    
    for task in tasks:
        try:
            result = task()
            logger.info(f"维护任务完成: {task.__name__} - {result}")
        except Exception as e:
            logger.error(f"维护任务失败 {task.__name__}: {e}")
    
    # 记录维护日志
    maintenance_log = {
        'timestamp': datetime.now().isoformat(),
        'tasks_executed': len(tasks),
        'status': 'completed'
    }
    
    # 保存维护记录
    with open('logs/maintenance.json', 'a') as f:
        f.write(json.dumps(maintenance_log) + '\n')
    
    return maintenance_log

# 定时执行维护任务（每天凌晨3点）
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(func=perform_maintenance, trigger='cron', hour=3, minute=0)
scheduler.start()
```

## 🤝 贡献指南

### 开发流程
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

### 提交规范 (v1.0.2更新)
- `feat`: 新功能（如：Markdown文档搜索）
- `fix`: 修复bug（如：图片提取问题）
- `docs`: 文档更新（如：API文档）
- `style`: 代码格式调整
- `perf`: 性能优化（如：搜索速度提升）
- `refactor`: 代码重构（如：文档处理器重构）
- `test`: 测试相关（如：文档搜索测试）
- `chore`: 构建过程或辅助工具变动

### 测试要求
- 新功能需包含单元测试
- 确保现有测试通过
- 更新相关文档
- 遵循代码规范

### 新增贡献方向 (v1.0.2)
- **文档搜索算法优化**：改进搜索准确性和性能
- **图片处理增强**：支持更多图片格式和压缩算法
- **文档解析改进**：更好的Markdown语法支持
- **缓存机制优化**：更高效的文档内容缓存
- **移动端适配**：优化移动端文档查看体验

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持与反馈

- **问题反馈**: 通过GitHub Issues提交
- **功能建议**: 欢迎提出新功能建议
- **技术讨论**: 在Discussions板块交流
- **紧急问题**: 查看故障排除章节

## 🎉 版本历史

### v1.0.2 (当前版本) - 2025年12月重大更新
#### 核心升级
- ✅ **文档检索全面升级**：PDF → Markdown，更精确、更快速
- ✅ **完整项目支持**：支持Python-100-days-master所有文档
- ✅ **智能图片提取**：自动提取文档图片并转换
- ✅ **章节结构化**：自动识别和索引文档章节
- ✅ **多模式搜索**：章节、关键词、全文、模糊搜索

#### 架构优化
- 🔧 **界面重构**：文档功能移至侧边栏，更专业
- 🔧 **性能提升**：文档检索速度提升5-10倍
- 🔧 **缓存优化**：智能缓存机制，减少重复加载
- 🔧 **API增强**：新增Markdown相关API接口
- 🔧 **向后兼容**：保持原有PDF接口兼容性

#### Bug修复
- 🐛 修复大文档加载内存问题
- 🐛 修复图片路径解析问题
- 🐛 修复搜索索引构建异常
- 🐛 修复文档编码识别问题

### v1.0.1 (上一版本) - 2025年12月更新
#### 新增功能
- ✅ **增强PDF识别**：改进图片提取算法，支持批量处理
- ✅ **图像上传功能**：支持多格式图片上传和预览
- ✅ **多模态对话**：支持图片+文本混合输入
- ✅ **图片分析**：AI可以分析上传的图片内容
- ✅ **图片管理**：图片上传、预览、删除完整流程
- ✅ **数据库优化**：新增图片元数据表和相关索引

#### 改进内容
- 🔧 优化PDF手册图片检索准确度
- 🔧 增强API接口文档和错误处理
- 🔧 改进文件上传安全性检查
- 🔧 优化移动端图片上传体验
- 🔧 添加图片压缩和缩略图生成

#### Bug修复
- 🐛 修复PDF图片提取时的内存泄漏问题
- 🐛 修复文件上传时的路径安全问题
- 🐛 修复对话中图片显示异常问题
- 🐛 修复数据库连接池管理问题

### v1.0.0 (基础版本)
- ✅ 完整的AI对话系统
- ✅ 代码工具集（语法检查、执行、分析）
- ✅ 增强PDF手册带图片检索
- ✅ 语音识别功能
- ✅ Python网页爬虫
- ✅ 用户系统和对话历史
- ✅ 响应式Web界面
- ✅ 完整的API接口

### 未来计划
- [ ] 实时协作功能
- [ ] 更多编程语言文档支持
- [ ] 离线文档搜索
- [ ] 文档版本管理
- [ ] API文档自动生成
- [ ] 代码片段库
- [ ] 学习进度跟踪
- [ ] 移动端App

---

**感谢使用PyAssistant v1.0.2！** 🚀

如果您觉得这个项目有帮助，请考虑：
- ⭐ Star这个项目
- 📢 分享给其他开发者
- 🐛 报告遇到的问题
- 💡 提出改进建议

让我们一起打造更好的Python开发体验！
