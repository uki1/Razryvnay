
#include "hx711.h"

Hx711 scale(A5, A4);


// Hx711.DOUT - pin #A2
// Hx711.SCK - pin #A1

void setup() {

  Serial.begin(9600);

}

void loop() {
  long mas=0;
  sens(97.7, 10);
  mas += scale.getGram();
  sens(9860, 6);
  mas += scale.getGram();
  sens(97800, 8);
  mas += scale.getGram();
  sens(9460000, 12);
  mas += scale.getGram();
  sens(974, 4);
  mas += scale.getGram();
  sens(972000, 2);
  Serial.print(mas/5.0, 1);
  Serial.println(";-");
}

void sens(float resist, int port){
  pinMode(port, OUTPUT);
  digitalWrite(port, HIGH);

  delay(10);

  float sum = 0;
  int tim = 5;

  for (byte i = 0; i < tim; i++)
  {
    delay(10);
    sum += analogRead(A0);
  }


  float sensorValue = sum / float(tim);
  float R = resist / ((5.0 / ((5.0 / 1023.0) * sensorValue)) - 1);

  Serial.print(R);

  if (sensorValue>512){
    sensorValue = sensorValue -(2*(sensorValue-512));
  }
  Serial.print(";");
  Serial.println(sensorValue);  

  digitalWrite(port, LOW);
  pinMode(port, INPUT);
  delay(10);
}







