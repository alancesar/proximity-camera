#include <Ultrasonic.h>

const int PIN_ECHO = 6;
const int PIN_TRIGGER = 7;

Ultrasonic ultrasonic(PIN_TRIGGER, PIN_ECHO);

float microSecs, cm, minDistance;
bool tuning = true, starting = true;
char incomingByte;

void setup() {
  Serial.begin(9600);
}

void loop() {

  if (starting) {
    minDistance = start();
    starting = false;
    tuning = false;
  }

  if (tuning) {
    minDistance = tune();
    tuning = false;
  }

  if (Serial.available() > 0) {
    incomingByte = Serial.read();

    if (incomingByte == '1') {
      tuning = true;
      return;
    }
  }
  
  if (getDistance() <= minDistance) {
    Serial.println(1);
  } else {
    Serial.println(0);
  }

  delay(1000);
}

float start() {
  delay(4000);
  return tune();
}

float tune() {
  int i = 0;
  float minDistance;

  minDistance = getDistance();
  delay(2000);

  while (i < 5) {
    cm = getDistance();

    if (cm > minDistance) {
      minDistance = cm;
    }

    delay(2000);
    i++;
  }

  return minDistance * .9;
}

float getDistance() {
  int micSecs = ultrasonic.timing();
  return ultrasonic.convert(micSecs, Ultrasonic::CM);
}

