import serial
import time


py_serial = serial.Serial(port='COM3', baudrate=9600, timeout=1)

print("--- 서보 모터 제어 프로그램 ---")
print("각도를 입력하세요 (0~180). 종료하려면 'q'를 누르세요.")


while True:
    command = input("Angle: ")
    
    if command.lower() == 'q':
        break
    
    if command.isdigit():

        py_serial.reset_input_buffer() 

        py_serial.write(f"{command}\n".encode())
        time.sleep(0.1) 

        if py_serial.in_waiting > 0: 
             response = py_serial.readline().decode().rstrip()
             print(f"아두이노 응답: {response}")
    else:
        print("0에서 180 사이의 숫자만 입력해주세요.")

py_serial.close()
print("프로그램을 종료합니다.")