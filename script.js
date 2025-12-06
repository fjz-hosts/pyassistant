:root {
    /* 深色主题变量 (默认) */
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #10b981;
    --accent: #f59e0b;
    --danger: #ef4444;
    --dark-1: #0f172a;
    --dark-2: #1e293b;
    --dark-3: #334155;
    --light-1: #f8fafc;
    --light-2: #e2e8f0;
    --light-3: #cbd5e1;
    --radius: 12px;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --transition: all 0.3s ease;
}

[data-theme="light"] {
    /* 浅色主题变量 */
    --dark-1: #ffffff;
    --dark-2: #f8fafc;
    --dark-3: #e2e8f0;
    --light-1: #0f172a;
    --light-2: #1e293b;
    --light-3: #475569;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, var(--dark-1) 0%, var(--dark-2) 100%);
    color: var(--light-1);
    min-height: 100vh;
    line-height: 1.6;
    overflow: hidden;
    transition: background-color 0.3s ease, color 0.3s ease;
}

/* 浅色主题特定样式 */
[data-theme="light"] {
    background: linear-gradient(135deg, var(--dark-1) 0%, var(--dark-2) 100%);
}

[data-theme="light"] .sidebar {
    border-right-color: var(--dark-3);
    background: var(--dark-2);
}

[data-theme="light"] .logo {
    border-bottom-color: var(--dark-3);
}

[data-theme="light"] .nav-section {
    border-bottom-color: var(--dark-3);
}

[data-theme="light"] .history-item {
    border-bottom-color: rgba(0, 0, 0, 0.05);
}

[data-theme="light"] .history-item:hover {
    background: rgba(0, 0, 0, 0.02);
}

[data-theme="light"] .nav-item:hover {
    background: rgba(0, 0, 0, 0.02);
}

[data-theme="light"] .header {
    border-bottom-color: var(--dark-3);
    background: var(--dark-2);
}

[data-theme="light"] .input-container {
    border-top-color: var(--dark-3);
    background: var(--dark-2);
}

[data-theme="light"] .message-content {
    background: var(--dark-2);
    border: 1px solid var(--dark-3);
    color: var(--light-1);
}

[data-theme="light"] .user .message-content {
    background: var(--primary);
    color: white;
    border: none;
}

[data-theme="light"] .system .message-content {
    background: var(--accent);
    color: white;
    border: none;
}

[data-theme="light"] .message-text code {
    background: var(--dark-3);
    color: var(--light-1);
}

[data-theme="light"] .message-text pre {
    background: var(--dark-3) !important;
    border: 1px solid var(--dark-3);
}

[data-theme="light"] .message-text pre code {
    background: transparent;
}

[data-theme="light"] .tool-card {
    border-color: var(--dark-3);
    background: var(--dark-2);
}

[data-theme="light"] .tool-card:hover {
    border-color: var(--primary);
}

[data-theme="light"] .action-btn {
    border-color: var(--dark-3);
    color: var(--light-2);
}

[data-theme="light"] .action-btn:hover {
    background: rgba(0, 0, 0, 0.02);
    color: var(--light-1);
}

[data-theme="light"] .input-field {
    border-color: var(--dark-3);
    background: var(--dark-1);
    color: var(--light-1);
}

[data-theme="light"] .btn-outline {
    border-color: var(--dark-3);
    color: var(--light-2);
    background: transparent;
}

[data-theme="light"] .btn-outline:hover {
    background: rgba(0, 0, 0, 0.02);
    color: var(--light-1);
}

[data-theme="light"] .tool-input,
[data-theme="light"] .tool-input-text {
    border-color: var(--dark-3);
    background: var(--dark-1);
    color: var(--light-1);
}

[data-theme="light"] .feature-item {
    background: var(--dark-2);
    border-color: var(--dark-3);
    color: var(--light-1);
}

[data-theme="light"] .feature-item span {
    color: var(--light-2);
}

[data-theme="light"] .welcome-subtitle {
    color: var(--light-3);
}

[data-theme="light"] .nav-title {
    color: var(--light-3);
}

[data-theme="light"] .history-date {
    color: var(--light-3);
}

[data-theme="light"] .message-time {
    color: var(--light-3);
}

[data-theme="light"] .user .message-time {
    color: rgba(255, 255, 255, 0.7);
}

[data-theme="light"] .system .message-time {
    color: rgba(255, 255, 255, 0.7);
}

[data-theme="light"] .typing-indicator {
    background: var(--dark-2);
}

[data-theme="light"] .typing-dot {
    background: var(--light-3);
}

/* 代码执行结果浅色主题样式 */
[data-theme="light"] .code-execution-result {
    background: var(--dark-2);
    border-color: var(--dark-3);
}

[data-theme="light"] .execution-header {
    background: rgba(99, 102, 241, 0.1);
    border-bottom-color: var(--dark-3);
    color: var(--primary);
}

[data-theme="light"] .code-execution-result.error .execution-header {
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger);
}

[data-theme="light"] .section-title {
    color: var(--light-3);
}

[data-theme="light"] .output-content,
[data-theme="light"] .error-content {
    background: var(--dark-1);
    border-color: var(--dark-3);
    color: var(--light-1);
}

[data-theme="light"] .output-content {
    background: rgba(16, 185, 129, 0.05);
    border-color: rgba(16, 185, 129, 0.2);
}

[data-theme="light"] .error-content {
    background: rgba(239, 68, 68, 0.05);
    border-color: rgba(239, 68, 68, 0.2);
}

/* 代码高亮浅色主题 */
[data-theme="light"] .hljs {
    background: var(--dark-1) !important;
    border-color: var(--dark-3);
}

[data-theme="light"] .hljs-keyword {
    color: #d73a49 !important;
}

[data-theme="light"] .hljs-built_in {
    color: #6f42c1 !important;
}

[data-theme="light"] .hljs-string {
    color: #032f62 !important;
}

[data-theme="light"] .hljs-number {
    color: #005cc5 !important;
}

[data-theme="light"] .hljs-comment {
    color: #6a737d !important;
}

[data-theme="light"] .hljs-function {
    color: #6f42c1 !important;
}

[data-theme="light"] .hljs-params {
    color: #24292e !important;
}

[data-theme="light"] .hljs-title {
    color: #6f42c1 !important;
}

[data-theme="light"] .hljs-attr {
    color: #005cc5 !important;
}

[data-theme="light"] .hljs-variable {
    color: #24292e !important;
}

[data-theme="light"] .hljs-literal {
    color: #d73a49 !important;
}

[data-theme="light"] .hljs-type {
    color: #6f42c1 !important;
}

/* 移动端浅色主题 */
[data-theme="light"] .mobile-header,
[data-theme="light"] .mobile-bottom-nav {
    background: var(--dark-2);
    border-color: var(--dark-3);
}

/* 滚动条浅色主题 */
[data-theme="light"] ::-webkit-scrollbar-track {
    background: var(--dark-3);
}

[data-theme="light"] ::-webkit-scrollbar-thumb {
    background: var(--primary);
}

[data-theme="light"] ::-webkit-scrollbar-thumb:hover {
    background: var(--primary-dark);
}

/* 复制按钮样式 */
.message-header {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.message-actions {
    display: flex;
    gap: 8px;
}

.copy-btn {
    background: transparent;
    border: 1px solid var(--dark-3);
    border-radius: 4px;
    color: var(--light-3);
    cursor: pointer;
    padding: 4px 8px;
    font-size: 12px;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 4px;
}

.copy-btn:hover {
    background: rgba(99, 102, 241, 0.1);
    color: var(--primary);
    border-color: var(--primary);
}

.copy-btn.copied {
    background: var(--secondary);
    color: white;
    border-color: var(--secondary);
}

.copy-btn.copied i::before {
    content: "\f00c";
    /* fa-check */
}

/* 代码块复制按钮 */
.code-block-wrapper {
    position: relative;
    margin: 12px 0;
}

.code-block-header {
    position: absolute;
    top: 8px;
    right: 8px;
    display: flex;
    gap: 4px;
    opacity: 0;
    transition: var(--transition);
}

.code-block-wrapper:hover .code-block-header {
    opacity: 1;
}

.code-copy-btn {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid var(--dark-3);
    border-radius: 4px;
    color: var(--light-2);
    cursor: pointer;
    padding: 4px 8px;
    font-size: 11px;
    transition: var(--transition);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    gap: 4px;
}

.code-copy-btn:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.code-copy-btn.copied {
    background: var(--secondary);
    color: white;
    border-color: var(--secondary);
}

.code-copy-btn.copied i::before {
    content: "\f00c";
    /* fa-check */
}

.btn-text {
    font-size: 11px;
}

/* 浅色主题下的复制按钮 */
[data-theme="light"] .message-header {
    border-bottom-color: rgba(0, 0, 0, 0.1);
}

[data-theme="light"] .copy-btn {
    border-color: var(--dark-3);
    color: var(--light-3);
}

[data-theme="light"] .copy-btn:hover {
    background: rgba(99, 102, 241, 0.1);
    color: var(--primary);
}

[data-theme="light"] .code-copy-btn {
    background: rgba(248, 250, 252, 0.8);
    border-color: var(--dark-3);
    color: var(--light-3);
}

[data-theme="light"] .code-copy-btn:hover {
    background: var(--primary);
    color: white;
}

/* 主题切换按钮样式 */
#themeToggle {
    transition: var(--transition);
}

[data-theme="light"] #themeToggle {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

[data-theme="light"] #themeToggle:hover {
    background: var(--primary-dark);
    border-color: var(--primary-dark);
}

/* 语音输入按钮样式 */
.input-buttons {
    display: flex;
    gap: 8px;
    align-items: flex-end;
}

.voice-btn {
    background: var(--secondary);
    color: white;
    border: none;
    border-radius: var(--radius);
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: var(--transition);
    flex-shrink: 0;
}

.voice-btn:hover {
    background: #0da271;
    transform: translateY(-2px);
}

.voice-btn.recording {
    background: var(--danger);
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
    }

    70% {
        box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
    }
}

/* 语音状态显示 */
.voice-status {
    text-align: center;
    padding: 16px;
    background: var(--dark-2);
    border-radius: var(--radius);
    margin: 16px 24px 0;
    border: 1px solid var(--primary);
    animation: slideDown 0.3s ease;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.voice-recording {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: var(--primary);
    font-weight: 500;
}

.recording-pulse {
    animation: recordingPulse 1s infinite;
}

@keyframes recordingPulse {

    0%,
    100% {
        transform: scale(1);
        color: var(--primary);
    }

    50% {
        transform: scale(1.1);
        color: var(--danger);
    }
}

/* 语音识别结果样式 */
.voice-result {
    background: var(--dark-2);
    border: 1px solid var(--secondary);
    border-radius: var(--radius);
    padding: 12px 16px;
    margin: 8px 0;
    position: relative;
}

.voice-result-text {
    color: var(--light-2);
    font-size: 14px;
}

.voice-result-confidence {
    position: absolute;
    top: 8px;
    right: 8px;
    background: var(--secondary);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
}

/* 移动端语音按钮优化 */
@media (max-width: 768px) {
    .input-buttons {
        flex-direction: column;
        gap: 4px;
    }

    .voice-btn,
    .send-btn {
        width: 40px;
        height: 40px;
    }

    .voice-status {
        padding: 12px;
        margin: 12px 16px 0;
    }

    .voice-recording {
        font-size: 14px;
    }
}

.app-container {
    display: flex;
    min-height: 100vh;
    max-width: 1600px;
    margin: 0 auto;
}

/* 侧边栏样式 - 固定位置 */
.sidebar {
    width: 280px;
    background: var(--dark-2);
    border-right: 1px solid var(--dark-3);
    display: flex;
    flex-direction: column;
    transition: var(--transition);
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 100;
    overflow: hidden;
}

/* 侧边栏内容区域滚动 */
.sidebar-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}

.logo {
    padding: 24px 20px;
    border-bottom: 1px solid var(--dark-3);
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
}

.logo-icon {
    width: 36px;
    height: 36px;
    background: var(--primary);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

.logo-text {
    font-size: 20px;
    font-weight: 700;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.nav-section {
    padding: 20px 0;
    border-bottom: 1px solid var(--dark-3);
    flex-shrink: 0;
}

.nav-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--light-3);
    padding: 0 20px 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    color: var(--light-2);
    text-decoration: none;
    transition: var(--transition);
    cursor: pointer;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--light-1);
}

.nav-item.active {
    background: rgba(99, 102, 241, 0.1);
    color: var(--primary);
    border-right: 3px solid var(--primary);
}

.nav-item i {
    width: 20px;
    text-align: center;
}

.history-section {
    flex: 1;
    overflow-y: auto;
    padding: 20px 0;
}

.history-item {
    padding: 12px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    cursor: pointer;
    transition: var(--transition);
}

.history-item:hover {
    background: rgba(255, 255, 255, 0.05);
}

.history-title {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.history-date {
    font-size: 12px;
    color: var(--light-3);
}

/* 主内容区域样式 */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-left: 280px;
    height: 100vh;
}

/* 头部区域 - 固定位置 */
.header {
    padding: 16px 24px;
    background: var(--dark-2);
    border-bottom: 1px solid var(--dark-3);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
    z-index: 50;
    position: relative;
}

.header-title {
    font-size: 20px;
    font-weight: 600;
}

.header-actions {
    display: flex;
    gap: 12px;
}

.btn {
    padding: 8px 16px;
    border-radius: var(--radius);
    border: none;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
}

.btn-outline {
    background: transparent;
    color: var(--light-2);
    border: 1px solid var(--dark-3);
}

.btn-outline:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--light-1);
}

/* 聊天容器 - 可滚动区域 */
.chat-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
}

/* 聊天消息区域 - 可滚动 */
.chat-messages {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
    min-height: 0;
}

.message {
    display: flex;
    gap: 16px;
    max-width: 90%;
    width: 100%;
    animation: fadeIn 0.3s ease;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message.user {
    align-self: flex-end;
    flex-direction: row-reverse;
    margin-left: auto;
}

.message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.user .message-avatar {
    background: var(--primary);
}

.assistant .message-avatar {
    background: var(--secondary);
}

.system .message-avatar {
    background: var(--accent);
}

.message-content {
    background: var(--dark-2);
    border-radius: var(--radius);
    padding: 16px;
    box-shadow: var(--shadow);
    flex: 1;
    min-width: 0;
    word-break: break-word;
}

.user .message-content {
    background: var(--primary);
    color: white;
    margin-left: 20%;
}

.system .message-content {
    background: var(--accent);
    color: var(--dark-1);
}

.message-text {
    line-height: 1.6;
    width: 100%;
    overflow-x: auto;
}

.message-text pre {
    margin: 12px 0;
    border-radius: 8px;
    overflow-x: auto;
    background: var(--dark-1) !important;
    max-width: 100%;
}

.message-text code {
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    background: var(--dark-1);
    padding: 2px 6px;
    border-radius: 4px;
    white-space: pre-wrap;
}

.message-text pre code {
    background: transparent;
    padding: 16px;
    display: block;
    white-space: pre;
    overflow-x: auto;
}

.message-text pre code::-webkit-scrollbar {
    height: 8px;
}

.message-text pre code::-webkit-scrollbar-track {
    background: var(--dark-3);
    border-radius: 4px;
}

.message-text pre code::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 4px;
}

.message-text :where(h1, h2, h3, h4, h5, h6) {
    margin: 16px 0 8px 0;
    line-height: 1.3;
}

.message-text p {
    margin: 8px 0;
}

.message-text ul,
.message-text ol {
    margin: 8px 0;
    padding-left: 24px;
}

.message-text li {
    margin: 4px 0;
}

.message-text table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
}

.message-text th,
.message-text td {
    border: 1px solid var(--dark-3);
    padding: 8px 12px;
    text-align: left;
}

.message-text th {
    background: var(--dark-3);
}

.message-time {
    font-size: 12px;
    color: var(--light-3);
    margin-top: 8px;
    text-align: right;
}

.user .message-time {
    color: rgba(255, 255, 255, 0.7);
}

.system .message-time {
    color: rgba(30, 41, 59, 0.7);
}

/* 输入区域样式 - 固定位置 */
.input-container {
    padding: 24px;
    border-top: 1px solid var(--dark-3);
    background: var(--dark-2);
    flex-shrink: 0;
    z-index: 50;
    position: relative;
}

.input-box {
    display: flex;
    gap: 12px;
    align-items: flex-end;
}

.input-field {
    flex: 1;
    background: var(--dark-1);
    border: 1px solid var(--dark-3);
    border-radius: var(--radius);
    padding: 16px;
    color: var(--light-1);
    font-family: inherit;
    resize: none;
    min-height: 56px;
    max-height: 120px;
    transition: var(--transition);
}

.input-field:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.send-btn {
    background: var(--primary);
    color: white;
    border: none;
    border-radius: var(--radius);
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: var(--transition);
    flex-shrink: 0;
}

.send-btn:hover {
    background: var(--primary-dark);
    transform: translateY(-2px);
}

.input-actions {
    display: flex;
    gap: 12px;
    margin-top: 12px;
}

.action-btn {
    background: transparent;
    border: 1px solid var(--dark-3);
    border-radius: var(--radius);
    padding: 8px 12px;
    color: var(--light-2);
    cursor: pointer;
    transition: var(--transition);
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.action-btn:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--light-1);
}

/* 工具界面样式 */
.tools-container {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    min-height: 0;
}

.tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}

.tool-card {
    background: var(--dark-2);
    border-radius: var(--radius);
    padding: 24px;
    border: 1px solid var(--dark-3);
    transition: var(--transition);
}

.tool-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

.tool-icon {
    width: 50px;
    height: 50px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    color: var(--primary);
    font-size: 20px;
}

.tool-card h3 {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}

.tool-card p {
    color: var(--light-3);
    margin-bottom: 16px;
    font-size: 14px;
}

.tool-input {
    width: 100%;
    background: var(--dark-1);
    border: 1px solid var(--dark-3);
    border-radius: var(--radius);
    padding: 12px;
    color: var(--light-1);
    font-family: inherit;
    resize: vertical;
    min-height: 100px;
    margin-bottom: 12px;
    transition: var(--transition);
}

.tool-input:focus {
    outline: none;
    border-color: var(--primary);
}

.tool-input-text {
    width: 100%;
    background: var(--dark-1);
    border: 1px solid var(--dark-3);
    border-radius: var(--radius);
    padding: 12px;
    color: var(--light-1);
    font-family: inherit;
    margin-bottom: 12px;
    transition: var(--transition);
}

.tool-input-text:focus {
    outline: none;
    border-color: var(--primary);
}

.tool-button {
    width: 100%;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: var(--radius);
    padding: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition);
}

.tool-button:hover {
    background: var(--primary-dark);
}

/* 加载动画 */
.typing-indicator {
    display: inline-flex;
    gap: 4px;
    padding: 8px 16px;
    background: var(--dark-2);
    border-radius: 20px;
}

.typing-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--light-3);
    animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing {

    0%,
    60%,
    100% {
        transform: translateY(0);
        opacity: 0.4;
    }

    30% {
        transform: translateY(-5px);
        opacity: 1;
    }
}

/* 代码执行结果样式 */
.code-execution-result {
    background: var(--dark-2);
    border-radius: var(--radius);
    border: 1px solid var(--dark-3);
    overflow: hidden;
    margin: 8px 0;
    box-shadow: var(--shadow);
}

.code-execution-result.error {
    border-color: var(--danger);
}

.execution-header {
    background: rgba(99, 102, 241, 0.1);
    padding: 12px 16px;
    border-bottom: 1px solid var(--dark-3);
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: var(--primary);
}

.code-execution-result.error .execution-header {
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger);
}

.execution-content {
    padding: 16px;
}

.section-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--light-3);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.section-title::before {
    content: "▸";
    font-size: 12px;
    color: var(--primary);
}

.source-code-section {
    margin-bottom: 16px;
}

.source-code-section pre {
    margin: 0;
    border-radius: 8px;
    background: var(--dark-1) !important;
    border: 1px solid var(--dark-3);
    overflow: hidden;
}

.output-section,
.error-section {
    margin-top: 12px;
}

.output-content,
.error-content {
    background: var(--dark-1);
    padding: 12px;
    border-radius: 6px;
    border: 1px solid var(--dark-3);
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-all;
    min-height: 40px;
}

.output-content {
    color: var(--light-2);
    background: rgba(16, 185, 129, 0.05);
    border-color: rgba(16, 185, 129, 0.3);
}

.error-content {
    color: var(--danger);
    background: rgba(239, 68, 68, 0.05);
    border-color: rgba(239, 68, 68, 0.3);
}

.no-output {
    color: var(--light-3);
    font-style: italic;
}

/* 代码高亮优化 */
.hljs {
    background: var(--dark-1) !important;
    padding: 16px !important;
    border-radius: 8px;
    border: 1px solid var(--dark-3);
    font-size: 14px;
    line-height: 1.5;
}

.hljs-keyword {
    color: #ff79c6 !important;
    font-weight: 600;
}

.hljs-built_in {
    color: #50fa7b !important;
}

.hljs-string {
    color: #f1fa8c !important;
}

.hljs-number {
    color: #bd93f9 !important;
}

.hljs-comment {
    color: #6272a4 !important;
    font-style: italic;
}

.hljs-function {
    color: #8be9fd !important;
}

.hljs-params {
    color: #f8f8f2 !important;
}

.hljs-title {
    color: #8be9fd !important;
}

.hljs-attr {
    color: #50fa7b !important;
}

.hljs-variable {
    color: #f8f8f2 !important;
}

.hljs-literal {
    color: #ff79c6 !important;
}

.hljs-type {
    color: #8be9fd !important;
}

/* 移动端顶部栏 */
.mobile-header {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: var(--dark-2);
    border-bottom: 1px solid var(--dark-3);
    padding: 0 16px;
    z-index: 1000;
    align-items: center;
    justify-content: space-between;
}

.mobile-menu-toggle {
    font-size: 20px;
    color: var(--light-2);
    cursor: pointer;
    padding: 8px;
}

.mobile-logo {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    font-size: 18px;
}

.mobile-logo i {
    color: var(--primary);
}

.mobile-actions {
    display: flex;
    gap: 8px;
}

.mobile-action-btn {
    background: transparent;
    border: none;
    color: var(--light-2);
    font-size: 18px;
    cursor: pointer;
    padding: 8px;
    border-radius: 6px;
    transition: var(--transition);
}

.mobile-action-btn:hover {
    background: rgba(255, 255, 255, 0.05);
    color: var(--light-1);
}

/* 移动端底部导航 */
.mobile-bottom-nav {
    display: none;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--dark-2);
    border-top: 1px solid var(--dark-3);
    padding: 8px 0;
    z-index: 1000;
}

.mobile-bottom-nav .nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px 0;
    color: var(--light-2);
    text-decoration: none;
    transition: var(--transition);
    cursor: pointer;
    flex: 1;
    font-size: 12px;
}

.mobile-bottom-nav .nav-item.active {
    color: var(--primary);
}

.mobile-bottom-nav .nav-item i {
    font-size: 16px;
}

/* 滚动条样式 */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: var(--dark-3);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-dark);
}

/* 响应式设计 */
@media (max-width: 1024px) {
    .sidebar {
        width: 240px;
    }

    .main-content {
        margin-left: 240px;
    }
}

@media (max-width: 768px) {
    .mobile-header {
        display: flex;
    }

    .mobile-bottom-nav {
        display: flex;
    }

    .app-container {
        flex-direction: column;
        padding-top: 60px;
        padding-bottom: 60px;
    }

    .sidebar {
        position: fixed;
        top: 60px;
        left: -280px;
        height: calc(100vh - 120px);
        z-index: 999;
        transition: var(--transition);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
    }

    .sidebar.active {
        left: 0;
    }

    .main-content {
        width: 100%;
        margin-left: 0;
        height: calc(100vh - 120px);
    }

    .header {
        padding: 12px 16px;
    }

    .header-title {
        font-size: 18px;
    }

    .header-actions {
        gap: 8px;
    }

    .btn {
        padding: 6px 12px;
        font-size: 12px;
    }

    .chat-messages {
        padding: 16px;
    }

    .message {
        max-width: 95%;
    }

    .user .message-content {
        margin-left: 5%;
    }

    .input-container {
        padding: 16px;
    }

    .input-field {
        font-size: 16px;
        /* 至少16px防止iOS Safari自动放大 */
    }

    .input-actions {
        flex-wrap: wrap;
        gap: 8px;
    }

    .action-btn {
        flex: 1;
        min-width: calc(50% - 4px);
        font-size: 12px;
        padding: 6px 8px;
    }

    .tools-container {
        padding: 16px;
    }

    .tools-grid {
        grid-template-columns: 1fr;
        gap: 16px;
    }

    .tool-card {
        padding: 16px;
    }

    .tool-input,
    .tool-input-text {
        font-size: 16px;
        /* 至少16px防止iOS Safari自动放大 */
    }

    .tool-icon {
        width: 40px;
        height: 40px;
        font-size: 18px;
    }

    .tool-card h3 {
        font-size: 16px;
    }

    .tool-card p {
        font-size: 13px;
    }

    .feature-list {
        grid-template-columns: 1fr;
        gap: 12px;
    }

    .welcome-message {
        padding: 20px 16px;
    }

    .welcome-title {
        font-size: 20px;
    }

    .welcome-subtitle {
        font-size: 14px;
    }

    .message-text pre code {
        font-size: 12px;
        padding: 12px;
    }

    .code-execution-result {
        margin: 6px 0;
    }

    .execution-content {
        padding: 12px;
    }

    .output-content,
    .error-content {
        font-size: 12px;
        padding: 10px;
    }

    /* 移动端复制按钮优化 */
    .message-header {
        margin-bottom: 6px;
        padding-bottom: 6px;
    }

    .copy-btn {
        padding: 3px 6px;
        font-size: 11px;
    }

    .code-block-header {
        opacity: 1;
        /* 移动端始终显示复制按钮 */
        top: 4px;
        right: 4px;
    }

    .code-copy-btn {
        padding: 3px 6px;
        font-size: 10px;
    }
}

/* 超小屏幕优化 */
@media (max-width: 480px) {
    .mobile-header {
        height: 50px;
        padding: 0 12px;
    }

    .mobile-logo {
        font-size: 16px;
    }

    .app-container {
        padding-top: 50px;
        padding-bottom: 50px;
    }

    .sidebar {
        top: 50px;
        height: calc(100vh - 100px);
    }

    .mobile-bottom-nav {
        height: 50px;
    }

    .mobile-bottom-nav .nav-item {
        font-size: 11px;
    }

    .mobile-bottom-nav .nav-item i {
        font-size: 14px;
    }

    .header {
        padding: 8px 12px;
    }

    .header-title {
        font-size: 16px;
    }

    .header-actions {
        flex-direction: column;
        gap: 4px;
    }

    .btn {
        padding: 4px 8px;
        font-size: 11px;
    }

    .chat-messages {
        padding: 12px;
    }

    .input-container {
        padding: 12px;
    }

    .input-field {
        padding: 12px;
        font-size: 16px;
        /* 至少16px防止iOS Safari自动放大 */
    }

    .send-btn {
        width: 40px;
        height: 40px;
    }

    .tools-container {
        padding: 12px;
    }

    .tool-card {
        padding: 12px;
    }

    .tool-input,
    .tool-input-text {
        font-size: 16px;
        /* 至少16px防止iOS Safari自动放大 */
    }

    .message-avatar {
        width: 32px;
        height: 32px;
        font-size: 16px;
    }

    .message-content {
        padding: 12px;
    }

    .hljs {
        padding: 12px !important;
        font-size: 12px;
    }
}

/* 欢迎消息样式 */
.welcome-message {
    text-align: center;
    padding: 40px 20px;
}

.welcome-icon {
    font-size: 48px;
    color: var(--primary);
    margin-bottom: 16px;
}

.welcome-title {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 8px;
}

.welcome-subtitle {
    color: var(--light-3);
    margin-bottom: 24px;
}

.feature-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-top: 24px;
}

.feature-item {
    background: var(--dark-2);
    padding: 16px;
    border-radius: var(--radius);
    text-align: center;
    border: 1px solid var(--dark-3);
    transition: var(--transition);
}

.feature-item:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
}

.feature-item i {
    color: var(--primary);
    font-size: 20px;
    margin-bottom: 8px;
}

.feature-item span {
    font-size: 14px;
    color: var(--light-2);
}

/* 暗色模式优化 */
@media (prefers-color-scheme: dark) {
    body {
        background: var(--dark-1);
    }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
    .nav-item.active {
        background: rgba(99, 102, 241, 0.2);
    }

    .btn-primary {
        background: var(--primary-dark);
    }

    .message.user .message-content {
        background: var(--primary-dark);
    }

    .execution-header {
        background: rgba(99, 102, 241, 0.2);
    }
}

/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* 打印样式 */
@media print {

    .mobile-header,
    .mobile-bottom-nav,
    .input-container,
    .header-actions {
        display: none !important;
    }

    .app-container {
        flex-direction: column;
        padding: 0;
    }

    .sidebar {
        position: static;
        width: 100%;
        height: auto;
    }

    .main-content {
        width: 100%;
        margin-left: 0;
    }

    body {
        background: white;
        color: black;
    }

    .message-content {
        background: #f5f5f5 !important;
        color: black !important;
        border: 1px solid #ddd;
    }
}

/* 可访问性改进 */
@media (prefers-reduced-transparency: reduce) {

    .sidebar,
    .message-content,
    .tool-card {
        background: var(--dark-1);
    }
}

/* 焦点可见性改进 */
.btn:focus-visible,
.action-btn:focus-visible,
.send-btn:focus-visible,
.tool-button:focus-visible,
.copy-btn:focus-visible,
.code-copy-btn:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}

.input-field:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 0;
}

/* 登录/注册模态框样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
    backdrop-filter: blur(4px);
}

.modal-content {
    background: var(--dark-2);
    border-radius: var(--radius);
    width: 90%;
    max-width: 450px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: var(--shadow);
    animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid var(--dark-3);
}

.modal-header h2 {
    margin: 0;
    font-size: 24px;
    color: var(--light-1);
}

.modal-close {
    background: none;
    border: none;
    color: var(--light-3);
    font-size: 24px;
    cursor: pointer;
    padding: 5px;
    transition: var(--transition);
}

.modal-close:hover {
    color: var(--light-1);
}

.modal-body {
    padding: 20px;
}

.auth-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--dark-3);
}

.auth-tab {
    background: none;
    border: none;
    padding: 12px 20px;
    color: var(--light-3);
    cursor: pointer;
    font-size: 16px;
    border-bottom: 2px solid transparent;
    transition: var(--transition);
}

.auth-tab.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}

.auth-tab:hover {
    color: var(--light-1);
}

.auth-form {
    margin-top: 20px;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: var(--light-2);
    font-size: 14px;
    font-weight: 500;
}

.form-group input {
    width: 100%;
    padding: 12px;
    background: var(--dark-1);
    border: 1px solid var(--dark-3);
    border-radius: 8px;
    color: var(--light-1);
    font-size: 16px;
    transition: var(--transition);
}

.form-group input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.btn-block {
    width: 100%;
    margin-top: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.error-message {
    margin-top: 15px;
    padding: 12px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid var(--danger);
    border-radius: 8px;
    color: var(--danger);
    font-size: 14px;
}

/* 用户信息显示 */
.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-right: 15px;
}

.user-name {
    color: var(--light-2);
    font-size: 14px;
}

.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
}

/* 对话历史样式增强 */
.history-section .nav-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.refresh-history-btn {
    background: none;
    border: none;
    color: var(--light-3);
    cursor: pointer;
    padding: 5px;
    border-radius: 4px;
    transition: var(--transition);
}

.refresh-history-btn:hover {
    color: var(--primary);
    background: rgba(99, 102, 241, 0.1);
}

.history-item {
    position: relative;
    padding: 12px;
    cursor: pointer;
    border-bottom: 1px solid var(--dark-3);
    transition: var(--transition);
    border-radius: 8px;
    margin-bottom: 4px;
}

.history-item:hover {
    background: var(--dark-3);
}

.history-item.active {
    background: rgba(99, 102, 241, 0.2);
    border-left: 3px solid var(--primary);
}

.history-item-content {
    flex: 1;
}

.history-title {
    font-size: 14px;
    color: var(--light-1);
    margin-bottom: 6px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.history-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: var(--light-3);
}

.history-count {
    font-size: 11px;
}

.history-delete-btn {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--light-3);
    cursor: pointer;
    padding: 5px;
    border-radius: 4px;
    opacity: 0;
    transition: var(--transition);
}

.history-item:hover .history-delete-btn {
    opacity: 1;
}

.history-delete-btn:hover {
    color: var(--danger);
    background: rgba(239, 68, 68, 0.1);
}

.no-history {
    padding: 20px;
    text-align: center;
    color: var(--light-3);
    font-size: 14px;
}

/* 浅色主题下的模态框 */
[data-theme="light"] .modal-content {
    background: var(--dark-2);
}

[data-theme="light"] .modal-header {
    border-bottom-color: var(--dark-3);
}

[data-theme="light"] .auth-tabs {
    border-bottom-color: var(--dark-3);
}

[data-theme="light"] .form-group input {
    background: var(--dark-1);
    border-color: var(--dark-3);
    color: var(--light-1);
}

[data-theme="light"] .history-item.active {
    background: rgba(99, 102, 241, 0.1);
}

/* Python爬虫界面样式 */
.crawler-container {
    padding: 20px;
    width: 100%;
    margin: 0 auto;
    height: calc(100vh - 80px);
    overflow-y: auto;
    overflow-x: hidden;
    /* 禁止横向滚动 */
    box-sizing: border-box;
    /* 确保padding包含在宽度内 */
}

.crawler-header {
    text-align: center;
    margin-bottom: 30px;
}

.crawler-header h2 {
    color: var(--primary);
    font-size: 28px;
    margin-bottom: 10px;
}

.crawler-header p {
    color: var(--light-2);
    font-size: 16px;
}

.crawler-controls {
    background: var(--dark-2);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 30px;
    max-width: 100%;
    box-sizing: border-box;
}

.url-input-group {
    display: flex;
    gap: 12px;
    align-items: flex-end;
    flex-wrap: wrap;
    /* 允许换行 */
}

.url-input-group label {
    color: var(--light-1);
    font-weight: 500;
    margin-bottom: 8px;
    display: block;
    width: 100%;
    /* 标签单独一行 */
}

.url-input {
    flex: 1;
    min-width: 300px;
    /* 最小宽度 */
    padding: 12px 16px;
    background: var(--dark-1);
    border: 1px solid var(--dark-3);
    border-radius: 8px;
    color: var(--light-1);
    font-size: 16px;
    transition: var(--transition);
    box-sizing: border-box;
    max-width: 100%;
}

.url-input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.crawler-button {
    padding: 12px 24px;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    /* 按钮文字不换行 */
}

.crawler-button:hover:not(:disabled) {
    background: var(--primary-dark);
    transform: translateY(-1px);
}

.crawler-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.crawler-results {
    background: var(--dark-2);
    border-radius: 12px;
    padding: 0;
    margin-bottom: 30px;
    display: none;
    max-width: 100%;
    box-sizing: border-box;
    overflow-y: auto;
}

.results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid var(--dark-3);
    flex-wrap: wrap;
    /* 允许标题和按钮换行 */
    gap: 16px;
}

.results-header h3 {
    color: var(--light-1);
    font-size: 20px;
    margin: 0;
    flex: 1;
    min-width: 200px;
}

.result-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    /* 按钮换行 */
}

.result-content {
    padding: 24px;
    max-width: 100%;
    box-sizing: border-box;
}

.url-info {
    margin-bottom: 20px;
    padding: 12px;
    background: var(--dark-1);
    border-radius: 6px;
    border-left: 4px solid var(--primary);
    word-break: break-all;
    /* URL长时自动换行 */
    overflow-wrap: break-word;
}

.url-info strong {
    color: var(--light-1);
}

.markdown-preview h4 {
    color: var(--light-1);
    margin-bottom: 16px;
}

.preview-container {
    background: var(--dark-1);
    border-radius: 8px;
    padding: 0;
    overflow: hidden;
    max-width: 100%;
}

.preview-container pre {
    margin: 0;
    padding: 16px;
    max-height: 400px;
    overflow-y: auto;
    overflow-x: auto;
    /* 代码区域允许横向滚动 */
    white-space: pre-wrap;
    /* 关键：长文本自动换行 */
    word-wrap: break-word;
    word-break: break-all;
}

.preview-container code {
    font-family: 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.4;
    white-space: pre-wrap;
    /* 关键：代码自动换行 */
    word-wrap: break-word;
    word-break: break-all;
    display: block;
    max-width: 100%;
}

.crawler-info {
    background: var(--dark-2);
    border-radius: 12px;
    padding: 24px;
    max-width: 100%;
    box-sizing: border-box;
}

.info-card h4 {
    color: var(--light-1);
    margin-bottom: 16px;
    font-size: 18px;
}

.info-card ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.info-card li {
    padding: 8px 0;
    color: var(--light-2);
    position: relative;
    padding-left: 24px;
    word-break: break-word;
    /* 列表项文字换行 */
}

.info-card li:before {
    content: "•";
    color: var(--primary);
    position: absolute;
    left: 0;
    font-size: 18px;
}

/* 修复长文本显示的特殊类 */
.long-text-container {
    max-width: 100%;
    overflow-x: auto;
    word-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
}

/* 移动端适配 */
@media (max-width: 768px) {
    .crawler-container {
        padding: 16px;
        height: calc(100vh - 60px);
    }

    .url-input-group {
        flex-direction: column;
        align-items: stretch;
    }

    .url-input {
        min-width: auto;
        /* 移动端取消最小宽度 */
        width: 100%;
    }

    .results-header {
        flex-direction: column;
        gap: 16px;
        align-items: flex-start;
    }

    .result-actions {
        width: 100%;
        justify-content: flex-end;
    }

    .preview-container pre,
    .preview-container code {
        font-size: 12px;
        /* 移动端字体稍小 */
    }
}

/* 浅色主题适配 */
[data-theme="light"] .crawler-controls,
[data-theme="light"] .crawler-results,
[data-theme="light"] .crawler-info {
    background: var(--dark-2);
}

[data-theme="light"] .url-input,
[data-theme="light"] .preview-container,
[data-theme="light"] .url-info {
    background: var(--dark-1);
}

.user-uploaded-image,
.handbook-image {
    max-width: 100%;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.user-uploaded-image img,
.handbook-image img {
    max-width: 100%;
    display: block;
}

.image-caption {
    padding: 8px;
    background: #f5f5f5;
    font-size: 12px;
    color: #666;
    text-align: center;
}

.image-preview-container {
    margin-top: 10px;
    border: 2px dashed #ddd;
    border-radius: 8px;
    padding: 10px;
    background: #f9f9f9;
}

.preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-weight: 500;
}

.remove-preview-btn {
    background: #ff4444;
    color: white;
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

#previewImage {
    max-width: 100%;
    max-height: 200px;
    border-radius: 4px;
}

.image-btn {
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-btn:hover {
    background: #45a049;
}

/* ==================== 文档查询样式 ==================== */

.documentation-container {
    padding: 20px;
    height: calc(100vh - 80px);
    overflow-y: auto;
    width: 100%;
}

.documentation-header {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--dark-3);
}

.documentation-header h2 {
    color: var(--primary);
    font-size: 28px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.documentation-header p {
    color: var(--light-2);
    font-size: 16px;
    margin-bottom: 20px;
}

.documentation-search {
    display: flex;
    gap: 12px;
    max-width: 600px;
}

.documentation-search input {
    flex: 1;
    padding: 12px 16px;
    background: var(--dark-1);
    border: 1px solid var(--dark-3);
    border-radius: 8px;
    color: var(--light-1);
    font-size: 14px;
    transition: var(--transition);
}

.documentation-search input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-light);
}

.documentation-search button {
    padding: 12px 24px;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
}

.documentation-search button:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
}

.documentation-content {
    display: flex;
    gap: 20px;
    min-height: 600px;
    height: calc(100vh - 200px);
    background: var(--dark-2);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--dark-3);
}

.doc-sidebar {
    width: 320px;
    min-width: 320px;
    border-right: 1px solid var(--dark-3);
    background: var(--dark-2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.doc-sidebar h3 {
    padding: 20px;
    margin: 0;
    color: var(--light-1);
    font-size: 18px;
    font-weight: 600;
    border-bottom: 1px solid var(--dark-3);
    display: flex;
    align-items: center;
    gap: 10px;
}

.doc-list {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}

.loading-docs {
    text-align: center;
    padding: 40px 20px;
    color: var(--light-3);
    font-size: 14px;
}

.no-docs {
    text-align: center;
    padding: 40px 20px;
    color: var(--light-3);
    font-size: 14px;
}

.doc-directory {
    margin-bottom: 24px;
}

.dir-header {
    padding: 12px 16px;
    background: var(--dark-3);
    border-radius: 8px;
    margin-bottom: 12px;
    color: var(--light-2);
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition);
}

.dir-header:hover {
    background: var(--dark-4);
    color: var(--light-1);
}

.dir-files {
    padding-left: 20px;
}

.doc-item {
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: var(--transition);
    border: 1px solid transparent;
    background: var(--dark-1);
    display: flex;
    align-items: center;
}

.doc-item:hover {
    background: var(--dark-3);
    border-color: var(--primary);
}

.doc-item.active {
    background: var(--primary-light);
    border-color: var(--primary);
}

.doc-item-icon {
    width: 36px;
    height: 36px;
    min-width: 36px;
    border-radius: 8px;
    background: rgba(99, 102, 241, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    margin-right: 12px;
}

.doc-item-content {
    flex: 1;
    min-width: 0;
}

.doc-item-name {
    font-weight: 500;
    margin-bottom: 4px;
    color: var(--light-1);
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.has-images {
    color: var(--secondary);
    font-size: 12px;
    flex-shrink: 0;
}

.doc-item-meta {
    display: flex;
    gap: 10px;
    font-size: 12px;
    color: var(--light-3);
}

.doc-item-size {
    background: rgba(156, 163, 175, 0.1);
    padding: 2px 6px;
    border-radius: 4px;
}

.doc-item-path {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 修复文档内容宽度过长问题 */
.doc-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    width: 100%;
}

.doc-viewer {
    flex: 1;
    padding: 0;
    width: 100%;
    overflow-y: auto;
    overflow-x: auto; /* 添加横向滚动 */
}

.markdown-content {
    padding: 40px;
    max-width: 100%;
    margin: 0 auto;
    color: var(--light-1);
    box-sizing: border-box;
    min-width: min-content; /* 确保内容不被压缩 */
}

.doc-body {
    line-height: 1.8;
    font-size: 16px;
    word-wrap: break-word;
    overflow-wrap: break-word;
    max-width: 100%;
    overflow-x: auto; /* 添加横向滚动 */
    width: 100%;
}

/* 修复表格溢出问题 */
.doc-body table {
    width: 100%;
    margin: 20px 0;
    border-collapse: collapse;
    background: var(--dark-1);
    border-radius: 8px;
    border: 1px solid var(--dark-3);
    max-width: 100%;
    overflow-x: auto;
    display: block;
    table-layout: fixed; /* 固定表格布局 */
}

.doc-body th,
.doc-body td {
    padding: 12px 16px;
    text-align: left;
    border: 1px solid var(--dark-3);
    color: var(--light-2);
    word-break: break-word; /* 单元格内容自动换行 */
    max-width: 400px; /* 限制最大宽度 */
}

/* 修复代码块溢出 */
.doc-body pre {
    margin: 20px 0;
    border-radius: 8px;
    max-width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    background: var(--dark-1) !important;
    border: 1px solid var(--dark-3);
    word-break: break-all; /* 代码自动换行 */
}

.doc-body pre code {
    display: block;
    padding: 20px;
    overflow-x: auto;
    font-size: 14px;
    line-height: 1.6;
    background: transparent !important;
    white-space: pre-wrap; /* 关键：代码自动换行 */
    word-wrap: break-word;
}

.welcome-doc {
    text-align: center;
    padding: 60px 20px;
    max-width: 600px;
    margin: 0 auto;
}

.doc-icon {
    width: 80px;
    height: 80px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    color: var(--primary);
    font-size: 32px;
}

.doc-title {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 12px;
    color: var(--light-1);
}

.doc-subtitle {
    color: var(--light-3);
    margin-bottom: 30px;
    font-size: 16px;
    line-height: 1.6;
}

.doc-stats {
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-top: 30px;
}

.stat-item {
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--light-3);
    font-size: 14px;
}

.stat-item i {
    color: var(--primary);
    font-size: 18px;
}

.stat-item span {
    font-weight: 600;
    color: var(--light-1);
}

.loading-content {
    text-align: center;
    padding: 60px 20px;
    color: var(--light-3);
    font-size: 16px;
}

.error-message {
    background: var(--danger-light);
    border: 1px solid var(--danger);
    border-radius: 8px;
    padding: 20px;
    color: var(--danger);
    margin: 20px;
    text-align: center;
}

.error-message h3 {
    margin-top: 0;
    color: var(--danger);
}

.doc-header {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--dark-3);
}

.doc-header h1 {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 12px;
    color: var(--light-1);
}

.doc-path-info {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--light-3);
    font-size: 14px;
    background: var(--dark-1);
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid var(--dark-3);
}

.doc-body h1 {
    font-size: 28px;
    margin: 32px 0 16px 0;
    color: var(--light-1);
    border-bottom: 2px solid var(--primary);
    padding-bottom: 8px;
}

.doc-body h2 {
    font-size: 24px;
    margin: 28px 0 14px 0;
    color: var(--light-1);
}

.doc-body h3 {
    font-size: 20px;
    margin: 24px 0 12px 0;
    color: var(--light-1);
}

.doc-body h4 {
    font-size: 18px;
    margin: 20px 0 10px 0;
    color: var(--light-1);
}

.doc-body p {
    margin: 16px 0;
    color: var(--light-2);
}

.doc-body strong {
    color: var(--light-1);
    font-weight: 600;
}

.doc-body em {
    color: var(--light-2);
    font-style: italic;
}

.doc-body ul,
.doc-body ol {
    margin: 16px 0;
    padding-left: 24px;
}

.doc-body li {
    margin: 8px 0;
    color: var(--light-2);
}

.doc-body blockquote {
    margin: 20px 0;
    padding: 12px 20px;
    border-left: 4px solid var(--primary);
    background: var(--dark-1);
    border-radius: 6px;
    color: var(--light-2);
    font-style: italic;
}

.doc-body code:not(pre code) {
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    background: var(--dark-3);
    color: var(--light-1);
    padding: 2px 6px;
    border-radius: 4px;
    margin: 0 2px;
    white-space: normal;
    word-break: break-word;
}

.doc-body a {
    color: var(--primary);
    text-decoration: none;
    transition: var(--transition);
}

.doc-body a:hover {
    color: var(--primary-dark);
    text-decoration: underline;
}

.doc-body img {
    max-width: 100%;
    height: auto;
}

.doc-images {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid var(--dark-3);
}

.doc-images h3 {
    font-size: 20px;
    margin-bottom: 20px;
    color: var(--light-1);
    display: flex;
    align-items: center;
    gap: 10px;
}

.image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
}

.gallery-item {
    background: var(--dark-1);
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--dark-3);
    transition: var(--transition);
}

.gallery-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
    border-color: var(--primary);
}

.gallery-item img {
    width: 100%;
    height: 150px;
    object-fit: cover;
    display: block;
    cursor: pointer;
    transition: var(--transition);
}

.gallery-item:hover img {
    transform: scale(1.05);
}

.image-caption {
    padding: 12px;
    font-size: 12px;
    color: var(--light-3);
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 搜索相关样式 */
.search-results {
    padding: 20px;
}

.results-header {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--dark-3);
}

.results-header h2 {
    color: var(--light-1);
    font-size: 24px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.results-stats {
    color: var(--light-3);
    font-size: 14px;
}

.search-result-item {
    background: var(--dark-1);
    border: 1px solid var(--dark-3);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    cursor: pointer;
    transition: var(--transition);
}

.search-result-item:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}

.result-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.result-index {
    background: var(--primary);
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
    flex-shrink: 0;
}

.result-file {
    flex: 1;
    font-weight: 600;
    color: var(--light-1);
    font-size: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.view-source-btn {
    flex-shrink: 0;
    padding: 6px 12px;
    background: transparent;
    border: 1px solid var(--dark-3);
    color: var(--light-2);
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 6px;
}

.view-source-btn:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}

.result-content {
    color: var(--light-2);
    line-height: 1.6;
    font-size: 14px;
    max-height: 600px;
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
}

.result-content::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 20px;
    background: linear-gradient(to bottom, transparent, var(--dark-1));
}

.no-results {
    text-align: center;
    padding: 60px 20px;
    color: var(--light-3);
}

.no-results i {
    font-size: 48px;
    margin-bottom: 20px;
    color: var(--light-4);
}

.no-results h3 {
    font-size: 20px;
    margin-bottom: 12px;
    color: var(--light-1);
}

.no-results p {
    color: var(--light-3);
    max-width: 400px;
    margin: 0 auto;
    line-height: 1.6;
}

/* 浅色主题适配 */
[data-theme="light"] .documentation-content {
    background: var(--dark-2);
    border-color: var(--dark-3);
}

[data-theme="light"] .doc-sidebar {
    background: var(--dark-2);
    border-right-color: var(--dark-3);
}

[data-theme="light"] .doc-sidebar h3 {
    color: var(--light-1);
    border-bottom-color: var(--dark-3);
}

[data-theme="light"] .doc-item {
    background: var(--dark-1);
}

[data-theme="light"] .doc-item:hover {
    background: var(--dark-3);
}

[data-theme="light"] .doc-item.active {
    background: var(--primary-light);
}

[data-theme="light"] .doc-path {
    background: var(--dark-1);
    border-color: var(--dark-3);
    color: var(--light-3);
}

[data-theme="light"] .markdown-content {
    color: var(--light-1);
}

[data-theme="light"] .doc-body h1,
[data-theme="light"] .doc-body h2,
[data-theme="light"] .doc-body h3,
[data-theme="light"] .doc-body h4 {
    color: var(--light-1);
}

[data-theme="light"] .doc-body p {
    color: var(--light-2);
}

[data-theme="light"] .doc-body li {
    color: var(--light-2);
}

[data-theme="light"] .search-result-item {
    background: var(--dark-1);
    border-color: var(--dark-3);
}

[data-theme="light"] .result-content::after {
    background: linear-gradient(to bottom, transparent, var(--dark-1));
}

/* LaTeX 数学公式样式 */
.katex {
    font-size: 1.1em !important;
    text-rendering: auto;
}

.katex-display {
    margin: 1.5em 0 !important;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 10px 0;
}

.katex-display > .katex {
    max-width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
}

/* 行内公式 */
.katex-inline {
    background: var(--dark-3);
    padding: 2px 6px;
    border-radius: 4px;
    margin: 0 2px;
}

/* 块级公式 */
.katex-block {
    background: var(--dark-1);
    padding: 15px;
    border-radius: 8px;
    border: 1px solid var(--dark-3);
    margin: 20px 0;
    overflow-x: auto;
}

/* 移动端公式优化 */
@media (max-width: 768px) {
    .katex {
        font-size: 1em !important;
    }
    
    .katex-display {
        margin: 1em 0 !important;
        overflow-x: auto;
    }
    
    .katex-block {
        padding: 10px;
    }
}

/* 移动端适配 */
@media (max-width: 768px) {
    .documentation-content {
        flex-direction: column;
        height: auto;
    }
    
    .doc-sidebar {
        width: 100%;
        min-width: auto;
        border-right: none;
        border-bottom: 1px solid var(--dark-3);
    }
    
    .doc-list {
        max-height: 300px;
    }
    
    .markdown-content {
        padding: 20px;
    }
    
    .doc-body {
        font-size: 14px;
    }
    
    .doc-body h1 {
        font-size: 24px;
    }
    
    .doc-body h2 {
        font-size: 20px;
    }
    
    .doc-body h3 {
        font-size: 18px;
    }
    
    .doc-body pre code {
        font-size: 12px;
        padding: 12px;
    }
    
    .doc-body table {
        font-size: 12px;
    }
    
    .doc-body th,
    .doc-body td {
        padding: 8px 12px;
        max-width: 200px; /* 移动端更小的最大宽度 */
    }
    
    .image-gallery {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
}

/* ==================== 图像查看模态框样式 ==================== */

.image-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(15, 23, 42, 0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 20000;
    backdrop-filter: blur(8px);
    animation: fadeIn 0.3s ease;
}

.image-modal-content {
    background: var(--dark-2);
    border-radius: var(--radius);
    width: 90%;
    max-width: 800px;
    max-height: 90vh;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    animation: modalSlideIn 0.3s ease;
}

.image-modal-content .modal-header {
    padding: 20px;
    border-bottom: 1px solid var(--dark-3);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.image-modal-content .modal-header h3 {
    margin: 0;
    color: var(--light-1);
    font-size: 20px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: 20px;
}

.image-modal-content .modal-body {
    padding: 20px;
    text-align: center;
    max-height: 70vh;
    overflow-y: auto;
}

.image-modal-content .modal-body img {
    max-width: 100%;
    max-height: 60vh;
    border-radius: 8px;
    object-fit: contain;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.image-modal-content .modal-footer {
    padding: 20px;
    border-top: 1px solid var(--dark-3);
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    background: var(--dark-2);
}

/* 图像上传区域样式补充 */
.upload-area {
    position: relative;
    cursor: pointer;
}

.upload-area input[type="file"] {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    opacity: 0;
    cursor: pointer;
}

/* Markdown图片样式 */
.markdown-image-container,
.output-image-container {
    margin: 20px 0;
    text-align: center;
}

.markdown-image,
.output-image {
    max-width: 100%;
    max-height: 400px;
    border-radius: 8px;
    cursor: pointer;
    transition: var(--transition);
    border: 1px solid var(--dark-3);
    background: var(--dark-1);
    padding: 4px;
}

.markdown-image:hover,
.output-image:hover {
    transform: scale(1.01);
    box-shadow: var(--shadow);
    border-color: var(--primary);
}

/* 上传按钮状态 */
#confirmUpload:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

#confirmUpload:disabled:hover {
    background: var(--primary);
    transform: none;
}

/* 输入框占位符样式 */
.tool-input::placeholder,
.tool-input-text::placeholder,
.url-input::placeholder,
#docSearchInput::placeholder,
#questionInput::placeholder {
    color: var(--light-4);
    opacity: 0.7;
}

/* 按钮禁用状态 */
button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
}

button:disabled:hover {
    background: inherit !important;
    color: inherit !important;
    border-color: inherit !important;
}

/* 用户信息显示样式补充 */
#userInfoHeader {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-right: 15px;
}

/* 历史记录项元数据样式补充 */
.history-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: var(--light-3);
}

.history-count {
    background: rgba(156, 163, 175, 0.1);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 11px;
}

/* 代码块滚动条优化 */
pre::-webkit-scrollbar {
    height: 8px;
}

pre::-webkit-scrollbar-track {
    background: var(--dark-3);
    border-radius: 4px;
}

pre::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 4px;
}

/* 暗色主题优化 */
[data-theme="dark"] .hljs {
    background: #282c34 !important;
}

[data-theme="dark"] .hljs-keyword {
    color: #c678dd !important;
}

[data-theme="dark"] .hljs-string {
    color: #98c379 !important;
}

[data-theme="dark"] .hljs-number {
    color: #d19a66 !important;
}

[data-theme="dark"] .hljs-comment {
    color: #5c6370 !important;
}

/* 响应式优化补充 */
@media (max-width: 480px) {
    .documentation-search {
        flex-direction: column;
    }
    
    .documentation-search button {
        width: 100%;
        justify-content: center;
    }
    
    .mobile-bottom-nav .nav-item {
        font-size: 10px;
        padding: 6px 0;
    }
    
    .mobile-bottom-nav .nav-item i {
        font-size: 16px;
    }
}

/* 打印优化 */
@media print {
    .documentation-content {
        display: block;
        height: auto;
    }
    
    .doc-sidebar {
        display: none;
    }
    
    .doc-toolbar {
        display: none;
    }
    
    .markdown-content {
        padding: 0;
    }
}

/* 可访问性改进 */
.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* 加载动画 */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.fa-spin {
    animation: spin 1s linear infinite;
}

/* 过渡动画优化 */
.fade-enter {
    opacity: 0;
    transform: translateY(10px);
}

.fade-enter-active {
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.3s, transform 0.3s;
}

.fade-exit {
    opacity: 1;
    transform: translateY(0);
}

.fade-exit-active {
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.3s, transform 0.3s;
}
