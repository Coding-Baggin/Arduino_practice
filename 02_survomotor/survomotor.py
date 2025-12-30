import serial
import time

# 아두이노 연결 설정 (timeout=1 추가)
# 1초 동안 데이터가 안 오면 기다리기를 멈추고 다음 코드로 진행함
py_serial = serial.Serial(port='COM3', baudrate=9600, timeout=1)

print("--- 서보 모터 제어 프로그램 ---")
print("각도를 입력하세요 (0~180). 종료하려면 'q'를 누르세요.")

while True:
    command = input("Angle: ")
    
    if command.lower() == 'q':
        break
    
    # 입력값이 숫자인지 확인
    if command.isdigit():
        # 아두이노로 각도 전송 (문자열 전송 후 인코딩)
        py_serial.write(command.encode())
        time.sleep(0.1) # 아두이노가 처리할 시간을 잠시 줌
        
        # 아두이노로부터 온 확인 메시지 읽기
        if py_serial.in_waiting > 0:
            response = py_serial.readline().decode().rstrip()
            print(f"아두이노 응답: {response}")
    else:
        print("0에서 180 사이의 숫자만 입력해주세요.")

py_serial.close()
print("프로그램을 종료합니다.")
