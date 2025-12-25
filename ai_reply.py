import os
from zhipuai import ZhipuAI
from dotenv import load_dotenv
from memory import ChatMemory

load_dotenv()

# 请确保 .env 文件里有API_KEY
client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))

# 记忆轮数
memory = ChatMemory(max_turns=8)

# === 核心人设：===
SYSTEM_PROMPT_NORMAL = """
你是一个真实的人类，正在QQ上和朋友聊天。
人设要求：
1. 说话语气要“贱贱的”、“欠欠的”，带点流里流气，潇洒一点，可以骂他。
2. 极其口语化，多用反问句，可以用“呵呵”、“切”、“笑死”。装逼“”。
3. 惜字如金，不要长篇大论，能三个字说完绝不发十个字。
4. 如果对方问无聊的问题，就敷衍他；如果对方怼你，你就阴阳怪气怼回去。
5. 绝对不要承认自己是AI，绝对不要带“你好”、“请问”这种客套话。
6.尽量不要超过20个字
"""

# === 主动找话题人设 ===
SYSTEM_PROMPT_IDLE = """
你正在QQ上聊天，对方好久没回消息了，或者你需要开启一个话题。
要求：
1. 语气随意、无厘头，像突然想到的。
2. 可以是发个牢骚、讲个冷笑话、或者单纯为了骚扰对方一下。
3. 比如说：“人呢？死哪去了？” 或者 “突然觉得你长得像个土豆。”
4. 不要问“在吗”，太老土了。
"""


def ai_reply(user_text: str, mode: str = "reply") -> str:
    """
    mode: "reply" (正常回复) | "active" (主动找话题)
    """

    # ========= 主动找话题模式 =========
    if mode == "active":
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_IDLE},
            {
                "role": "user",
                "content": "对方不理我，给我生成一句贱贱的骚扰话。"
            }
        ]

        try:
            resp = client.chat.completions.create(
                model="glm-4-flash",  # 使用较快且便宜的模型
                messages=messages,
                temperature=0.95,
                top_p=0.9
            )
            reply = resp.choices[0].message.content.strip()
            # 记忆中也要加上这句，防止上下文断裂
            memory.add_ai(reply)
            return reply
        except Exception as e:
            print(f"AI API Error: {e}")
            return "..."

    # ========= 正常聊天模式 =========
    # 存入对方消息
    memory.add_user(user_text)

    messages = [
                   {"role": "system", "content": SYSTEM_PROMPT_NORMAL}
               ] + memory.messages()

    try:
        resp = client.chat.completions.create(
            model="glm-4-flash",
            messages=messages,
            temperature=0.8,
            top_p=0.9
        )
        reply = resp.choices[0].message.content.strip()

        # 简单过滤，防止AI抽风发太长
        if len(reply) > 40:
            # 如果太长，尝试截断或者保留前两句
            parts = reply.replace("。", ",").split(",")
            reply = parts[0]

        memory.add_ai(reply)
        return reply
    except Exception as e:
        print(f"AI API Error: {e}")
        return "切，懒得理你。"