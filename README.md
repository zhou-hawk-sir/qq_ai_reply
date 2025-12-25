	# QQ 自动聊天 AI (OCR 版)
 
一个基于 Python 的 QQ 自动回复机器人，通过屏幕截图和 OCR (光学字符识别) 技术读取聊天内容，并利用智谱 AI (ZhipuAI) 生成具有特定“人设”的回复。该项目支持上下文记忆、主动找话题以及可视化的坐标校准。
 
## 功能特性
 
- **OCR 屏幕识别**: 使用 `PaddleOCR` 实时读取 QQ 聊天窗口内的文字，支持低阈值短词识别。
- **智能回复**: 调用智谱 AI `glm-4-flash` 模型生成回复，模拟真人语气。
- **上下文记忆**: 内置 `ChatMemory` 模块，使用双端队列 (`deque`) 维护多轮对话历史（默认记忆 8 轮）。
- **主动聊天**: 内置空闲检测机制，当超过 70 秒无新消息时，AI 会主动开启话题。
- **防复读机制**: 本地缓存 OCR 识别结果，防止因识别抖动导致的重复回复或误识别自己发送的消息。
- **坐标校准工具**: 提供可视化的 `get_region.py` 脚本，辅助用户快速配置屏幕抓取区域、输入框点击位置及消息判定的左右阈值。
 
## 环境要求
 
- Python 3.x
- 智谱 AI API Key ([申请地址](https://open.bigmodel.cn/))
 
## 安装依赖
 
请确保已安装以下第三方库：
 
```bash
pip install pyautogui opencv-python numpy paddleocr zhipuai python-dotenv pyperclip
bash

复制代码
配置步骤
1. 配置 API Key
在项目根目录下创建 .env 文件，并填入你的智谱 AI Key：

ZHIPU_API_KEY=your_api_key_here
bash

复制代码
2. 校准屏幕坐标 (重要)
由于不同电脑屏幕分辨率和 QQ 窗口位置不同，必须先进行坐标校准。

运行校准脚本：
python get_region.py
bash

复制代码
按照终端提示，依次移动鼠标到：
聊天记录区域的左上角和右下角
输入框的中间空白处
好友消息的文字气泡最左边边缘
你自己消息的文字气泡最右边边缘
脚本结束后，会输出一段包含 REGION, CLICK_POS, FRIEND_LEFT_THRESHOLD, ME_RIGHT_THRESHOLD 的配置代码。
将输出的代码完整复制并覆盖到 qq_ocr_live.py 文件中的对应配置区域。
使用方法
打开 QQ 聊天窗口，并确保聊天区域可见且未被遮挡。
运行主程序：
python qq_ocr_live.py
bash

复制代码
程序将自动开始监听屏幕：
场景 A: 当检测到好友发送消息时，经过防复读和有效性检查后，调用 AI 生成回复并自动发送。
场景 B: 当超过 70 秒无新消息时，AI 会自动发起一句“贱贱的”骚扰话语。
项目结构
memory.py: 实现对话记忆的核心类 ChatMemory，负责存储和检索历史消息。
qq_ocr_live.py: 主程序，负责截图、OCR 识别、消息有效性过滤、发送者判定（好友/自己）及模拟键盘输入。
ai_reply.py: 处理与智谱 AI 的交互，包含 System Prompt（人设定义）和接口调用逻辑。
get_region.py: 屏幕坐标校准辅助工具。
人设说明
当前 AI 人设定义在 ai_reply.py 中，具有以下特征：

语气：贱贱的、欠欠的、口语化、带点流里流气。
风格：惜字如金，喜欢反问句，会阴阳怪气，绝对不承认自己是 AI。
主动模式：无厘头、喜欢骚扰对方。
如需修改人设，请编辑 ai_reply.py 中的 SYSTEM_PROMPT_NORMAL（正常回复）和 SYSTEM_PROMPT_IDLE（主动找话题）变量。

注意事项
运行时请勿遮挡 QQ 聊天窗口，否则 OCR 无法正确识别文字。
确保网络连接正常，以便调用智谱 AI API。
程序使用了 pyautogui 进行模拟操作，运行时请勿强行移动鼠标干扰发送过程。
默认 OCR 置信度阈值设为 0.6，且对文本长度（2-50字）和黑名单（如“发送”、“AI”等）进行了过滤，以减少误触。
