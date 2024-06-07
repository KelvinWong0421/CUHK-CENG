int green = 2;
int yellow = 3;
int red = 4;

void setup() {
  // put your setup code here, to run once:
  pinMode(green, OUTPUT); 
  pinMode(yellow, OUTPUT); 
  pinMode(red, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  state_1();
  state_2();
  state_3();
  state_4();
}

void state_1(){
  digitalWrite(red, HIGH);
  digitalWrite(yellow, LOW);
  digitalWrite(green, LOW);

  delay(5000);
}

void state_2() {
  digitalWrite(red, HIGH);
  digitalWrite(yellow, HIGH);
  digitalWrite(green, LOW);

  delay(3000);
}

void state_3() {
  digitalWrite(red, LOW);
  digitalWrite(yellow, LOW);
  digitalWrite(green, HIGH);

  delay(5000);
}

void state_4() {
  digitalWrite(red, LOW);
  digitalWrite(yellow, HIGH);
  digitalWrite(green, LOW);

  delay(3000);
}
