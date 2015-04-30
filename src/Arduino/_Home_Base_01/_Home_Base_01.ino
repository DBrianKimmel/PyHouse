/*
 * _Home_Base_01 project
 *
 * Arduino Uno
 * 
 *This is a base line project 
 */
#include<stdlib.h>
#include <SoftwareSerial.h>
SoftwareSerial monitor(0, 1); // RX, TX
// Variables
unsigned long time_start;
unsigned long time_now;


// Include various modules here



// Standard setup and loop
void setup() {
    monitor.begin(9600);
    Serial.begin(9600);
    Serial.println("_Home_Base_01\n");
    time_start = millis();
    time_delay = 0;
    // Include vaarious module setups here.
}
void loop() {
    time_now = millis();
    // Include various module loops here.
}
// ### END DBK

