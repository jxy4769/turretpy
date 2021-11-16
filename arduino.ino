#include<Servo.h>

Servo serX;
Servo serY;

String serialData;
int x = 0;
int y = 0;
void setup() {

  serX.attach(9);
  serY.attach(10);
  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  while (!Serial.available());
   serialData = Serial.readString();
   x = parseDataX(serialData);
   y = parseDataY(serialData);
   serX.write(x);
   serY.write(y);
}

int parseDataX(String data){
  data.remove(data.indexOf("Y"));
  data.remove(data.indexOf("X"), 1);
  return data.toInt();
}

int parseDataY(String data){
  data.remove(0,data.indexOf("Y") + 1);
  return data.toInt();
}