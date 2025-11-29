import pigpio
import time
PIN = 18  # 您的夾爪馬達插在 GPIO 18
STEP = 50 # 每次按鍵增加或減少的脈衝量 (微調精度)

current_pulse = 1500
print("正在連線到 pigpiod...")
pi = pigpio.pi()

if not pi.connected:
    print("❌ 錯誤：pigpiod 服務沒開！(sudo systemctl start pigpiod)")
    exit()
print(" [a] 減少脈衝 (夾緊/張開?) -50")
print(" [d] 增加脈衝 (張開/夾緊?) +50")
print(" [m] 回到中間 (1500)")
print(" [0] 放鬆馬達 (緊急停止!)")
print(" [q] 離開程式")

try:
    # 先回到中間
    pi.set_servo_pulsewidth(PIN, current_pulse)
    print(f"目前位置: {current_pulse}")

    while True:
        cmd = input("請輸入指令 (a/d/m/0/q): ").strip().lower()

        if cmd == 'a':
            current_pulse -= STEP
            # 安全限制，不讓它低於 600
            if current_pulse < 600: current_pulse = 600
            print(f"-> 調整至: {current_pulse}")
            pi.set_servo_pulsewidth(PIN, current_pulse)

        elif cmd == 'd':
            current_pulse += STEP
            # 安全限制，不讓它高於 2400
            if current_pulse > 2400: current_pulse = 2400
            print(f"-> 調整至: {current_pulse}")
            pi.set_servo_pulsewidth(PIN, current_pulse)

        elif cmd == 'm':
            current_pulse = 1500
            print(f"-> 回到中間: {current_pulse}")
            pi.set_servo_pulsewidth(PIN, current_pulse)

        elif cmd == '0':
            print("-> ⛔️ 馬達已放鬆 (停止出力)")
            pi.set_servo_pulsewidth(PIN, 0)
            
        elif cmd == 'q':
            break
            
        else:
            print("指令錯誤，請輸入 a, d, m, 0 或 q")

        # 稍微暫停，避免連點
        # 這裡不 sleep 太久，保持反應靈敏

except KeyboardInterrupt:
    print("\n中斷")

finally:
    print("結束程式，放鬆馬達...")
    pi.set_servo_pulsewidth(PIN, 0)
    pi.stop()
