#include <Servo.h>

// Pins
const int sensorLeftPin = A4;
const int sensorRightPin = A5;
const int servoPin = 11;

// Variables 
Servo servo;
int servoPos = 0;
int sensorLeftAO = 0;
int sensorRightAO = 0;
int headband = 20;

void setup() {
  servo.attach(servoPin);
  servo.write(0);
  Serial.begin(9600);
}

void loop() {
  sensorLeftAO = analogRead(sensorLeftPin);
  sensorRightAO = analogRead(sensorRightPin);

  Serial.print(sensorLeftAO);
  Serial.print(" ");
  Serial.print(sensorRightAO);
  Serial.println();

  // Compare and rotate
  if(sensorLeftAO < sensorRightAO){
    // Rotate left
    if(sensorRightAO- sensorLeftAO > headband && servoPos > 0){
      servo.write(--servoPos);
      delay(30);
    }
  }else if(sensorRightAO < sensorLeftAO){
    // Rotate right
    if(sensorLeftAO- sensorRightAO > headband && servoPos<180){
      servo.write(++servoPos);
      delay(30);
    }
  }
}
