import serial
import time
from pynput import keyboard

try:
    py_serial = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    print("포트 연결 중...")
    time.sleep(2) 
except Exception as e:
    print(f"연결 실패: {e}")
    exit()


current_angle = 90


if py_serial.in_waiting > 0:
    first_msg = py_serial.readline().decode().rstrip()
    print(f"아두이노 상태: {first_msg}")

def send_command(angle):
    """아두이노에 각도 명령을 보내는 함수"""
    py_serial.reset_input_buffer()  
    py_serial.write(f"{angle}\n".encode())
    
  
    py_serial.write(f"{angle}\n".encode())


    response = py_serial.readline()


    if response: 
        print(f"아두이노 응답: {response.decode().strip()}")    

def on_press(key):
    global current_angle
    
    try:
        if key == keyboard.Key.left:
            current_angle = max(0, current_angle - 10)
            send_command(current_angle)
        elif key == keyboard.Key.right:
            current_angle = min(180, current_angle + 10)
            send_command(current_angle)
        elif hasattr(key, 'char') and key.char == 'q':

            print("프로그램을 종료합니다.")
            return False  
    except Exception as e:
        print(f"오류 발생: {e}")

print("\n--- 키보드 조향 제어 시작 ---")
print("방향키 [←] [→] 로 조절하세요. 'q'를 누르면 종료합니다.")

with keyboard.Listener(on_press=on_press) as listener:

    listener.join()
py_serial.close()