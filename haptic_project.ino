#include <math.h>
// PIN Declare
int pwmPin = 5; // PWM output pin for motor up
int dirPin = 8; // direction output pin for motor up
int dirPin2 = 9; // 2nd direction output pin for motor up
int encPin1 = 2; // encoder read pin 1
int encPin2 = 3; // encoder read pin 2
int triggerPin = 0; // pin for trigger TODO
int pwmPin2 = 6; // PWM output pin for motor down
int dirPin3 = 7; // direction output pin for motor down
int dirPin4 = 10; // 2nd direction output pin for motor down
int encPin3 = 12; // encoder read pin 1
int encPin4 = 13; // encoder read pin 2
// Position tracking variables
int trigger = 0;
int updatedPos_up = 0;     // keeps track of the encoder position for motor up
int rawPos_up = 0;      // rawpos for motor up
int lastRawPos_up = 0;     // last raw reading from the encoder
int updatedPos_down = 0;     // keeps track of the encoder position for motor down
int rawPos_down = 0;      // rawpos for motor down
int lastRawPos_down = 0;     // last raw reading from the encoder
int EncLookup [4][4] = {
                        {0, -1, +1, 0},
                        {+1, 0, 0, -1},
                        {-1, 0, 0, +1},
                        {0, +1, -1, 0}
                        };  // encoder increment lookup table
// convert
//drive wheel angle
double th1 = 0;
double th2 = 0;
float pos_x = 0;
float pos_y = 0;
float L = 12; // in centimeters TODO
// Velocity tracking and filtering
double curr_time = 0;

void setup() 
{
  // Set up serial communication
  Serial.begin(115200);
  
  // Set PWM frequency 
  setPwmFrequency(pwmPin,1); 
  setPwmFrequency(pwmPin2,1); 
  // Input pins
  pinMode(encPin1,INPUT);       // set encoder pin 1 to be an input
  pinMode(encPin2,INPUT);       // set encoder pin 2 to be an input
  pinMode(encPin3,INPUT);       // set encoder pin 3 to be an input
  pinMode(encPin4,INPUT);       // set encoder pin 4 to be an input
  pinMode(triggerPin, INPUT);
  // Output pins
  pinMode(pwmPin, OUTPUT);  // PWM pin for motor up
  pinMode(pwmPin2, OUTPUT);  // PWM pin for motor down
  pinMode(dirPin, OUTPUT);  // dir pin for motor A
  pinMode(dirPin2,OUTPUT);   // second dir pin for motor B
  pinMode(dirPin3, OUTPUT);  // dir pin for motor B
  pinMode(dirPin4,OUTPUT);   // second dir pin for motor B
  
  // Initialize motor 
  analogWrite(pwmPin, 0);     // set to not be spinning (0/255)
  analogWrite(pwmPin2, 0);     // set to not be spinning (0/255)
  digitalWrite(dirPin, LOW);  // set direction
  digitalWrite(dirPin2,LOW);
  digitalWrite(dirPin3, LOW);  // set direction
  digitalWrite(dirPin4,LOW);
  // Initialize position variables
  lastRawPos_up = (digitalRead(encPin1) + 2 * digitalRead(encPin2)) & (0b11);
  lastRawPos_down = (digitalRead(encPin3) + 2 * digitalRead(encPin4)) & (0b11); 
}


void loop() {
  curr_time = millis()/64.0; // get the current time but scale it because we adjusted the timers for the PWM.
  rawPos_up = (digitalRead(encPin1) + 2 * digitalRead(encPin2)) & (0b11);
  rawPos_down = (digitalRead(encPin3) + 2 * digitalRead(encPin4)) & (0b11);
  int encInc_up = EncLookup[lastRawPos_up][rawPos_up];
    if (encInc_up == -1 || encInc_up == 1) {
      updatedPos_up -= encInc_up;
    }
  lastRawPos_up = rawPos_up;
  int encInc_down = EncLookup[lastRawPos_down][rawPos_down];
    if (encInc_down == -1 || encInc_down == 1) {
      updatedPos_down += encInc_down;
    }
  lastRawPos_down = rawPos_down;
  th1 = map(updatedPos_up, 13, -196, 90, 0); 
  th2 = map(updatedPos_down, -202, 6, 0, 90);
  double th1_rad = th1/180 * PI;
  double th2_rad = th2/180 * PI;
  // Serial.println(String(updatedPos_up) + "," + String(updatedPos_down));
  // Serial.println(String(th1) + "," + String(th1_1));  
  double ph1= (th1_rad + th2_rad)/2;
  double ph2= (th1_rad - th2_rad)/2;
  pos_x = sqrt(2 * (1 - cos(ph1 * 2))) * L * sin(ph2);
  pos_y = sqrt(2 * (1 - cos(ph1 * 2))) * L * cos(ph2);
  float pos_x_game = -1024 * (pos_x - 12.5)/25;
  float pos_y_game =  1024 * (pos_y - 9)/11 ;
  Serial.println(String(pos_x_game) + "," + String(pos_y_game) + "," + String(trigger));
  double Jacob [2][2]={ 
    {L/2 * (sin(ph1) * cos(ph2) + sin(ph2)*cos(ph1)) , L/2 * (sin(ph2)*cos(ph1) - sin(ph1)*cos(ph2))},
    {L/2 * (cos(ph1) * cos(ph2) - sin(ph2)*sin(ph1)) , L/2 * (cos(ph1)*cos(ph2) + sin(ph2)*sin(ph1))}
  };
  // double Torque [2][1] = Jacob * Force;
  // TODO





}


void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    } else {
      TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x7; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}
