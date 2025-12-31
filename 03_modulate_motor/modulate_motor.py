import serial
import time
from pynput import keyboard

# 1. 시리얼 포트 설정 (본인의 포트에 맞게 COM3 등 수정)
try:
    py_serial = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    print("포트 연결 중...")
    time.sleep(2)  # 아두이노 리셋 대기 (Flow 1번 반영)
except Exception as e:
    print(f"연결 실패: {e}")
    exit()

# 현재 서보 모터의 각도를 파이썬이 관리함
current_angle = 90

# 아두이노의 첫 인사말 확인 (Flow 2번 반영)
if py_serial.in_waiting > 0:
    first_msg = py_serial.readline().decode().strip()
    print(f"아두이노 상태: {first_msg}")

def send_command(angle):
    """아두이노에 각도 명령을 보내는 함수"""
    py_serial.reset_input_buffer()  # 버퍼 청소 (Flow 3번 반영)
    py_serial.write(f"{angle}\n".encode())
    
    # 아두이노의 응답 확인 (Flow 7번 반영)
    time.sleep(0.05)
    if py_serial.in_waiting > 0:
        response = py_serial.readline().decode().strip()
        print(f"확인: {response}")

def on_press(key):
    global current_angle
    
    try:
        if key == keyboard.Key.left:
            # 왼쪽 키: 각도 감소 (최소 0도)
            current_angle = max(0, current_angle - 10)
            send_command(current_angle)
        elif key == keyboard.Key.right:
            # 오른쪽 키: 각도 증가 (최대 180도)
            current_angle = min(180, current_angle + 10)
            send_command(current_angle)
        elif hasattr(key, 'char') and key.char == 'q':
            print("프로그램을 종료합니다.")
            return False  # 리스너 종료
    except Exception as e:
        print(f"오류 발생: {e}")

print("\n--- 키보드 조향 제어 시작 ---")
print("방향키 [←] [→] 로 조절하세요. 'q'를 누르면 종료합니다.")

# 키보드 입력 감지 시작
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

py_serial.close()