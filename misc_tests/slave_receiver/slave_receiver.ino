// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


#include <Wire.h>

int cc, x, z, nb, cmd;
long nbl;
char c;
char *str ;
char msg[6] = {'0','1','2','3','4','5'};
int i = 0;
String xheading;
float heading;
unsigned long currentTime;
unsigned long currentTime2;

void setup() {
  Serial.begin(9600);
  // Random
  randomSeed(100);
  
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  // NB: la réception déclenche une interruption.
  // Wire.onRequest(sendEvent);
  Serial.println("i2c init") ;
}

void loop() {
  delay(200);
  Serial.print(heading);
  // histoire de vérifier que c'est bien un float, on ajoute 1.1 !
  Serial.print(" (+ 1.1 = ");
  Serial.print(heading + 1.1);
  Serial.println(")");
  Serial.print(currentTime);
  Serial.print(" ");
  Serial.println(currentTime2);
  // Serial.println("Ready...");
}

void sendEvent(){
  // ok aussi avec msg
  // Wire.write(msg);
  str = "azeaze";
  Wire.write(str);
  // la valeur lue par le RPi (read_i2c_block_data) est un tableau des codes ASCII
  // !!! attention : ne pas utiliser read_block_data sur le RPi !!!
}

void receiveEvent() {
  currentTime = millis();
  nbl = Wire.available();
  // Serial.print("nb = ");
  // Serial.println(nbl);
  cmd = Wire.read();
  // Serial.print("cmd = ");
  // Serial.println(cmd);
  nb = Wire.read();
  // Serial.print("nb = ");
  // Serial.println(nb);
  int li[nb];
  xheading = "";
  for (i = 0; i < nb; i++){
    /*
    li[i] = Wire.read();
    xheading += char(li[i]);
    */
    xheading += char(Wire.read());
  }
  heading = xheading.toFloat();
  currentTime2 = millis();
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void XreceiveEvent(int howMany) {
  while (1 < Wire.available()) { // loop through all but the last
    c = Wire.read(); // receive byte as a character
  }
  x = Wire.read();    // receive byte as an integer
  Serial.println(x);         // print the integer
}
