import pigpio
import time

# --- 您的專屬設定 ---
SERVO_PIN = 18      # 夾爪馬達腳位
VAL_CLOSE = 2350    # 您測出的閉合值
VAL_OPEN  = 1600    # 您測出的張開值
# ------------------

print("正在連線到 pigpiod...")
pi = pigpio.pi()

if not pi.connected:
    print("❌ 錯誤：pigpiod 服務沒開！請輸入 sudo systemctl start pigpiod")
    exit()

print(f"✅ 連線成功！")
print(f"開始連續動作：張開({VAL_OPEN}) <-> 閉合({VAL_CLOSE})")
print("按 Ctrl+C 可以隨時停止")

try:
    while True:
        # 動作 1: 張開
        print(f"-> 張開 (PWM: {VAL_OPEN})")
        pi.set_servo_pulsewidth(SERVO_PIN, VAL_OPEN)
        time.sleep(1.5) # 給它 1.5 秒的時間去動作

        # 動作 2: 閉合
        print(f"-> 閉合 (PWM: {VAL_CLOSE})")
        pi.set_servo_pulsewidth(SERVO_PIN, VAL_CLOSE)
        time.sleep(1.5) # 給它 1.5 秒的時間去動作

except KeyboardInterrupt:
    print("\n使用者中斷測試")

finally:
    # 這是最重要的保護機制
    print("-> 放鬆馬達 (設為 0)")
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    pi.stop()
    print("程式結束")