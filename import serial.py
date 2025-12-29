import serial                   
import time                     
import pandas as pd              
import matplotlib.pyplot as plt 


port = 'COM3' 
baud = 9600
py_serial = serial.Serial(port, baud, timeout=1)  


distances = []
times = []
start_time = time.time()

print("--- 데이터 수집 및 그래프 시작 (Ctrl+C로 종료) ---")

try: 
    plt.ion() 
    fig, ax = plt.subplots()            
    line, = ax.plot([], [], 'r-') 
  
    ax.set_ylim(0, 100) 
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Distance (cm)')

    while True:
        if py_serial.readable():   
            res = py_serial.readline().decode().strip()

            if res.isdigit(): 
                val = int(res)
                curr_time = time.time() - start_time


                distances.append(val)
                times.append(curr_time)
                
                
                line.set_data(times, distances) 
                ax.set_xlim(max(0, curr_time - 10), curr_time + 1) 

                plt.pause(0.01)
                
                print(f"시간: {curr_time:.1f}s, 거리: {val}cm")

except KeyboardInterrupt:
    df = pd.DataFrame({'Time': times, 'Distance': distances})
    df.to_csv('distance_log.csv', index=False) 
    print("\n--- 데이터 저장 완료: distance_log.csv ---")
    plt.close() 

