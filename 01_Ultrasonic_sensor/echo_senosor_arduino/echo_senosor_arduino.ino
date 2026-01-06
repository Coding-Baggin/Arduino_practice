const int trigPin = 9;
const int echoPin = 8;
/*const int로 둔 이유
1.코드가 길어질 때 섞어 쓸 수도 있는데 그것을 걸러주는 역할을 함
2.아두이노의 조그마한 저장용량을 조금이나마 아낄 수 있음
*/


void setup() {
  Serial.begin(9600); // 파이썬과 맞출 통신 속도
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 17 / 1000;

  // 파이썬이 읽기 쉽게 숫자만 한 줄씩 출력
  Serial.println(distance); 
  delay(100); // 0.1초마다 데이터 전송
}
/*digitalWrite는 trigPin 즉 OUTPUT으로 전압을 가함, 나의 초음파 sensor는 10 microsecond 이상 전압을 가해져야 전압을 인식함
전압을 인식한 센서는 HIGH로 설정되고 pulseIn을 통해 반사되어 다시 돌아와서 LOW가 되는 시간을 측정함
long으로 저장하는 이유는 int는 3만 언저리까지 저장가능하고 long은 21억까지 저장하기 때문임, 소숫점은 상관 없음
17/1000은 소리의 속도 340m/s는 0.017/microsecond로 나타남 */

/*delay(100)을 쓴 이유는 "이전 초음파가 사라질 때까지 기다려주고(물리적 이유)", 
**"파이썬이 체하지 않게 천천히 떠먹여 주기 위해서(통신적 이유)"**입니다.
최소 delay(60)*/