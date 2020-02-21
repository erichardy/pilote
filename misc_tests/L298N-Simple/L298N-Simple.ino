#include <L298N.h>

//pin definition
#define EN 12 // 9
#define IN1 2 // 8
#define IN2 3 // 7

/*
 * NB: les pins utilisées sont celles qui sont laissées disponibles par le module LCD + boutons :
 * https://www.amazon.fr/KEYESTUDIO-r%C3%A9tro%C3%A9clairage-Clavier-caract%C3%A8res-dextension/dp/B07H3Q3X6C/
 * 
 */

//create a motor instance
L298N motor(EN, IN1, IN2);
int i;

void setup() {

  //used for display information
  Serial.begin(9600);

  motor.setSpeed(255); // an integer between 0 and 255
  motor.forward();
  delay(1000);
  motor.backward();
  delay(1000);
}

void loop() {

  //tell the motor to go forward (may depend by your wiring)
  motor.forward();

  //print the motor satus in the serial monitor
  Serial.print("Is moving = ");
  Serial.println(motor.isMoving());

  delay(1000);

  //stop running
  motor.stop();

  Serial.print("Is moving = ");
  Serial.println(motor.isMoving());

  delay(1000);

  //change the initial speed
  // motor.setSpeed(255);

  //tell the motor to go back (may depend by your wiring)
  motor.backward();

  Serial.print("Is moving = ");
  Serial.println(motor.isMoving());

  delay(1000);

  //stop running
  motor.stop();

  Serial.print("Is moving = ");
  Serial.println(motor.isMoving());

  //change the initial speed
  // motor.setSpeed(255);

  Serial.print("Get new speed = ");
  Serial.println(motor.getSpeed());
  delay(3000);
  
  for (i = 0; i < 5; i++) {
    motor.forward();
    delay(100);
    motor.backward();
    delay(100);
  }
  for (i = 0; i < 5; i++) {
    motor.forward();
    delay(200);
    motor.backward();
    delay(200);
  }
  for (i = 0; i < 5; i++) {
    motor.forward();
    delay(500);
    motor.backward();
    delay(500);
  }
  for (i = 0; i < 5; i++) {
    motor.forward();
    delay(1000);
    motor.backward();
    delay(1000);
  }
  
  // delay(1000);
  
}
