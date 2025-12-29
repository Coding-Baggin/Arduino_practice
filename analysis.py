import pandas as pd  
import matplotlib.pyplot as plt

# 1. 데이터 불러오기
try:
    df = pd.read_csv('distance_log.csv')
except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 먼저 main.py를 실행해서 데이터를 쌓아주세요.")
    exit()

# 2. 데이터 클리닝 (공학적 판단)
# 거리가 0이거나 200cm 이상인 데이터는 센서 오류로 간주하고 제거합니다.
df_clean = df[(df['Distance'] > 0) & (df['Distance'] < 200)].copy()

# 3. 데이터 부드럽게 만들기 (Moving Average - 이동 평균 필터)
# 5개의 데이터를 평균 내서 튀는 값을 억제합니다. (현업 필수 기술!)
df_clean['Moving_Avg'] = df_clean['Distance'].rolling(window=5).mean()
#df_clean['Moving_Avg']라는 column을 추가후, rolling:데이터를 하나씩 훑으며 내려감, 5개씩 보고(window=5) 평균을 냄
#window 조절해가면서 적절한 데이터 값을 찾음, 작으면 노이즈 제거 효과 x, 너무 크면 너무 느림

# 4. 시각화 비교
plt.figure(figsize=(10, 5)) 
#자, 이제 보고서를 붙일 **전시판(Figure)**을 가져와! 크기는 가로 10, 세로 5 비율로 널찍하게 준비해.
plt.plot(df['Time'], df['Distance'], 'gray', alpha=0.3, label='Raw Data (Original)')
#x축, y축, alpha = 투명도
plt.plot(df_clean['Time'], df_clean['Moving_Avg'], 'r-', linewidth=2, label='Filtered Data (Moving Avg)')

plt.title('Sensor Data Filtering')
plt.xlabel('Time (s)')
plt.ylabel('Distance (cm)')
plt.legend() #범례 (labeling 한것) 달아줘
plt.grid(True)#모눈종이 눈금을 그려줘
plt.show()#이제 화면에 띄워라
