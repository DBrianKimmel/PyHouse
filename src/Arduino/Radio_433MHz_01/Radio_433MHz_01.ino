/*
 * WiFi_01
 *
 * Arduino Uno
 * 
 *This is a base line project 
 */
#include<stdlib.h>
#include <SoftwareSerial.h>
SoftwareSerial monitor(5, 7); // RX, TX
// Include various modules here


// Module Radio_433_MHz_01 - Radio Receiver
#include <RCSwitch.h>    // C:\Users\briank\Downloads\Projects\libraries\RCSwitch (legacy)

// Pins
#define RADIO_PIN  2
#define RADIO_INTERRUPT  0

RCSwitch radio433 = RCSwitch();

void radio433_setup() {
    Serial.println("Setup Start.");
    radio433.enableReceive(RADIO_INTERRUPT);    // Receiver on inerrupt 0 => that is pin #2
}

void radio433_loop() {
    if (radio433.available()) {
        int value = radio433.getReceivedValue();
        if (value == 0) {
            Serial.print("Unknown encoding");
        } else {
            Serial.print("Received ");
            Serial.print( radio433.getReceivedValue() );
            Serial.print(" / ");
            Serial.print( radio433.getReceivedBitlength() );
            Serial.print("bit ");
            Serial.print("Protocol: ");
            Serial.println( radio433.getReceivedProtocol() );
        }
        radio433.resetAvailable();
    } else {
        Serial.println("Not Available.");
        delay(3*1000);
    }
}




// Standard setup and loop
void setup() {
    monitor.begin(9600);
    Serial.begin(9600);
    Serial.println("Radio_433_MHz_01\n");
    // Include vaarious module setups here.
    radio433_setup();
}
void loop() {
    // Include various module loops here.
    radio433_loop();
}

// ### END DBK

