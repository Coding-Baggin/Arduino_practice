const int echoPin = 8;
const int trigPin = 9;

void main(){
  Serial.begin(9600)
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
}

void loop(){
  digitalWrite(trigPin, LOW);
  delay(2);
  digitalWrite(trigPin,HIGH);
  delay(10);
  digitalWrite(trigPin,LOW);
  delay(2);

  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.017;
  Serial.println(distance);
  delay(100);  
  
  }