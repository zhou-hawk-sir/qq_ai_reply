	# QQ 自动聊天 AI (OCR 版)
	基于 Python 和 OCR 技术的 QQ 自动回复机器人，具备上下文记忆、主动找话题及特定人设模拟功能。
	## ✨ 功能特性
	*   **OCR 屏幕识别**: 使用 PaddleOCR 实时读取屏幕聊天记录，无需接入 QQ 协议。
	*   **上下文记忆**: 使用 `deque` 维护多轮对话历史（默认 8 轮），让 AI 更懂上下文。
	*   **主动找话题**: 内置空闲检测机制（默认 70 秒），无人说话时 AI 会主动发起贱贱的骚扰。
	*   **智能去重**: 本地缓存 OCR 识别结果，防止重复回复或误识别自己发送的消息。
	*   **人设模拟**: 基于智谱 AI (GLM-4-Flash) 模型，内置"贱贱的"、"流里流气"的真人语气人设。
	*   **可视化校准**: 提供坐标校准工具，自动适配不同分辨率屏幕。
	## 📦 环境依赖
	*   Python 3.x
	*   智谱 AI API Key ([申请地址](https://open.bigmodel.cn/))
	## 🛠️ 安装步骤
	1.  **克隆项目**
	    ```bash
	    git clone <your-repo-url>
	    cd <project-directory>
	    ```
	2.  **安装依赖库**
	    ```bash
	    pip install pyautogui opencv-python numpy paddleocr zhipuai python-dotenv pyperclip
	    ```
	3.  **配置 API Key**
	    在项目根目录下创建 `.env` 文件，并填入你的 Key：
	    ```env
	    ZHIPU_API_KEY=your_actual_api_key_here
	    ```
	## 🚀 使用指南
	### 第一步：校准坐标 (必须)
	由于不同电脑屏幕分辨率不同，首次使用必须运行校准脚本以获取准确的截图区域和点击坐标。
	1.  运行校准工具：
	    ```bash
	    python get_region.py
	    ```
	2.  按照终端提示，依次移动鼠标点击聊天区域的对角线、输入框中心、好友消息左边缘、自己消息右边缘。
	3.  脚本结束后，复制终端输出的配置代码段。
	4.  打开 `qq_ocr_live.py`，找到文件开头的 `参数配置` 区域，用刚才复制的内容**完全覆盖**原有的 `REGION`、`CLICK_POS`、`FRIEND_LEFT_THRESHOLD` 和 `ME_RIGHT_THRESHOLD` 变量。
	### 第二步：运行机器人
	1.  打开 QQ 聊天窗口，并确保其位于屏幕最前方。
	2.  运行主程序：
	    ```bash
	    python qq_ocr_live.py
	    ```
	3.  程序将自动开始监听，当好友发消息时会自动回复，或长时间无消息时主动找话题。
	## 📂 项目结构说明
	| 文件名 | 说明 |
	| :--- | :--- |
	| `memory.py` | 聊天记忆模块，使用 `deque` 存储 User 和 Assistant 的历史对话。 |
	| `ai_reply.py` | AI 接口模块，对接智谱 AI，定义了 System Prompt（人设）和回复逻辑。 |
	| `qq_ocr_live.py` | **主程序**。负责截图、OCR 识别、判断消息归属、防复读及模拟键盘输入。 |
	| `get_region.py` | 辅助工具，用于获取屏幕坐标参数，简化配置流程。 |
	## 🎭 人设自定义
	如需修改 AI 的性格，请编辑 `ai_reply.py` 文件中的以下变量：
	*   `SYSTEM_PROMPT_NORMAL`: 正常回复时的人设（当前设定为：贱贱的、惜字如金、阴阳怪气）。
	*   `SYSTEM_PROMPT_IDLE`: 主动找话题时的人设（当前设定为：无厘头、骚扰、冷笑话）。
	## ⚠️ 注意事项
	1.  **屏幕遮挡**: 运行时请确保 QQ 聊天窗口不被其他窗口遮挡，否则 OCR 无法识别文字。
	2.  **分辨率变动**: 如果你改变了窗口大小或屏幕分辨率，需要重新运行 `get_region.py` 进行校准。
	3.  **网络环境**: 需要能够访问智谱 AI 的 API 接口。
	4.  **误触防护**: 程序包含黑名单过滤（如“发送”、“图片”等）和长度限制（2-50字），以降低误操作概率，但建议初次使用时在旁观察。
	## 📄 开源协议
	MIT License
