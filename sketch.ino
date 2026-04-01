// SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL[](http://www.arduino.cc)
//
// SPDX-License-Identifier: MPL-2.0

#include <Arduino_RouterBridge.h>
#include <Servo.h>

const int servoPin  = 9;
const int buzzerPin = 8;

Servo myServo;

void set_servo(int angle) {
  angle = constrain(angle, 0, 180);
  myServo.write(angle);
  delay(600);  // time to reach position – increase if servo moves slowly
}

void buzz(int ms) {
  digitalWrite(buzzerPin, HIGH);
  delay(ms);
  digitalWrite(buzzerPin, LOW);
}

void setup() {
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  myServo.attach(servoPin);
  myServo.write(90);          // Start at default position

  Bridge.begin();
  delay(2000);

  Bridge.provide("set_servo", set_servo);
  Bridge.provide("buzz", buzz);

  // Short double buzz on boot to confirm sketch is running
  buzz(150);
  delay(200);
  buzz(150);
}

void loop() {
  Bridge.update();
}
