QQ Auto Chat AI 🤖
一个基于OCR和AI的QQ自动聊天机器人，能够实时识别聊天窗口中的消息并使用AI生成回复，支持上下文记忆和主动发起话题功能。

✨ 核心特性
实时OCR识别：使用PaddleOCR实时截取QQ聊天窗口并识别文本

智能AI回复：集成智谱AI大模型，生成符合人设的回复

完整上下文记忆：保留最近对话历史，回复更自然连贯

主动聊天模式：长时间无消息时主动发起话题

防复读机制：避免重复识别和回复相同内容

坐标校准工具：提供可视化坐标校准脚本

📁 项目结构
├── qq_ocr_live.py      # 主程序：OCR识别 + AI回复
├── ai_reply.py         # AI回复逻辑：调用智谱API
├── memory.py           # 对话记忆管理
├── get_region.py       # 坐标校准工具
├── .env                # API密钥配置（需手动创建）
└── requirements.txt    # 依赖包列表
🚀 快速开始
1. 环境准备
# 克隆项目
git clone https://github.com/yourusername/qq-auto-chat-ai.git
cd qq-auto-chat-ai

# 安装依赖
pip install -r requirements.txt
2. API密钥配置
前往智谱AI开放平台注册账号并获取API密钥

在项目根目录创建.env文件：

env
ZHIPU_API_KEY=your_api_key_here
3. 坐标校准
bash
python get_region.py
按照提示依次校准：

聊天记录区域（左上角和右下角）

输入框点击位置

好友消息左边缘

自己消息右边缘

程序会生成配置代码，复制到qq_ocr_live.py中替换相应变量。

4. 运行机器人
bash
python qq_ocr_live.py
⚙️ 配置说明
主要参数（qq_ocr_live.py）
参数	说明	默认值
REGION	OCR截图区域	{"x": 11, "y": 86, "w": 936, "h": 664}
CLICK_POS	输入框点击坐标	(356, 896)
FRIEND_LEFT_THRESHOLD	好友消息左阈值	96
ME_RIGHT_THRESHOLD	自己消息右阈值	852
AUTO_TALK_INTERVAL	主动聊天间隔(秒)	70
AI人设配置（ai_reply.py）
正常回复模式：语气"贱贱的"、"欠欠的"，惜字如金

主动找话题模式：无厘头、随意，用于打破沉默

🎯 使用场景
自动陪聊：QQ好友无聊时陪你聊天

消息自动回复：忙碌时自动回复简单消息

聊天测试：测试聊天机器人的对话效果

娱乐互动：有趣的AI对话体验

⚠️ 重要提醒
合法使用
仅用于学习和娱乐目的

遵守QQ用户协议

不得用于骚扰、诈骗等非法用途

技术限制
OCR识别可能存在误差

AI回复可能不符合预期

不支持图片、表情等非文本消息

运行要求
保持QQ聊天窗口在顶层

确保聊天区域可见

网络连接稳定

🔧 常见问题
Q: OCR识别不到消息？
A: 检查REGION配置是否正确，确保聊天窗口在截图区域内。

Q: AI回复太长？
A: 在ai_reply.py中调整SYSTEM_PROMPT_NORMAL的提示词，或修改长度限制。

Q: 误识别自己的消息？
A: 重新校准ME_RIGHT_THRESHOLD，确保正确区分左右消息。

Q: 响应速度慢？
A: 可尝试降低OCR识别频率或使用更快的AI模型。

🛠️ 自定义修改
修改AI人设
编辑ai_reply.py中的SYSTEM_PROMPT_NORMAL和SYSTEM_PROMPT_IDLE，调整语气和风格。

调整记忆长度
在ai_reply.py中修改：

python
memory = ChatMemory(max_turns=8)  # 改为其他数字
修改回复频率
在qq_ocr_live.py中调整：

python
AUTO_TALK_INTERVAL = 70  # 主动聊天间隔
time.sleep(0.5)          # 检测间隔
📦 依赖包
txt
pyautogui>=0.9.54
opencv-python>=4.8.1
numpy>=1.24.3
paddleocr>=2.7.0
zhipuai>=2.0.1
python-dotenv>=1.0.0
pyperclip>=1.8.2
📄 许可证
本项目仅供学习和娱乐使用，请遵守相关法律法规和平台规定。

🤝 贡献
欢迎提交Issue和Pull Request！

⚠️ 免责声明
本项目为开源学习项目，作者不对使用本软件造成的任何后果负责。使用者应自行承担风险，并遵守相关法律法规。

温馨提示：适度使用，保持真实人际交往更重要哦~ 😊
