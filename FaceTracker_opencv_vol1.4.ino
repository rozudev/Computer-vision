#include <Servo.h>

Servo servo_tilt;
Servo servo_pan;

String inputString = "";
int x_axis = 320;
int y_axis = 240;
int servoX = 90;
int servoY = 90;
int lastX = 90;
int lastY = 90;

void setup() {

  servo_tilt.attach(10); // up-down
  servo_pan.attach(9); // left-right
  servo_tilt.write(90);
  servo_pan.write(90);

  Serial.begin(115200);

}

void loop() {
 
 if (Serial.available()) {
  inputString = Serial.readStringUntil('\n');

  int commaIndex = inputString.indexOf(',');

  if (commaIndex > 0){
    x_axis = inputString.substring(0, commaIndex).toInt();
    y_axis = inputString.substring(commaIndex + 1).toInt();

    // Map camera to servo angles
    int targetX = map(x_axis, 0, 640, 0, 180);
    int targetY = map(y_axis, 0, 480, 0, 180);

    // Smooth movement 
    servoX = servoX + (targetX - servoX) *0.6;
    servoY = servoY + (targetY - servoY) *0.6;

    if (abs(servoX - lastX) >2) {
      servo_pan.write(servoX);
      lastX = servoX;
    }
    if (abs(servoY - lastY) >2) {
      servo_tilt.write(servoY);
      lastY = servoY;
    } 
  }
 }

}