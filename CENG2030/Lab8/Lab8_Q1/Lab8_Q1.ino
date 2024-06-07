int ledPin = 13; // this number indicates the pin number of the Arduino board
int irPin = 2;

void setup() {
  // set the input & output pins here
  pinMode(ledPin, OUTPUT);
  pinMode(irPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // read the output digital signal from the IR sensor
  // if an obstacle is detected, turn the red LED on
  // if there is no obstacle, turn the red LED off
  int value = digitalRead(irPin);

  digitalWrite(ledPin, (value)? HIGH:LOW);
  Serial.println(value);

  delay(10);
}
