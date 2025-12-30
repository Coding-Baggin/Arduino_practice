#include <Servo.h>
/*servomotor는 단순히 HIGH/LOW 전압으로 작동하지 않고 전압의 width를 통해 각도를 modulate하는데 
우리가 직접 microseconds를 통해 전압의 시간을 조절하면 오차가 자주 생기기 때문에 servo library를 사용*/
Servo myServo;  // 서보 모터 객체 생성
/*Servo.h가 설계도라면, 이 설계도를 myServo라는 객체에 직접 설계도를 주입하는 것*/

void setup() {
  Serial.begin(9600); // 파이썬과 대화할 통로
  Serial.setTimeout(10); //parseInt가 숫자를 기다리는 시간을 1초에서 0.01초로 단축
  /*이렇게 하지 않으면 parseInt가 120을 보고 \n를 읽기전까지 잠깐 멈추는 그 1초 사이에 python이 in_waiting
  buffer를 읽게 됨으로써 바로 전의 응답을 읽지 못하고 이전의 응답을 읽게됨)*/
  myServo.attach(9);  // 9번 핀에 서보 모터 연결, 설계도가 있는 myServo가 어디에 연결되어 있는지를 설정
  myServo.write(90);  
  // 시작할 때 정중앙(90도) 보기, 90도가 직진 상태임, 이거 없으면 마지막 각도 그대로 있거나 전원이 들어오면 무작위로 튈 수 있음
  Serial.println("Servo System Ready!"); //나중에 디버깅 할 때 편함, 기계 시스템에서는 초기화 하는 것이 중요함
}

void loop() {
  // 파이썬으로부터 시리얼 버퍼에 데이터가 들어왔는지 확인 =>available은 들어와 있는 데이터의 양을 알려줌
  /*컴퓨터는 굉장히 빠른 속도로 정보를 보내지만 아두이노는 센서를 재거나 모터를 돌리느라 바빠 못 볼 수 있음
  => 임시 저장 공간인 시리어 버퍼를 통해 데이터가 날아가지 않도록 함*/
  if (Serial.available() > 0) {
    /* 버퍼에 들어온 데이터를 몽땅 다 정수로 읽음 (예: "1", "2", "0" -> 120), 숫자를 뱉어냄
    parseInt()는 숫자를 하나씩 실제로 꺼냄 =>그러 버퍼는 다시 비워지고 available()은 0이 됨
    만약 문자가 같이 있다면 available은 0이 되지 않고 문자 갯수로 남아있음 => python에서 isdigit으로 제겅*/
    int angle = Serial.parseInt(); 
    
    // 서보 모터가 움직일 수 있는 범위(0~180)인지 확인
    if (angle >= 0 && angle <= 180) {
      myServo.write(angle); // 모터 회전 명령
      
      // 확인을 위해 파이썬으로 응답 보냄
      Serial.print("Moved to: "); 
      //print 함수는 보내기만 하고 줄바꿈은 안함 : 전송 대기줄에 있음(python의 readline 때문)
      Serial.println(angle);// 
      //따로 보내는 이유 => 아두이노의 메모리 아끼기 + 가독성 높이기
    }
  }
}