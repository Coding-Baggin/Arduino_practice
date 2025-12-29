import serial                   #Arduino와 연결하기 위해
import time                     #그래프에서 시간을 나타내기 위해
import pandas as pd             #데이터를 엑셀 형식으로 저장하기 위해 
import matplotlib.pyplot as plt #matplotlib에서 그래프 그리는 기능 불러오기

# 설정
port = 'COM3' # 본인의 포트 번호로 확인!
baud = 9600
py_serial = serial.Serial(port, baud, timeout=1)  
# computer에서 이 port를 열고 baud의 속도로 기다릴테니 맞춰보내라는 규격
# timeout은 1초 동안 데이터가 안 들어오면 빈 데이터 값을 할당함 
# -> if문에서 걸려서 그래프는 정지함, 다시 데이터가 들어오면 직선으로 한번에 연결됨(pyplot의 성질 - 점을 연결)
#함수의 결과 값은 byte 데이터로 들어옴

distances = []
times = []
start_time = time.time()

print("--- 데이터 수집 및 그래프 시작 (Ctrl+C로 종료) ---")

try: #try except 구조는 ctrl + c를 눌렀을 때 메모리에 있던 데이터를 한번에 하드디스크에 저장하기 위한 장치이다.
    plt.ion() # 실시간 그래프 모드 켜기
    fig, ax = plt.subplots()            #그래프를 그릴 장비 (책상 :fig, 종이 :ax) setting
    line, = ax.plot([], [], 'r-') 
#r- : 빨간색, 실선, ax.plot은 원래 list 형태로 값을 주기 때문에 그 안에 객체 하나만 가져오기 위해서 ,씀
  
    ax.set_ylim(0, 100) # 거리 범위 0~100cm 설정, 이렇게 안 하면 눈금 계속 바뀜
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Distance (cm)')

    while True:
        if py_serial.readable():    #하드웨어/ 통로 체크 : 읽을 수 없는 상태에서 억지로 readline 하면 프로그램 에러
            res = py_serial.readline().decode().strip()
#b'15\r\n'데이터를 읽음 : readline ->'15\r\n'로 만들어줌 : decode 
# -> '15'(문자열) \r(다음 맨 줄 앞으로 가서 시작)이나 \n을 없애줌: strip'
            if res.isdigit(): 
# 아두이노에서 보내준 데이터 값이 순수한 숫자가 아닌 '15b' 같은 노이즈로 찍혔을 때를 대비함
# 에러가 나면 프로그램이 죽기 때문에 int로 바꾸는 작업을 if문으로 숫자로 들어온 것을 확인하고 바꿔줌
                val = int(res)
                curr_time = time.time() - start_time
#그래프에 찍히는 시간 : 현재 시간 - 처음 시각

                distances.append(val)
                times.append(curr_time)
                
                # 그래프 업데이트
                line.set_data(times, distances) #지금까지 리스트에 있는 것으로 다시 그려
                ax.set_xlim(max(0, curr_time - 10), curr_time + 1) # 최근 10초 데이터만 보기
#set_xlim(왼쪽 끝, 오른쪽 끝) : 가로축 범위 강제 지정, curr_time + 1 : 현재 시간보다 앞선 미래 공간 : 가독성
#슬라이딩 윈도우 기법, max 함수로 음수인 부분 제거
                plt.pause(0.01)
#잠깐 쉬는 동안 그래프를 다시 그려(실시간으로 그래프가 움직여야 할 때, 사용자가 창을 마우스로 조작할 때 주로 사용)
                
                print(f"시간: {curr_time:.1f}s, 거리: {val}cm")

except KeyboardInterrupt:
    # 종료 시 데이터 저장
    df = pd.DataFrame({'Time': times, 'Distance': distances})
    df.to_csv('distance_log.csv', index=False)  
    #pandas는 기본적으로 행 번호를 같이 저장하려고 하는데 index False로 없앰, 시간이 있기 때문임 + 간결, 효율
    print("\n--- 데이터 저장 완료: distance_log.csv ---")
    plt.close() # 열린 창을 강제로 닫음

