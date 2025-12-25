import pyautogui
import os
import time


def get_mouse_pos(prompt):
    print(f"\n👉 {prompt}")
    print("   (请移动鼠标到指定位置，按回车键确认)")
    input()
    x, y = pyautogui.position()
    print(f"   ✅ 锁定坐标: {x}, {y}")
    return x, y


def main():
    print("========================================")
    print("    QQ 机器人坐标校准 (v4.0 边缘判定版)")
    print("========================================")
    print("核心逻辑：")
    print("- 好友消息靠左：检测【文本框最左边】")
    print("- 自己消息靠右：检测【文本框最右边】")
    print("========================================\n")
    # 1. 截图区域
    print("【第一步：校准 OCR 截图区域】")
    x1, y1 = get_mouse_pos("移到聊天记录区域的【左上角】")
    x2, y2 = get_mouse_pos("移到聊天记录区域的【右下角】")
    # 2. 输入框点击位置
    print("\n【第二步：校准输入框点击位置】")
    click_x, click_y = get_mouse_pos("移到输入框【中间空白处】")
    # 3. 好友左边缘判定
    print("\n【第三步：好友左阈值判定】")
    print("   找一条【好友发】的消息。")
    print("   将鼠标移到【文字气泡的最左边边缘】（光标紧贴着字的左边）。")
    friend_left_x, _ = get_mouse_pos("移到好友消息【文字的最左边】")
    # 4. 自己右边缘判定
    print("\n【第四步：自己右阈值判定】")
    print("   找一条【你自己发】的消息。")
    print("   将鼠标移到【文字气泡的最右边边缘】（光标紧贴着字的右边）。")
    me_right_x, _ = get_mouse_pos("移到你自己消息【文字的最右边】")
    # 计算
    region_x = x1
    region_y = y1
    region_w = x2 - x1
    region_h = y2 - y1
    print("\n\n" + "=" * 40)
    print("🎉 配置完成！请复制以下代码：")
    print("=" * 40)
    print(f"""
REGION = {{
    "x": {region_x},
    "y": {region_y},
    "w": {region_w},
    "h": {region_h}
}}
# 输入框点击坐标
CLICK_POS = ({click_x}, {click_y})
# 阈值配置
# 好友判定：如果文字的最左边 < 此值，判定为好友
FRIEND_LEFT_THRESHOLD = {friend_left_x + 20}  # 加一点容错空间
# 自己判定：如果文字的最右边 > 此值，判定为我自己
ME_RIGHT_THRESHOLD = {me_right_x - 20}    # 减一点容错空间
""")
    print("=" * 40)
    print("说明：代码会自动给阈值留一点余量，防止误判。")
    input("\n按回车退出...")


if __name__ == "__main__":
    main()