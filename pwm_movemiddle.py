import pigpio
import time

# --- 設定 ---
BASE_PIN = 18   # 底座馬達腳位
SPEED = 0.01    # 每個小步之間的等待時間 (秒) -> 越小越快，越大越慢
STEP = 10       # 每次移動的脈衝量 -> 越小越細膩，但計算量大

pi = pigpio.pi()
if not pi.connected:
    exit()

# 記錄目前位置 (假設一開始在中間)
current_pos = 1500
pi.set_servo_pulsewidth(BASE_PIN, current_pos)

def slow_move(pin, target_pos):
    """
    讓馬達從 [目前位置] 慢慢移動到 [目標位置]
    """
    global current_pos
    
    # 判斷是往上加還是往下減
    if target_pos > current_pos:
        step_dir = STEP
    else:
        step_dir = -STEP
        
    # 開始慢慢走
    # range(開始, 結束, 步伐)
    for pwm in range(current_pos, target_pos, step_dir):
        pi.set_servo_pulsewidth(pin, pwm)
        time.sleep(SPEED) # 這裡決定速度！
        
    # 確保最後停在準確的目標點
    pi.set_servo_pulsewidth(pin, target_pos)
    
    # 更新目前位置記錄
    current_pos = target_pos

try:
    print("1. 慢慢back (1000)...")
    slow_move(BASE_PIN, 2000)
    time.sleep(1)

    print("2. 慢慢forward (2350)...")
    slow_move(BASE_PIN, 2350)
    time.sleep(1)

    print("3. 超級reset (1550)...")
    # 臨時把速度調慢
    
    slow_move(BASE_PIN, 1550)
    
    print("測試完成")

except KeyboardInterrupt:
    pass
finally:
    pi.set_servo_pulsewidth(BASE_PIN, 0) # 放鬆
    pi.stop()
