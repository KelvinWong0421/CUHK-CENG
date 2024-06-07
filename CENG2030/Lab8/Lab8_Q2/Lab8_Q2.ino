#include <Servo.h>

const int irPin = 2;
const int ledPin = 13;

Servo myservo; // create servo object to control a servo
int pos = 0; // variable to store the servo position
int state = 0;
int nowSensorOut = 0;

void setup() {
  myservo.attach(9); // attaches the servo on pin 9 to the servo object
  pinMode(irPin, INPUT);
  pinMode(ledPin,OUTPUT);
}

void loop() {
  nowSensorOut = digitalRead(irPin);

  // LED on/off
  digitalWrite(ledPin, (nowSensorOut)?HIGH:LOW);

// Rotate Motor
  if (nowSensorOut) {
    state = 1 - state;

    if (state) {
      for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo.write(pos); // tell servo to go to position in variable 'pos'
        delay(15); // waits 15ms for the servo to reach the position
      }
    } else {
      for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
        myservo.write(pos); // tell servo to go to position in variable 'pos'
        delay(15); // waits 15ms for the servo to reach the position
      }
    }
  }
}
