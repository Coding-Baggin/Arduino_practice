import serial
import time
from pynput import keyboard
#의미: pynput이라는 외부 라이브러리에서 keyboard와 관련된 기능만 쏙 빼서 쓰겠다는 뜻입니다.
#역할: 파이썬 기본 기능에는 "키보드가 눌리는 순간"을 감시하는 기능이 없습니다. 
# 이 라이브러리를 쓰면 프로그램이 다른 일을 하다가도 키보드 입력(이벤트)이 들어오면 
# 즉시 우리가 만든 on_press 함수를 실행해줍니다.

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
    first_msg = py_serial.readline().decode().rstrip()
    print(f"아두이노 상태: {first_msg}")

def send_command(angle):
    """아두이노에 각도 명령을 보내는 함수"""
    py_serial.reset_input_buffer()  # 버퍼 청소 (Flow 3번 반영)
    py_serial.write(f"{angle}\n".encode())
    
    # 아두이노의 응답 확인 (Flow 7번 반영)
    # 1. 일단 아두이노에게 명령 전송
    py_serial.write(f"{angle}\n".encode())

    # 2. if문 없이 바로 읽기 시도 (설정된 timeout만큼 알아서 기다림)
    response = py_serial.readline()

    # 3. 읽어온 데이터가 비어있지 않을 때만 출력 (안전장치)
    if response: 
        print(f"아두이노 응답: {response.decode().strip()}")    

def on_press(key):
    global current_angle
    
    try:
        if key == keyboard.Key.left:
        #keyboard(내의) (특수) Key (중에) left 라는 의미
            # 왼쪽 키: 각도 감소 (최소 0도)
            current_angle = max(0, current_angle - 10)
            send_command(current_angle)
        elif key == keyboard.Key.right:
            # 오른쪽 키: 각도 증가 (최대 180도)
            current_angle = min(180, current_angle + 10)
            send_command(current_angle)
        elif hasattr(key, 'char') and key.char == 'q':
        #특수키 이외의 일반 글자키는 char라는 자료형에 담겨 있는데 우선 이 주머니가 있는지 물어보고
        #그 안에 있는 글자가 q인지 확인하는 것, hasattr = has attribute라는 뜻
            print("프로그램을 종료합니다.")
            return False  # 리스너 종료, return 값이 없으면 None(True, None일때 Listener 진행됨)
    except Exception as e:
        print(f"오류 발생: {e}")

print("\n--- 키보드 조향 제어 시작 ---")
print("방향키 [←] [→] 로 조절하세요. 'q'를 누르면 종료합니다.")

# 키보드 입력 감지 시작
with keyboard.Listener(on_press=on_press) as listener:
#keyboard.Linstener가 keyboard가 눌리는지 계속 감시 => on_press라는 함수에 어떤 key가 눌리는지 전달 
# as listener은 길게 부르기 귀찮으니 keyboard.Listener을 앞으로 listener라고 부르는 것
#with : 지금부터 keyboard.Listener 시작 => listener라고 부름 => 
    listener.join()
    #python의 코드가 끝났더라도 키보드를 감시하는 listener 종료 전까지 계속 진행됨 
py_serial.close()