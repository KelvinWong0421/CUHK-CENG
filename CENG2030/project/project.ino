const int ledpin = 13;
const int analogpin = A5;
const int threshold = 550;

bool pulseCounted = false;
int pulseCount = 0;
int rawPulseValue = 0;
int PulseRate = 0;

void setup() {
  Serial.begin(9600);

  // setup for led
  pinMode(ledpin, OUTPUT);
  digitalWrite(ledpin, LOW);   // turn the LED on (HIGH is the voltage level)
}

void loop() {
  // Read rawpulse
  rawPulseValue = analogRead(analogpin);

  // compare and on off pulsecounted
  if (rawPulseValue > threshold) {
    digitalWrite(ledpin, HIGH);
    if (!pulseCounted) {
      pulseCount++;
      pulseCounted = true;
    }
  } else {
    digitalWrite(ledpin, LOW);
    pulseCounted = false;
  }

  // Calculate pulserate
  PulseRate = pulseCount * 60000/ millis() ;

  // Print pulse and heart rate
  Serial.print("SignalLevel:");
  Serial.print(rawPulseValue);
  Serial.print(",");
  Serial.print("PulseRate:");
  Serial.println(PulseRate);
}
