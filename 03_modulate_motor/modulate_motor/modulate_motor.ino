#include <Servo.h>

Servo myServo; 
const int servoPin = 9; // 서보 모터 연결 핀

void setup() {
  Serial.begin(9600); 
  // 파이썬 숫자를 읽을 때 0.01초만 기다리도록 설정 (Flow 4번 반영)
  Serial.setTimeout(10); 
p
  myServo.attach(servoPin);  
  myServo.write(90); // 초기 각도 정중앙

  // 파이썬이 부팅을 확인할 수 있도록 인사말 전송 (Flow 2번 반영)
  Serial.println("Servo System Ready!"); 
}

void loop() {
  if (Serial.available() > 0) {
    // 1. 숫자 읽기
    int angle = Serial.parseInt(); 
    
    // 2. 버퍼에 남은 줄바꿈 문자 등 찌꺼기 청소 (Flow 5번 반영)
    while(Serial.available() > 0) { 
      Serial.read(); 
    } 

    // 3. 각도 범위 확인 및 동작 (Flow 6번 반영)
    if (angle >= 0 && angle <= 180) {
      myServo.write(angle); 
      delay(50); // 모터가 움직일 최소 시간 보장
      
      // 4. 결과를 파이썬으로 다시 보고 (Flow 6번 반영)
      Serial.print("Moved to: "); 
      Serial.println(angle);
    }
  }
}