/*
 * Home_Base project 01
 *
 * Arduino Uno
 * 
 *This is a base line project 
 */
#include<stdlib.h>
#include <SoftwareSerial.h>
SoftwareSerial monitor(0, 1); // RX, TX
// Variables
unsigned long time_delay;



// Include various modules here

// Module - Temperature_01 - DHT11 Temperature / Humidity Sensor
#include <dht.h>    // C:\Users\briank\Downloads\Projects\libraries\DHTlib (legacy)
#define LOOP_DELAY  60 * 1000    // seconds to delay
dht Sensor;    // Instantiate
// Pins
#define DHT11_PIN  3
void debug_PrintReading() {
    Serial.print("Humidity: ");
    Serial.print(Sensor.humidity);
    Serial.print("%\t Temperature: ");
    Serial.print(Sensor.temperature);
    Serial.print(" C\t Temperature: ");
    Serial.print(convert_C2F(Sensor.temperature));
    Serial.println(" F");
}
void print_error(int8_t p_erc) {
    if (p_erc == DHTLIB_OK) return;
    if (p_erc == DHTLIB_ERROR_CHECKSUM) Serial.println("Checksum Error!");
    if (p_erc == DHTLIB_ERROR_TIMEOUT) Serial.println("DHT11 Timeout!");
    if (p_erc == DHTLIB_ERROR_CONNECT) Serial.println("DHT11 Connection Error!");
    if (p_erc == DHTLIB_ERROR_ACK_L) Serial.println("DHT11 ACK_L error!");
    if (p_erc == DHTLIB_ERROR_ACK_H) Serial.println("DHT11 ACK_H error!");
}
int8_t ReadTemps(){
    int8_t l_erc = Sensor.read11(DHT11_PIN);
    return l_erc;
}
double convert_C2F(double p_temp) {
    double converted = ((p_temp / 5.0) * 9.0) + 32.0;
    return converted;
}
void sensor_setup() {
}
void sensor_loop() {
    if ((time_now - time_delay) > LOOP_DELAY) {
        time_delay = time_now;
    } else {
        //Serial.print("Now ");
        //Serial.print(time_now);
        //Serial.print(" ");
        //Serial.println(time_delay);
        return;
    }
    // Serial.println("Read sensor: ");
    int8_t l_erc = ReadTemps();
    print_error(l_erc);
    debug_PrintReading();
}
// Module End


// Standard setup and loop
void setup() {
    monitor.begin(9600);
    Serial.begin(9600);
    Serial.println("Temperature_01 - Temperature and Humidity\n");
    time_start = millis();
    time_delay = 0;
    // Include vaarious module setups here.
    sensor_setup();
}
void loop() {
    time_now = millis();
    // Include various module loops here.
    sensor_loop();
}
// ### END DBK

