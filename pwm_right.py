import pigpio
import time

# --- 設定 ---
PIN = 18        # 右臂馬達腳位 (請確認您的接線)
SPEED = 0.02    # 速度 (數字越大越慢)
STEP = 10       # 每次移動的幅度

pi = pigpio.pi()
if not pi.connected:
    print("❌ pigpiod 沒開！")
    exit()

# 初始位置設為 1500 (理論上的水平位置)
current_pos = 1500

def slow_move(target_pos):
    global current_pos
    print(f"目標: {target_pos}...", end="")
    
    if target_pos > current_pos:
        step_dir = STEP
    else:
        step_dir = -STEP
        
    for pwm in range(current_pos, target_pos, step_dir):
        pi.set_servo_pulsewidth(PIN, pwm)
        time.sleep(SPEED)
        
    pi.set_servo_pulsewidth(PIN, target_pos)
    current_pos = target_pos
    print(" 到達！")

try:
    print("⚠️ 測試開始！請把手放在電池盒開關上，撞到桌子立刻斷電！")
    time.sleep(1)

    # 1. 先回到中間 (水平)
    print("1. 回到中間 (1500)")
    pi.set_servo_pulsewidth(PIN, 1500)
    current_pos = 1500
    time.sleep(1)

    # 2. 測試往上 (通常數值變大或變小會往上，看馬達安裝方向)
    # 我們先試試看 1700
    print("2. 測試動作 A (1700)")
    slow_move(1700)
    time.sleep(1)

    # 3. 回到中間
    print("3. 回到中間 (1500)")
    slow_move(1500)
    time.sleep(1)

    # 4. 測試往下 (小心撞桌子！)
    # 我們只試到 1300，不要太低
    print("4. 測試動作 B (1000)")
    slow_move(1000)
    time.sleep(1)

    # 5. 回到中間
    print("5. 回到中間 (1500)")
    slow_move(1500)
    
    print("測試完成！")

except KeyboardInterrupt:
    print("\n停止")

finally:
    # 這裡可以選擇要不要放鬆
    # 如果手臂很重，放鬆(0)可能會直接「掉下來」撞桌子
    # 所以我們讓它停在 1500 就好，或者您可以小心地接住它
    print("放鬆馬達...")
    pi.set_servo_pulsewidth(PIN, 0)
    pi.stop()