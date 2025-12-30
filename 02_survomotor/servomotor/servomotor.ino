#include <Servo.h>
Servo myServo; 

void setup() {
  Serial.begin(9600); 
  Serial.setTimeout(10); 

  myServo.attach(9);  
  myServo.write(90);  

  Serial.println("Servo System Ready!"); 
}

void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt(); 
    
    while(Serial.available() > 0) { Serial.read(); } 

    if (angle >= 0 && angle <= 180) {
      myServo.write(angle); 
      
      delay(20);
      Serial.print("Moved to: "); 
      Serial.println(angle);// 
    }
  }
}