/*
 * IR project 01
 *
 * Arduino Uno
 * 
 *This is an InfraRed receiver 
 */
#include<stdlib.h>
#include <SoftwareSerial.h>
SoftwareSerial monitor(0, 1); // RX, TX

// Include various modules here

// ========================================================

// Module - IR_01 - Infrared Receiver using TSOP31238
#include <DbkIRremote.h>    // C:\Program Files (x86)\Arduino\libraries\RobotIRremote

// Pins
#define IR_RECEIVE_PIN  8

IRrecv ir_receive(IR_RECEIVE_PIN);
decode_results ir_decoded;


void ir_debug_print() {
    Serial.print(" Bits: ");
    Serial.print(ir_decoded.bits);
    Serial.print("\t Raw Length: ");
    Serial.print(ir_decoded.rawlen);
    Serial.print("\t Decode Type: ");
    Serial.print(ir_decoded.decode_type, DEC);
    Serial.print("\t Decode Value: ");
    Serial.println(ir_decoded.value, HEX);
}
void ir_receive_setup() {
    ir_receive.enableIRIn();    // Initialize IR Receiver
}
void ir_receive_loop() {
    int l_ret = ir_receive.decode(&ir_decoded);
    if (l_ret) {
        ir_debug_print();
    }
    ir_receive.resume();
    delay(100);
}

// ========================================================

// Standard setup and loop
void setup() {
    monitor.begin(9600);
    Serial.begin(9600);
    Serial.println("IR_01 - Framework");
    Serial.println();
    // Include vaarious module setups here.
    ir_receive_setup();
}
void loop() {
    // Include various module loops here.
    ir_receive_loop();
}
// ### END DBK

