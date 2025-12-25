import os
import time
import random
import re
import difflib
from collections import deque
import pyautogui
import cv2
import numpy as np
from paddleocr import PaddleOCR
from ai_reply import ai_reply  # 导入你的 ai_reply
import pyperclip

# ======================
# 第一步：环境初始化
# ======================
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# ======================
# 参数配置
# ======================
REGION = {"x": 11, "y": 86, "w": 936, "h": 664}
CLICK_POS = (356, 896)
FRIEND_LEFT_THRESHOLD = 96
ME_RIGHT_THRESHOLD = 852
# 主动聊天时间间隔（秒）
AUTO_TALK_INTERVAL = 70
# ======================
# 初始化 OCR
# ======================
ocr = PaddleOCR(
    lang="ch",
    use_textline_orientation=True
)


# ======================
# 核心工具函数
# ======================
def capture_chat_region():
    img = pyautogui.screenshot(region=(REGION["x"], REGION["y"], REGION["w"], REGION["h"]))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def force_focus_by_click():
    pyautogui.click(CLICK_POS[0], CLICK_POS[1])
    time.sleep(0.2)


def is_valid_text(text):
    """有效性检查，略微放宽以适应短句"""
    # 1. 长度检查：允许2个字符（防止 "nb", "在吗" 被过滤）
    if len(text) < 2 or len(text) > 50:
        return False
    # 2. 黑名单
    blacklist = ["关闭", "发送", "表情", "图片", "更多", "查看", "下载", "取消", "qq", "http", "://", "ai", "AI"]
    if any(b in text.lower() for b in blacklist):
        return False
    # 3. 纯数字或时间
    if text.isdigit() or re.match(r'^\d{1,2}:\d{2}$', text):
        return False
    # 4. 乱码检查
    garbage_chars = sum(1 for c in text if not (c.isalnum() or '\u4e00' <= c <= '\u9fff'))
    if len(text) > 0 and (garbage_chars / len(text)) > 0.3:
        return False
    if text.strip() == "":
        return False
    return True


def is_similar(a, b, threshold=0.85):
    """判断两个字符串是否相似"""
    return difflib.SequenceMatcher(None, a, b).ratio() > threshold


def ocr_image(img):
    result = ocr.predict(img)
    outputs = []
    if not result or not result[0]:
        return outputs
    data = result[0]
    boxes = data.get('dt_polys')
    texts = data.get('rec_texts')
    scores = data.get('rec_scores')
    if boxes is None:
        return outputs
    for i in range(len(boxes)):
        try:
            box = boxes[i]
            text = texts[i]
            score = scores[i]
            # 【关键修复】大幅降低置信度阈值
            # 短词如 "nb" 置信度往往不高，如果设为 0.75 会被丢弃
            # 设为 0.6 可以抓取更多模糊短句，让后续逻辑去判断
            if score < 0.6:
                continue
            outputs.append((box, text, score))
        except Exception:
            continue
    return outputs


def is_friend_msg(box):
    """判定是否为左侧好友消息"""
    x_coords = [p[0] for p in box]
    min_x = min(x_coords)
    max_x = max(x_coords)
    center_x = (min_x + max_x) / 2
    if max_x >= (ME_RIGHT_THRESHOLD - 20):
        return False
    if min_x <= FRIEND_LEFT_THRESHOLD:
        if center_x > (REGION["w"] / 2):
            return False
        return True
    return False


def get_best_message(candidates):
    """
    【核心修复】从候选文本中选出视觉上最下方的一条
    """
    if not candidates:
        return None
    valid_candidates = []
    for box, text, score in candidates:
        # 清理首尾空格
        clean_text = text.strip()
        if not is_valid_text(clean_text):
            continue
        if not is_friend_msg(box):
            continue
        # 获取 Y 坐标底部
        y_coords = [p[1] for p in box]
        bottom_y = max(y_coords)
        valid_candidates.append((bottom_y, clean_text, score))
    if not valid_candidates:
        return None
    # 按 Y 坐标从大到小排序，取第一条（最下面的一条）
    valid_candidates.sort(key=lambda x: x[0], reverse=True)
    return valid_candidates[0][1]


# ======================
# 主循环
# ======================
if __name__ == "__main__":
    print("========================================")
    print("🤖 QQ 自动聊天 AI (终极记忆版)")
    print("✨ 特性：低阈值短词识别 | 完整上下文记忆 | AI动态找话题")
    print("========================================")
    time.sleep(2)
    # 1. OCR 防复读记录（用于屏蔽 OCR 识别抖动，不传给 AI）
    ocr_dedup_history = deque(maxlen=10)
    # 2. 活跃时间追踪（用于触发主动聊天）
    last_active_time = time.time()
    while True:
        try:
            current_time = time.time()
            img = capture_chat_region()
            raw_ocr_results = ocr_image(img)
            current_msg = get_best_message(raw_ocr_results)
            # ==========================================
            # 场景 A: 检测到新消息
            # ==========================================
            if current_msg:
                # 更新活跃时间
                last_active_time = current_time
                # 1. 本地 OCR 防复读检查
                # 目的：如果 OCR 把 "nb" 识别成 " n b " 和 "nb"，只处理第一个
                is_ocr_duplicate = False
                for old_msg in ocr_dedup_history:
                    if is_similar(current_msg, old_msg):
                        is_ocr_duplicate = True
                        break
                if is_ocr_duplicate:
                    time.sleep(0.5)
                    continue
                # 记录到本地防复读
                ocr_dedup_history.append(current_msg)
                print(f"\n👉 好友：{current_msg}")
                # 2. 调用 AI 回复
                # 这里不需要传 history，你的 ai_reply.py 内部有 memory = ChatMemory()
                # 它会自动处理上下文记忆，不需要我们在外面维护
                reply = ai_reply(current_msg)
                print(f"🤖 AI：{reply}")
                # 3. 发送
                # 模拟人类思考延迟
                think_time = random.uniform(1.0, 2.0)
                time.sleep(think_time)
                force_focus_by_click()
                time.sleep(0.1)
                pyperclip.copy(reply)
                time.sleep(0.1)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(random.uniform(0.2, 0.4))
                pyautogui.press("enter")
                print("✅ 已回复")
                # 4. 把自己的回复也加入防复读，防止下一帧识别到自己的话
                ocr_dedup_history.append(reply)
                time.sleep(1.5)
            # ==========================================
            # 场景 B: 无人说话，触发 AI 主动找话题
            # ==========================================
            elif (current_time - last_active_time) > AUTO_TALK_INTERVAL:
                print(f"💤 超过 {AUTO_TALK_INTERVAL} 秒无消息，AI 主动找话题...")
                # 调用 ai_reply 的 active 模式
                # 这会利用你 ai_reply.py 里的 SYSTEM_PROMPT_IDLE 生成贱贱的话
                topic = ai_reply("", mode="active")
                print(f"🤖 (主动) {topic}")
                force_focus_by_click()
                time.sleep(0.1)
                pyperclip.copy(topic)
                time.sleep(0.1)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(random.uniform(0.2, 0.4))
                pyautogui.press("enter")
                # 记录，防止自己回复自己
                ocr_dedup_history.append(topic)
                # 重置计时
                last_active_time = current_time
                time.sleep(2.0)
            else:
                # 没有消息且未到主动聊天时间
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n👋 已退出")
            break
        except Exception as e:
            print(f"❌ 异常：{e}")
            time.sleep(2)