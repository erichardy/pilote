
#include <Wire.h>
#include <L298N.h>

//pins definition
// test mouvement moteur : 4 entre les pins i2c et les pins de commande du moteur
#define moveMotor 4
// Moteur : les pins 17, 27, 22 sont contigues
#define EN 9 // 9
#define IN1 8 // 8
#define IN2 7 // 7

// paramètres i2c
int adnAdress = 0x8;

// paramètres moteur
L298N motor(EN, IN1, IN2);
int i;

// divers
int steering; // la direction : babord / tribord
const int babord = 98;
const int tribord = 116;
unsigned long duration; // la durée de déplacement du vérin en milli-secondes. 5 digits, ex: 11025 (11.025 secondes)
unsigned long currentTime;
unsigned long x_currentTime = 0;
// 

void receiveCmd() {
  int nbl, nb, i, c ;
  String x_duration;
  nbl = Wire.available();
  // cmd : réception du sens, babord / tribord
  steering = Wire.read();
  nb = Wire.read(); // normalement doit toujours être égal à 5 !!!
  for (i = 0; i < nb; i++) {
    c = Wire.read();
    x_duration += char(c);
  }
  duration = x_duration.toInt();
  currentTime = micros();
}

void setup() {
  // initialisation i2c
  Wire.begin(adnAdress);                // join i2c bus with address #8
  Wire.onReceive(receiveCmd);
  
  //used for display information
  Serial.begin(9600);
  
  // initialisation moteur
  motor.setSpeed(255); // an integer between 0 and 255
  motor.forward();
  delay(1000);
  motor.backward();
  delay(1000);
  motor.stop();
}

void move(char steer, int dur){
  if (steer == 'b') {
    motor.forward();
  } else {
    motor.backward();
  }
  delay(dur);
  motor.stop();
}

void loop() {
  delay(500);
  if (x_currentTime != currentTime) {
    // send command to motor !!!
    Serial.print(char(steering));
    
    Serial.print(" / ");
    Serial.print(duration);
    Serial.print(" / ");
    Serial.print(duration + 10000);
    x_currentTime = currentTime;
    Serial.println(" ...");
    move(steering, duration);
  }

}
