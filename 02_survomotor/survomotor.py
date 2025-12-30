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

        py_serial.reset_input_buffer() #명령을 내리기 전에 우편함에 쌓여 있던 데이터 버림

        py_serial.write(f"{command}\n".encode()) #\n은 끝났다는 의미
        time.sleep(0.1) 
        # 아두이노로 write 안에 있는 것 전송! encode를 통해 문자열을 byte로 바꿔줌 
        # 아두이노가 처리할 시간을 잠시 줌 => 컴퓨터는 연산이 굉장히 빠르지만 아두이노는 처리할 시간이 필요함 
        
        # 아두이노로부터 온 확인 메시지 읽기
        if py_serial.in_waiting > 0: 
        #Serial.available의 python.version =>수신 버퍼에 데이터가 있니, 없는데 readline으로 읽으려고 하면 오류남
             response = py_serial.readline().decode().rstrip()
             #readline은 줄바꿈이 있어야 읽음, rstrip이나 strip이나 결과는 같은데 println은 데이터 끝에 줄바꿈 관련 기호들을
             #보내기 때문에 목적을 명확하게 하기 위해서 rstrip을 사용함
             print(f"아두이노 응답: {response}")
    else:
        print("0에서 180 사이의 숫자만 입력해주세요.")

py_serial.close()
print("프로그램을 종료합니다.")

#아두이노랑 파이썬의 버퍼를 고려하고 응답 속도를 고려하는게 되게 쉽지 않다. 이것을 잘 연습해야 할 것 같다.
