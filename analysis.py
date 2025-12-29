import pandas as pd  
import matplotlib.pyplot as plt


try:
    df = pd.read_csv('distance_log.csv')
except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 먼저 main.py를 실행해서 데이터를 쌓아주세요.")
    exit()


df_clean = df[(df['Distance'] > 0) & (df['Distance'] < 200)].copy()


df_clean['Moving_Avg'] = df_clean['Distance'].rolling(window=5).mean()



plt.figure(figsize=(10, 5)) 
plt.plot(df['Time'], df['Distance'], 'gray', alpha=0.3, label='Raw Data (Original)')
plt.plot(df_clean['Time'], df_clean['Moving_Avg'], 'r-', linewidth=2, label='Filtered Data (Moving Avg)')

plt.title('Sensor Data Filtering')
plt.xlabel('Time (s)')
plt.ylabel('Distance (cm)')
plt.legend() 
plt.grid(True)
plt.show()
