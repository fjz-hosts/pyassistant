from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).parent

# 上传配置
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# PDF配置
PDF_HANDBOOK_PATH = BASE_DIR / 'static' / 'Python背记手册.pdf'

# 确保目录存在
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)