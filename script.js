// 初始化代码高亮
hljs.highlightAll();

// DOM元素
const questionInput = document.getElementById('questionInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const clearChatButton = document.getElementById('clearChat');
const newChatButton = document.getElementById('newChat');
const exampleQuestionsButton = document.getElementById('exampleQuestions');
const syntaxCheckButton = document.getElementById('syntaxCheck');
const insertCodeButton = document.getElementById('insertCode');
const executeCodeButton = document.getElementById('executeCode');

// 语音识别相关元素
const voiceButton = document.getElementById('voiceButton');
const voiceInputBtn = document.getElementById('voiceInput');
const voiceStatus = document.getElementById('voiceStatus');

// 主题切换元素
const themeToggle = document.getElementById('themeToggle');
const themeText = document.getElementById('themeText');
const themeIcon = themeToggle.querySelector('i');

// 工具按钮
const syntaxCheckBtn = document.getElementById('syntaxCheckBtn');
const executeCodeBtn = document.getElementById('executeCodeBtn');
const analyzeCodeBtn = document.getElementById('analyzeCodeBtn');
const docSearchBtn = document.getElementById('docSearchBtn');

// 工具输入
const syntaxInput = document.getElementById('syntaxInput');
const executeInput = document.getElementById('executeInput');
const analyzeInput = document.getElementById('analyzeInput');
const docInput = document.getElementById('docInput');

// 移动端元素
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebar = document.getElementById('sidebar');
const mobileNewChat = document.getElementById('mobileNewChat');
const mobileInsertCode = document.getElementById('mobileInsertCode');
const mobileExampleQuestions = document.getElementById('mobileExampleQuestions');

// 语音识别相关变量
let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];
let audioStream = null;

// 复制功能
function initCopyButtons() {
    document.addEventListener('click', function(e) {
        if (e.target.closest('.copy-btn')) {
            const copyBtn = e.target.closest('.copy-btn');
            const messageContent = copyBtn.closest('.message-content');
            const messageText = messageContent.querySelector('.message-text');
            copyToClipboard(messageText.innerText, copyBtn);
        }
        
        if (e.target.closest('.code-copy-btn')) {
            const codeCopyBtn = e.target.closest('.code-copy-btn');
            const codeBlock = codeCopyBtn.closest('.code-block-wrapper').querySelector('code');
            copyToClipboard(codeBlock.innerText, codeCopyBtn);
        }
    });
}

function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = button.innerHTML;
        const originalText = button.querySelector('.btn-text');
        const originalBtnText = originalText ? originalText.textContent : '';
        
        button.classList.add('copied');
        if (originalText) {
            originalText.textContent = '已复制';
        } else {
            button.innerHTML = '<i class="fas fa-check"></i><span class="btn-text">已复制</span>';
        }
        
        setTimeout(() => {
            button.classList.remove('copied');
            if (originalText) {
                originalText.textContent = originalBtnText;
            } else {
                button.innerHTML = originalHTML;
            }
        }, 2000);
    }).catch(err => {
        console.error('复制失败:', err);
        alert('复制失败，请手动选择文本复制');
    });
}

function addCopyButtonToCodeBlocks() {
    document.querySelectorAll('pre code').forEach(codeBlock => {
        const preElement = codeBlock.closest('pre');
        if (!preElement) return;
        
        if (preElement.parentElement.classList.contains('code-block-wrapper')) {
            return;
        }
        
        const wrapper = document.createElement('div');
        wrapper.className = 'code-block-wrapper';
        
        const header = document.createElement('div');
        header.className = 'code-block-header';
        
        const copyBtn = document.createElement('button');
        copyBtn.className = 'code-copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i><span class="btn-text">复制代码</span>';
        copyBtn.title = '复制代码';
        
        header.appendChild(copyBtn);
        wrapper.appendChild(header);
        preElement.parentNode.insertBefore(wrapper, preElement);
        wrapper.appendChild(preElement);
    });
}

// 主题切换功能
function initTheme() {
    const savedTheme = localStorage.getItem('pyassistant-theme') || 'dark';
    setTheme(savedTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('pyassistant-theme', theme);
    
    if (theme === 'light') {
        themeText.textContent = '深色主题';
        themeIcon.className = 'fas fa-moon';
    } else {
        themeText.textContent = '浅色主题';
        themeIcon.className = 'fas fa-sun';
    }
    
    setTimeout(() => {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }, 100);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

// 添加主题切换事件监听
themeToggle.addEventListener('click', toggleTheme);

// 标签切换
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function () {
        const tab = this.getAttribute('data-tab');

        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        this.classList.add('active');

        document.getElementById('chatTab').style.display = tab === 'chat' ? 'flex' : 'none';
        document.getElementById('toolsTab').style.display = tab === 'tools' ? 'block' : 'none';
        document.getElementById('crawlerTab').style.display = tab === 'crawler' ? 'block' : 'none';

        if (window.innerWidth <= 768) {
            sidebar.classList.remove('active');
        }
    });
});

// 移动端底部导航
document.querySelectorAll('.mobile-bottom-nav .nav-item').forEach(item => {
    item.addEventListener('click', function() {
        const tab = this.getAttribute('data-tab');
        
        if (tab) {
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            document.querySelectorAll(`.nav-item[data-tab="${tab}"]`).forEach(i => i.classList.add('active'));
            
            document.getElementById('chatTab').style.display = tab === 'chat' ? 'flex' : 'none';
            document.getElementById('toolsTab').style.display = tab === 'tools' ? 'block' : 'none';
            document.getElementById('crawlerTab').style.display = tab === 'crawler' ? 'block' : 'none';
            
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        }
    });
});

// 移动端菜单切换
mobileMenuToggle.addEventListener('click', function() {
    sidebar.classList.toggle('active');
});

// 自动调整文本区域高度
questionInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// 发送消息
sendButton.addEventListener('click', sendMessage);
questionInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// 清除对话
clearChatButton.addEventListener('click', function () {
    if (confirm('确定要清空对话历史吗？')) {
        fetch('/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    chatMessages.innerHTML = `
                            <div class="welcome-message">
                                <div class="welcome-icon">
                                    <i class="fas fa-robot"></i>
                                </div>
                                <div class="welcome-title">欢迎使用 Python 编程助手</div>
                                <div class="welcome-subtitle">我可以帮助您解决各种 Python 编程问题</div>
                                <div class="feature-list">
                                    <div class="feature-item">
                                        <i class="fas fa-code"></i>
                                        <span>代码调试</span>
                                    </div>
                                    <div class="feature-item">
                                        <i class="fas fa-book"></i>
                                        <span>文档查询</span>
                                    </div>
                                    <div class="feature-item">
                                        <i class="fas fa-bug"></i>
                                        <span>错误修复</span>
                                    </div>
                                    <div class="feature-item">
                                        <i class="fas fa-rocket"></i>
                                        <span>性能优化</span>
                                    </div>
                                    <div class="feature-item">
                                        <i class="fas fa-microphone"></i>
                                        <span>语音输入</span>
                                    </div>
                                </div>
                            </div>
                        `;
                }
            })
            .catch(error => {
                console.error('清除对话错误:', error);
            });
    }
});

// 新建对话
newChatButton.addEventListener('click', function () {
    if (!isLoggedIn) {
        showLoginModal();
        return;
    }

    if (confirm('确定要开始新的对话吗？当前对话将被保存到历史记录中。')) {
        fetch('/new_conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 清空聊天界面
                    chatMessages.innerHTML = `
                        <div class="welcome-message">
                            <div class="welcome-icon">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div class="welcome-title">欢迎使用 Python 编程助手</div>
                            <div class="welcome-subtitle">我可以帮助您解决各种 Python 编程问题</div>
                        </div>
                    `;
                    // 重新加载历史列表
                    loadChatHistory();
                } else {
                    alert('新建对话失败: ' + (data.error || '未知错误'));
                }
            })
            .catch(error => {
                console.error('新建对话错误:', error);
                alert('新建对话失败，请重试');
            });
    }
});

// 移动端新建对话
mobileNewChat.addEventListener('click', function() {
    if (!isLoggedIn) {
        showLoginModal();
        return;
    }

    if (confirm('确定要开始新的对话吗？当前对话将被保存到历史记录中。')) {
        fetch('/new_conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 清空聊天界面
                chatMessages.innerHTML = `
                    <div class="welcome-message">
                        <div class="welcome-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="welcome-title">欢迎使用 Python 编程助手</div>
                        <div class="welcome-subtitle">我可以帮助您解决各种 Python 编程问题</div>
                    </div>
                `;
                // 重新加载历史列表
                loadChatHistory();
            } else {
                alert('新建对话失败: ' + (data.error || '未知错误'));
            }
        })
        .catch(error => {
            console.error('新建对话错误:', error);
            alert('新建对话失败，请重试');
        });
    }
});

// 示例问题
exampleQuestionsButton.addEventListener('click', function () {
    const examples = [
        "解释Python中的装饰器并给出实际应用示例",
        "什么是列表推导式？写一个复杂的例子",
        "如何用Python处理JSON数据的序列化和反序列化？",
        "解释Python的生成器和迭代器的区别及应用场景",
        "如何在Python中实现异步编程？给出async/await的例子",
        "Python的类型注解有什么好处？写一个带类型提示的函数",
        "解释Python的上下文管理器，并自定义一个",
        "Python的内存管理机制是怎样的？",
        "如何使用Python进行单元测试？",
        "Python的GIL是什么？它对多线程有什么影响？"
    ];

    const randomExample = examples[Math.floor(Math.random() * examples.length)];
    questionInput.value = randomExample;
    questionInput.focus();
    questionInput.style.height = 'auto';
    questionInput.style.height = (questionInput.scrollHeight) + 'px';
});

// 移动端示例问题
mobileExampleQuestions.addEventListener('click', function() {
    const examples = [
        "解释Python中的装饰器并给出实际应用示例",
        "什么是列表推导式？写一个复杂的例子",
        "如何用Python处理JSON数据的序列化和反序列化？",
        "解释Python的生成器和迭代器的区别及应用场景",
        "如何在Python中实现异步编程？给出async/await的例子",
        "Python的类型注解有什么好处？写一个带类型提示的函数",
        "解释Python的上下文管理器，并自定义一个",
        "Python的内存管理机制是怎样的？",
        "如何使用Python进行单元测试？",
        "Python的GIL是什么？它对多线程有什么影响？"
    ];

    const randomExample = examples[Math.floor(Math.random() * examples.length)];
    questionInput.value = randomExample;
    questionInput.focus();
    questionInput.style.height = 'auto';
    questionInput.style.height = (questionInput.scrollHeight) + 'px';

    document.querySelector('.nav-item[data-tab="chat"]').click();
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('active');
    }
});

// 插入代码模板
insertCodeButton.addEventListener('click', function () {
    const codeTemplate = `\`\`\`python
# 在这里输入您的Python代码
def example_function():
    print("Hello, World!")
    return True

result = example_function()
print(f"结果: {result}")
\`\`\``;

    if (questionInput.value) {
        questionInput.value += '\n\n' + codeTemplate;
    } else {
        questionInput.value = codeTemplate;
    }
    questionInput.focus();
    questionInput.style.height = 'auto';
    questionInput.style.height = (questionInput.scrollHeight) + 'px';
});

// 移动端插入代码
mobileInsertCode.addEventListener('click', function() {
    const codeTemplate = `\`\`\`python
# 在这里输入您的Python代码
def example_function():
    print("Hello, World!")
    return True

result = example_function()
print(f"结果: {result}")
\`\`\``;

    if (questionInput.value) {
        questionInput.value += '\n\n' + codeTemplate;
    } else {
        questionInput.value = codeTemplate;
    }
    questionInput.focus();
    questionInput.style.height = 'auto';
    questionInput.style.height = (questionInput.scrollHeight) + 'px';

    document.querySelector('.nav-item[data-tab="chat"]').click();
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('active');
    }
});

// 语法检查
syntaxCheckButton.addEventListener('click', function () {
    const code = prompt('请输入要检查的Python代码:');
    if (code) {
        checkSyntax(code);
    }
});

// 执行代码
executeCodeButton.addEventListener('click', function () {
    const code = prompt('请输入要执行的Python代码:');
    if (code) {
        executeCode(code);
    }
});

// 工具功能
syntaxCheckBtn.addEventListener('click', function () {
    const code = syntaxInput.value.trim();
    if (!code) {
        alert('请输入要检查的Python代码');
        return;
    }
    checkSyntax(code);
});

executeCodeBtn.addEventListener('click', function () {
    const code = executeInput.value.trim();
    if (!code) {
        alert('请输入要执行的Python代码');
        return;
    }
    executeCode(code);
});

analyzeCodeBtn.addEventListener('click', function () {
    const code = analyzeInput.value.trim();
    if (!code) {
        alert('请输入要分析的Python代码');
        return;
    }
    analyzeCode(code);
});

docSearchBtn.addEventListener('click', function () {
    const topic = docInput.value.trim();
    if (!topic) {
        alert('请输入要查询的主题');
        return;
    }
    getDocumentation(topic);
});

function checkSyntax(code) {
    fetch('/syntax_check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code })
    })
        .then(response => response.json())
        .then(data => {
            document.querySelector('.nav-item[data-tab="chat"]').click();

            if (data.success) {
                addMessage('system', `语法检查结果:\n${data.result}`, 'text');
            } else {
                addMessage('system', `错误: ${data.error}`, 'text');
            }

            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        })
        .catch(error => {
            addMessage('system', `网络错误: ${error}`, 'text');
        });
}

function executeCode(code) {
    fetch('/execute_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code })
    })
        .then(response => response.json())
        .then(data => {
            document.querySelector('.nav-item[data-tab="chat"]').click();

            // 解码代码中的HTML实体，确保特殊字符正常显示
            const decodedCode = decodeHtmlEntities(code);

            if (data.success) {
                const resultHtml = `
<div class="code-execution-result">
    <div class="execution-header">
        <i class="fas fa-play-circle"></i>
        <span>代码执行结果</span>
    </div>
    <div class="execution-content">
        <div class="source-code-section">
            <div class="section-title">执行的源代码：</div>
            <pre><code class="language-python">${escapeHtml(decodedCode)}</code></pre>
        </div>
        <div class="output-section">
            <div class="section-title">执行输出：</div>
            <div class="output-content">${formatOutput(data.result)}</div>
        </div>
    </div>
</div>
                `;
                addMessage('system', resultHtml, 'html');
            } else {
                const errorHtml = `
<div class="code-execution-result error">
    <div class="execution-header">
        <i class="fas fa-exclamation-circle"></i>
        <span>代码执行失败</span>
    </div>
    <div class="execution-content">
        <div class="source-code-section">
            <div class="section-title">执行的源代码：</div>
            <pre><code class="language-python">${escapeHtml(decodedCode)}</code></pre>
        </div>
        <div class="error-section">
            <div class="section-title">错误信息：</div>
            <div class="error-content">${formatOutput(data.error)}</div>
        </div>
    </div>
</div>
                `;
                addMessage('system', errorHtml, 'html');
            }

            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }

            setTimeout(() => {
                document.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
                addCopyButtonToCodeBlocks();
            }, 100);
        })
        .catch(error => {
            addMessage('system', `网络错误: ${error}`, 'text');
        });
}

function analyzeCode(code) {
    fetch('/analyze_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code })
    })
        .then(response => response.json())
        .then(data => {
            document.querySelector('.nav-item[data-tab="chat"]').click();

            if (data.success) {
                addMessage('system', `代码分析结果:\n${data.result}`, 'text');
            } else {
                addMessage('system', `错误: ${data.error}`, 'text');
            }

            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        })
        .catch(error => {
            addMessage('system', `网络错误: ${error}`, 'text');
        });
}

function getDocumentation(topic) {
    fetch('/get_documentation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic: topic })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.querySelector('.nav-item[data-tab="chat"]').click();
                addMessage('assistant', data.result, 'html');

                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('active');
                }
            } else {
                alert(`错误: ${data.error}`);
            }
        })
        .catch(error => {
            alert(`网络错误: ${error}`);
        });
}

// 辅助函数：HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 辅助函数：HTML实体解码
function decodeHtmlEntities(text) {
    const textarea = document.createElement('textarea');
    textarea.innerHTML = text;
    return textarea.value;
}

// 辅助函数：格式化输出
function formatOutput(output) {
    if (!output) return '<span class="no-output">(无输出)</span>';

    // 先解码HTML实体，确保特殊字符正常显示
    const decodedOutput = decodeHtmlEntities(output);

    // 替换换行符和制表符，但保留空格（不替换所有空格）
    return decodedOutput.replace(/\n/g, '<br>')
                 .replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
}

// 处理AI返回的HTML内容，解码HTML实体
function processAiContent(content) {
    let processedContent = decodeHtmlEntities(content);

    processedContent = processedContent.replace(/```python\s*([\s\S]*?)```/g, '<pre><code class="language-python">$1</code></pre>');
    processedContent = processedContent.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

    return processedContent;
}

function sendMessage() {
    if (!isLoggedIn) {
        showLoginModal();
        return;
    }

    const message = questionInput.value.trim();
    if (!message) {
        alert('请输入问题');
        return;
    }

    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    addMessage('user', message, 'text');
    questionInput.value = '';
    questionInput.style.height = 'auto';

    showTypingIndicator();

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message })
    })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator();

            if (data.success) {
                const processedAnswer = processAiContent(data.answer);
                addMessage('assistant', processedAnswer, 'html');
                // 重新加载历史列表以更新标题
                loadChatHistory();
            } else {
                if (data.error && data.error.includes('请先登录')) {
                    showLoginModal();
                } else {
                    addMessage('system', `错误: ${data.error}`, 'text');
                }
            }
        })
        .catch(error => {
            removeTypingIndicator();
            addMessage('system', `网络错误: ${error}`, 'text');
        });
}

function addMessage(sender, content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatarClass = sender === 'user' ? 'fa-user' :
        sender === 'assistant' ? 'fa-robot' : 'fa-info-circle';

    const now = new Date();
    const timeString = now.toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit'
    });

    let messageContent = '';
    if (type === 'html') {
        messageContent = content;
    } else {
        messageContent = content.replace(/\n/g, '<br>');
    }

    const showCopyButton = sender === 'assistant';

    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${avatarClass}"></i>
        </div>
        <div class="message-content">
            ${showCopyButton ? `
            <div class="message-header">
                <div class="message-actions">
                    <button class="copy-btn" title="复制整个回答">
                        <i class="fas fa-copy"></i>
                        <span class="btn-text">复制</span>
                    </button>
                </div>
            </div>
            ` : ''}
            <div class="message-text">${messageContent}</div>
            <div class="message-time">${timeString}</div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    setTimeout(() => {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
        addCopyButtonToCodeBlocks();
    }, 100);
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';
    typingDiv.id = 'typing-indicator';

    typingDiv.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        <div class="typing-indicator">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                    <div class="message-time">AI正在思考...</div>
                </div>
            `;

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// ==================== 语音识别功能 ====================

// 初始化语音识别
function initVoiceRecognition() {
    // 检查浏览器是否支持录音
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.warn('浏览器不支持语音录制');
        voiceButton.style.display = 'none';
        voiceInputBtn.style.display = 'none';
        if (document.getElementById('mobileVoiceInput')) {
            document.getElementById('mobileVoiceInput').style.display = 'none';
        }
        return;
    }

    // 请求麦克风权限
    navigator.mediaDevices.getUserMedia({
        audio: {
            sampleRate: 16000,
            channelCount: 1,
            echoCancellation: true,
            noiseSuppression: true
        }
    })
        .then(stream => {
            console.log('麦克风权限获取成功');
            setupMediaRecorder(stream);
        })
        .catch(err => {
            console.error('无法获取麦克风权限:', err);
            voiceButton.style.display = 'none';
            voiceInputBtn.style.display = 'none';
            if (document.getElementById('mobileVoiceInput')) {
                document.getElementById('mobileVoiceInput').style.display = 'none';
            }
            alert('无法访问麦克风，请检查浏览器权限设置');
        });
}

// 设置媒体录制器
function setupMediaRecorder(stream) {
    try {
        audioStream = stream;

        // 获取支持的MIME类型
        const options = {
            audioBitsPerSecond: 128000,
            mimeType: 'audio/webm;codecs=opus'
        };

        // 尝试创建MediaRecorder
        mediaRecorder = new MediaRecorder(stream, options);

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            sendAudioToServer(audioBlob);
            audioChunks = [];
        };

        mediaRecorder.onerror = (event) => {
            console.error('MediaRecorder错误:', event.error);
            stopRecording();
            showVoiceError('录音设备错误: ' + event.error);
        };

    } catch (error) {
        console.error('MediaRecorder设置失败:', error);
        // 尝试使用默认设置
        try {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                sendAudioToServer(audioBlob);
                audioChunks = [];
            };
        } catch (e) {
            console.error('MediaRecorder完全失败:', e);
            voiceButton.style.display = 'none';
            voiceInputBtn.style.display = 'none';
        }
    }
}

// 开始录音
function startRecording() {
    if (!mediaRecorder) {
        alert('语音录制功能初始化失败');
        return;
    }

    if (isRecording) {
        return;
    }

    try {
        audioChunks = [];
        mediaRecorder.start(100); // 每100ms收集一次数据
        isRecording = true;

        // 更新UI
        voiceButton.classList.add('recording');
        voiceButton.innerHTML = '<i class="fas fa-stop"></i>';
        voiceButton.title = '停止录音';

        voiceStatus.innerHTML = `
            <div class="voice-recording">
                <i class="fas fa-microphone recording-pulse"></i>
                <span>正在录音... 点击停止</span>
            </div>
        `;
        voiceStatus.style.display = 'block';

        // 设置最大录音时长（30秒）
        setTimeout(() => {
            if (isRecording) {
                stopRecording();
                showVoiceMessage('已达到最大录音时长（30秒）');
            }
        }, 30000);

    } catch (error) {
        console.error('开始录音失败:', error);
        showVoiceError('开始录音失败: ' + error.message);
    }
}

// 停止录音
function stopRecording() {
    if (mediaRecorder && isRecording) {
        try {
            mediaRecorder.stop();
            isRecording = false;

            // 更新UI
            voiceButton.classList.remove('recording');
            voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
            voiceButton.title = '开始录音';

            voiceStatus.innerHTML = `
                <div class="voice-recording">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span>识别中...</span>
                </div>
            `;

        } catch (error) {
            console.error('停止录音失败:', error);
            resetVoiceUI();
            showVoiceError('停止录音失败');
        }
    }
}

// 切换录音状态
function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
}

// 发送音频到服务器
function sendAudioToServer(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    fetch('/voice_recognition', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resetVoiceUI();

        if (data.success) {
            // 将识别结果填入输入框
            if (data.text && data.text.trim() !== '') {
                questionInput.value = data.text;
                questionInput.focus();
                questionInput.style.height = 'auto';
                questionInput.style.height = (questionInput.scrollHeight) + 'px';

                // 显示识别结果消息
                addMessage('system', `语音识别结果: ${data.text}`, 'text');

                // 自动切换到聊天标签
                document.querySelector('.nav-item[data-tab="chat"]').click();
            } else {
                showVoiceMessage('未能识别到有效语音内容');
            }
        } else {
            showVoiceError(`语音识别失败: ${data.error || '未知错误'}`);
        }
    })
    .catch(error => {
        console.error('语音识别网络错误:', error);
        resetVoiceUI();
        showVoiceError(`网络错误: ${error.message}`);
    });
}

// 重置语音UI状态
function resetVoiceUI() {
    voiceStatus.style.display = 'none';
    voiceButton.classList.remove('recording');
    voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
    voiceButton.title = '开始录音';
    isRecording = false;
}

// 显示语音错误消息
function showVoiceError(message) {
    addMessage('system', `语音输入错误: ${message}`, 'text');
}

// 显示语音信息消息
function showVoiceMessage(message) {
    addMessage('system', message, 'text');
}

// 添加事件监听器
voiceButton.addEventListener('click', toggleRecording);
voiceInputBtn.addEventListener('click', function() {
    if (!isRecording) {
        startRecording();
        document.querySelector('.nav-item[data-tab="chat"]').click();
    }
});

// 移动端语音输入
if (document.getElementById('mobileVoiceInput')) {
    document.getElementById('mobileVoiceInput').addEventListener('click', function() {
        if (!isRecording) {
            startRecording();
            document.querySelector('.nav-item[data-tab="chat"]').click();
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        }
    });
}

// 登录/注册相关变量
let isLoggedIn = false;
let currentUserId = null;
let currentUsername = null;

// 登录/注册模态框元素
const loginModal = document.getElementById('loginModal');
const loginTab = document.getElementById('loginTab');
const registerTab = document.getElementById('registerTab');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const closeModal = document.getElementById('closeModal');
const logoutBtn = document.getElementById('logoutBtnHeader');
const userInfoHeader = document.getElementById('userInfoHeader');
const userNameHeader = document.getElementById('userNameHeader');
const refreshHistoryBtn = document.getElementById('refreshHistory');

// 检查登录状态
function checkLoginStatus() {
    fetch('/check_login')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                isLoggedIn = true;
                currentUserId = data.user_id;
                currentUsername = data.username;
                updateUIForLoggedIn();
                loadChatHistory();
                // 加载当前对话的历史消息
                loadCurrentConversationHistory();
            } else {
                showLoginModal();
            }
        })
        .catch(error => {
            console.error('检查登录状态失败:', error);
            showLoginModal();
        });
}

// 加载当前对话的历史消息
function loadCurrentConversationHistory() {
    // 检查是否有从服务器传递的对话历史
    // 如果有，说明当前有活跃的对话，需要加载历史消息
    // 这个功能在页面加载时由后端渲染，所以不需要额外加载
}

// 更新UI为已登录状态
function updateUIForLoggedIn() {
    if (userInfoHeader) {
        userInfoHeader.style.display = 'flex';
        userNameHeader.textContent = currentUsername;
    }
    loginModal.style.display = 'none';
}

// 显示登录模态框
function showLoginModal() {
    loginModal.style.display = 'flex';
    loginTab.classList.add('active');
    registerTab.classList.remove('active');
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
    document.getElementById('modalTitle').textContent = '登录';
}

// 关闭模态框
function closeLoginModal() {
    loginModal.style.display = 'none';
}

// 切换登录/注册标签
loginTab.addEventListener('click', function() {
    loginTab.classList.add('active');
    registerTab.classList.remove('active');
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
    document.getElementById('modalTitle').textContent = '登录';
    clearAuthErrors();
});

registerTab.addEventListener('click', function() {
    registerTab.classList.add('active');
    loginTab.classList.remove('active');
    loginForm.style.display = 'none';
    registerForm.style.display = 'block';
    document.getElementById('modalTitle').textContent = '注册';
    clearAuthErrors();
});

// 清除错误信息
function clearAuthErrors() {
    document.getElementById('loginError').style.display = 'none';
    document.getElementById('registerError').style.display = 'none';
}

// 登录表单提交
loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    if (!username || !password) {
        showAuthError('loginError', '请输入用户名和密码');
        return;
    }

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            isLoggedIn = true;
            currentUserId = data.user_id;
            currentUsername = data.username;
            updateUIForLoggedIn();
            closeLoginModal();
            loadChatHistory();
            // 重新加载页面以获取对话历史
            location.reload();
        } else {
            showAuthError('loginError', data.error || '登录失败');
        }
    })
    .catch(error => {
        showAuthError('loginError', '网络错误，请重试');
    });
});

// 注册表单提交
registerForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('registerUsername').value.trim();
    const password = document.getElementById('registerPassword').value.trim();
    const confirmPassword = document.getElementById('confirmPassword').value.trim();

    if (!username || !password) {
        showAuthError('registerError', '请输入用户名和密码');
        return;
    }

    if (password !== confirmPassword) {
        showAuthError('registerError', '两次输入的密码不一致');
        return;
    }

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            isLoggedIn = true;
            currentUserId = data.user_id;
            currentUsername = data.username;
            updateUIForLoggedIn();
            closeLoginModal();
            loadChatHistory();
            // 重新加载页面以获取对话历史
            location.reload();
        } else {
            showAuthError('registerError', data.error || '注册失败');
        }
    })
    .catch(error => {
        showAuthError('registerError', '网络错误，请重试');
    });
});

// 显示认证错误
function showAuthError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

// 登出
if (logoutBtn) {
    logoutBtn.addEventListener('click', function() {
        if (confirm('确定要登出吗？')) {
            fetch('/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                isLoggedIn = false;
                currentUserId = null;
                currentUsername = null;
                userInfoHeader.style.display = 'none';
                chatMessages.innerHTML = `
                    <div class="welcome-message">
                        <div class="welcome-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="welcome-title">欢迎使用 Python 编程助手</div>
                        <div class="welcome-subtitle">我可以帮助您解决各种 Python 编程问题</div>
                    </div>
                `;
                document.getElementById('historyList').innerHTML = '';
                showLoginModal();
            })
            .catch(error => {
                console.error('登出失败:', error);
            });
        }
    });
}

// 关闭模态框事件
closeModal.addEventListener('click', closeLoginModal);
loginModal.addEventListener('click', function(e) {
    if (e.target === loginModal) {
        closeLoginModal();
    }
});

// 页面加载时初始化
window.addEventListener('load', function() {
    initTheme();
    initCopyButtons();
    initVoiceRecognition();

    if (window.innerWidth <= 768) {
        sidebar.classList.remove('active');
    }

    // 检查登录状态
    checkLoginStatus();

    // 初始化已渲染的消息（代码高亮、复制按钮等）
    setTimeout(() => {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
        addCopyButtonToCodeBlocks();
    }, 100);

    questionInput.focus();
});

// 加载对话历史
function loadChatHistory() {
    if (!isLoggedIn) {
        return;
    }

    fetch('/get_conversations')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const historyList = document.getElementById('historyList');
                historyList.innerHTML = '';

                if (data.conversations.length === 0) {
                    historyList.innerHTML = '<div class="no-history">暂无对话历史</div>';
                    return;
                }

                data.conversations.forEach(conv => {
                    const historyItem = document.createElement('div');
                    historyItem.className = 'history-item';
                    historyItem.dataset.conversationId = conv.id;

                    const date = new Date(conv.updated_at);
                    const now = new Date();
                    const diffTime = now - date;
                    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

                    let dateStr = '';
                    if (diffDays === 0) {
                        dateStr = '今天 ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
                    } else if (diffDays === 1) {
                        dateStr = '昨天 ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
                    } else if (diffDays < 7) {
                        dateStr = diffDays + '天前';
                    } else {
                        dateStr = date.toLocaleDateString('zh-CN');
                    }

                    const title = conv.title || '新对话';
                    historyItem.innerHTML = `
                        <div class="history-item-content">
                            <div class="history-title">${escapeHtml(title)}</div>
                            <div class="history-meta">
                                <span class="history-date">${dateStr}</span>
                                <span class="history-count">${conv.message_count || 0}条消息</span>
                            </div>
                        </div>
                        <button class="history-delete-btn" title="删除对话">
                            <i class="fas fa-trash"></i>
                        </button>
                    `;

                    // 点击加载对话
                    historyItem.querySelector('.history-item-content').addEventListener('click', function() {
                        loadConversation(conv.id);
                    });

                    // 删除对话
                    historyItem.querySelector('.history-delete-btn').addEventListener('click', function(e) {
                        e.stopPropagation();
                        if (confirm('确定要删除这个对话吗？')) {
                            deleteConversation(conv.id);
                        }
                    });

                    historyList.appendChild(historyItem);
                });
            } else {
                console.error('加载对话历史失败:', data.error);
            }
        })
        .catch(error => {
            console.error('加载对话历史失败:', error);
        });
}

// 加载指定对话
function loadConversation(conversationId) {
    fetch(`/load_conversation/${conversationId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 清空当前聊天界面
            chatMessages.innerHTML = '';

            // 加载历史消息
            if (data.history && data.history.length > 0) {
                data.history.forEach(msg => {
                    // 解码消息内容中的HTML实体，确保特殊字符正常显示
                    let decodedMessage = msg.message;
                    if (msg.type === 'text') {
                        decodedMessage = decodeHtmlEntities(msg.message);
                    } else if (msg.type === 'html') {
                        // 对于HTML类型，也需要解码，因为可能包含HTML实体
                        decodedMessage = decodeHtmlEntities(msg.message);
                    }
                    addMessage(msg.role, decodedMessage, msg.type);
                });
            } else {
                chatMessages.innerHTML = `
                    <div class="welcome-message">
                        <div class="welcome-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="welcome-title">欢迎使用 Python 编程助手</div>
                        <div class="welcome-subtitle">我可以帮助您解决各种 Python 编程问题</div>
                    </div>
                `;
            }

            // 更新历史列表选中状态
            document.querySelectorAll('.history-item').forEach(item => {
                item.classList.remove('active');
                if (item.dataset.conversationId == conversationId) {
                    item.classList.add('active');
                }
            });

            // 关闭移动端侧边栏
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        } else {
            alert('加载对话失败: ' + (data.error || '未知错误'));
        }
    })
    .catch(error => {
        console.error('加载对话失败:', error);
        alert('加载对话失败，请重试');
    });
}

// 删除对话
function deleteConversation(conversationId) {
    fetch(`/delete_conversation/${conversationId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 重新加载历史列表
            loadChatHistory();
            // 如果删除的是当前对话，清空聊天界面
            const currentConvId = document.querySelector('.history-item.active')?.dataset.conversationId;
            if (currentConvId == conversationId) {
                chatMessages.innerHTML = `
                    <div class="welcome-message">
                        <div class="welcome-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="welcome-title">欢迎使用 Python 编程助手</div>
                        <div class="welcome-subtitle">我可以帮助您解决各种 Python 编程问题</div>
                    </div>
                `;
            }
        } else {
            alert('删除对话失败: ' + (data.error || '未知错误'));
        }
    })
    .catch(error => {
        console.error('删除对话失败:', error);
        alert('删除对话失败，请重试');
    });
}

// 刷新历史记录
if (refreshHistoryBtn) {
    refreshHistoryBtn.addEventListener('click', function() {
        loadChatHistory();
    });
}

// 点击页面其他地方关闭移动端侧边栏
document.addEventListener('click', function(event) {
    if (window.innerWidth <= 768 &&
        !sidebar.contains(event.target) &&
        !mobileMenuToggle.contains(event.target) &&
        sidebar.classList.contains('active')) {
        sidebar.classList.remove('active');
    }
});

// 响应式调整
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        sidebar.classList.add('active');
    } else {
        sidebar.classList.remove('active');
    }
});

// 键盘快捷键
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        alert('快捷键帮助:\nCtrl+/ - 显示帮助\nCtrl+Enter - 发送消息\nCtrl+N - 新建对话\nCtrl+T - 切换主题\nCtrl+M - 语音输入');
    }

    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }

    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        newChatButton.click();
    }

    if (e.ctrlKey && e.key === 't') {
        e.preventDefault();
        toggleTheme();
    }

    if (e.ctrlKey && e.key === 'm') {
        e.preventDefault();
        toggleRecording();
    }
});

// 错误处理
window.addEventListener('error', function(e) {
    console.error('JavaScript错误:', e.error);
});

// 未处理的Promise拒绝
window.addEventListener('unhandledrejection', function(e) {
    console.error('未处理的Promise拒绝:', e.reason);
});

// 流式输出支持（可选功能）
function sendMessageStream() {
    const message = questionInput.value.trim();
    if (!message) {
        alert('请输入问题');
        return;
    }

    const welcomeMessage = document.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    addMessage('user', message, 'text');
    questionInput.value = '';
    questionInput.style.height = 'auto';

    showTypingIndicator();

    const eventSource = new EventSource(`/ask_stream?question=${encodeURIComponent(message)}`);
    let fullAnswer = '';

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);

        if (data.error) {
            removeTypingIndicator();
            addMessage('system', `错误: ${data.error}`, 'text');
            eventSource.close();
            return;
        }

        if (data.finished) {
            removeTypingIndicator();
            fullAnswer = data.full_answer;
            eventSource.close();
        } else {
            updateLastMessage(data.chunk);
        }
    };

    eventSource.onerror = function(event) {
        removeTypingIndicator();
        addMessage('system', '连接错误，请重试', 'text');
        eventSource.close();
    };
}

function updateLastMessage(content) {
    const lastMessage = document.querySelector('.message.assistant:last-child .message-text');
    if (lastMessage) {
        const decodedContent = decodeHtmlEntities(content);
        lastMessage.innerHTML = decodedContent;

        setTimeout(() => {
            document.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
            addCopyButtonToCodeBlocks();
        }, 100);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// 手册搜索功能
function searchHandbook(query) {
    fetch('/search_handbook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addMessage('assistant', data.result, 'html');
            } else {
                addMessage('system', `搜索失败: ${data.error}`, 'text');
            }
        })
        .catch(error => {
            addMessage('system', `网络错误: ${error}`, 'text');
        });
}

// 修改 ask_question 函数，在检测到基础概念问题时自动搜索手册
function enhanceQuestionWithHandbook(question) {
    const basicConcepts = ['是什么', '什么是', '定义', '概念', '介绍', '讲解', '说明', '含义'];
    const hasBasicConcept = basicConcepts.some(concept => question.includes(concept));
    
    if (hasBasicConcept) {
        console.log('检测到基础概念问题，将在回答中参考手册内容');
    }
    
    return question;
}

// 清理资源
window.addEventListener('beforeunload', function() {
    if (audioStream) {
        audioStream.getTracks().forEach(track => track.stop());
    }
});

// 爬虫功能元素
const startCrawlerBtn = document.getElementById('startCrawlerBtn');
const urlInput = document.getElementById('urlInput');
const copyResultBtn = document.getElementById('copyResultBtn');
const sendToChatBtn = document.getElementById('sendToChatBtn');
const crawlerResults = document.getElementById('crawlerResults');
const resultUrl = document.getElementById('resultUrl');
const markdownContent = document.getElementById('markdownContent');

// 爬虫按钮事件监听
startCrawlerBtn.addEventListener('click', function () {
    const url = urlInput.value.trim();
    if (!url) {
        alert('请输入要爬取的网址');
        return;
    }
    
    // 验证URL格式
    if (!isValidUrl(url)) {
        alert('请输入有效的网址格式（如：https://example.com）');
        return;
    }
    
    startWebCrawler(url);
});

// URL输入框回车事件
urlInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        startCrawlerBtn.click();
    }
});

// 复制结果按钮事件
copyResultBtn.addEventListener('click', function () {
    const content = markdownContent.innerText;
    copyToClipboard(content, copyResultBtn);
    
    // 临时修改按钮文本
    const originalText = copyResultBtn.innerHTML;
    copyResultBtn.innerHTML = '<i class="fas fa-check"></i> 已复制';
    setTimeout(() => {
        copyResultBtn.innerHTML = originalText;
    }, 2000);
});

// 发送到对话按钮事件
sendToChatBtn.addEventListener('click', function () {
    const content = markdownContent.innerText;
    const url = resultUrl.innerText;
    
    document.querySelector('.nav-item[data-tab="chat"]').click();
    
    const resultHtml = `
<div class="crawler-chat-result">
    <div class="crawler-header">
        <i class="fas fa-spider"></i>
        <span>网页爬取结果</span>
    </div>
    <div class="crawler-content">
        <div class="url-info">
            <strong>目标网址：</strong> ${url}
        </div>
        <pre><code class="language-markdown">${escapeHtml(content)}</code></pre>
    </div>
</div>
    `;
    
    addMessage('system', resultHtml, 'html');
    
    // 高亮代码
    setTimeout(() => {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
        addCopyButtonToCodeBlocks();
    }, 100);
});

function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function startWebCrawler(url) {
    // 显示加载状态
    startCrawlerBtn.disabled = true;
    startCrawlerBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 爬取中...';
    
    fetch('/web_crawler', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        // 恢复按钮状态
        startCrawlerBtn.disabled = false;
        startCrawlerBtn.innerHTML = '<i class="fas fa-spider"></i> 开始爬取';
        
        if (data.success) {
            // 显示爬取结果
            resultUrl.textContent = url;
            markdownContent.textContent = data.result;
            crawlerResults.style.display = 'block';
            
            // 滚动到结果区域
            crawlerResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
            // 高亮Markdown代码
            setTimeout(() => {
                hljs.highlightElement(markdownContent);
            }, 100);
            
        } else {
            // 显示错误信息
            alert(`爬取失败：${data.error || '未知错误'}`);
        }
    })
    .catch(error => {
        // 恢复按钮状态
        startCrawlerBtn.disabled = false;
        startCrawlerBtn.innerHTML = '<i class="fas fa-spider"></i> 开始爬取';
        alert(`网络错误：${error.message || '网络连接失败'}`);
    });
}