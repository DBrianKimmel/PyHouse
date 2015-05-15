/*
 * Home arduino package 01
 *
 * Arduino Uno
 * Temperature Humidity Sensor DHT-11
 * WiFi Adapter ESP-01
 * Infrared Sensor - TSOP31238
 * Light Sensor
 *
 */

#include<stdlib.h>
#include <SoftwareSerial.h>
SoftwareSerial monitor(0, 1); // RX, TX
// Variables
unsigned long time_start;
unsigned long time_delay;
unsigned long time_now;

// Include various modules here

// ========================================================

// Module WiFi_01 - Connect to WiFi access point
#include <ESP8266.h>    // C:\Users\briank\Downloads\Projects\libraries\ITEADLIB_Arduino_WeeESP8266-master (legacy)

// Pins
#define WIFI_TX  5
#define WIFI_RX  6

#define WIFI_SSID        "PINKPOPPY"
#define WIFI_PASSWORD    "Koepfinger-59"

ESP8266 wifi(monitor);

void print_bool(char* p_name, bool p_value) {
    Serial.print(p_name);
    if (p_value) Serial.println(" Success.");
    else Serial.println(" Failure.");
}
void wifiRestart() {
    bool l_erc = wifi.restart();
    print_bool("Restart: ", l_erc);
}
void wifiKick() {
    bool l_erc = wifi.kick();
    print_bool("Kick: ", l_erc);
}
void wifiGetVersion() {
    String l_version = wifi.getVersion().c_str();
    Serial.print("Firmware Version: ");
    Serial.println(l_version);
}
void wifiOprToStation() {
    bool l_erc = wifi.setOprToStation();
    print_bool("Set Operation Mode to Station: ", l_erc);
}
void wifiOprToSoftAP() {
    bool l_erc = wifi.setOprToSoftAP();
    print_bool("Set Operation Mode to SoftAP: ", l_erc);
}
void wifiOprToStationSoftAP() {
    bool l_erc = wifi.setOprToStationSoftAP();
    print_bool("Set Operation Mode to StationSoftAP: ", l_erc);
}
void wifiJoinAP(String p_ssid, String p_password) {
    bool l_erc = wifi.joinAP(WIFI_SSID, WIFI_PASSWORD);
    print_bool("Join AP: ", l_erc);
}
void wifiListAPs() {
    String l_ret = wifi.getAPList();
    Serial.println("List of APs: ");
    Serial.println(l_ret);
    Serial.println("__________");
}
void wifi_setup() {
    Serial.print("wifi_setup begin\n");
    wifiRestart();
    wifiKick();
    wifiGetVersion();
    wifiOprToStation();
    wifiOprToSoftAP();
    wifiOprToStationSoftAP();
    wifiJoinAP(WIFI_SSID, WIFI_PASSWORD);
    wifiListAPs();
    // Serial.print("setup end\r\n");
}
void wifi_loop() {
}
// Module END - WiFi

// ========================================================

// Module - Temperature_01 - DHT11 Temperature / Humidity Sensor
#include <dht.h>    // C:\Users\briank\Downloads\Projects\libraries\DHTlib (legacy)
#define LOOP_DELAY  06 * 1000    // seconds to delay
dht Sensor;    // Instantiate
// Pins
#define DHT11_PIN  4
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

void setup() {
    monitor.begin(9600);
    Serial.begin(9600);
    Serial.println("Home_01 - TEST PROGRAM\n");
    time_start = millis();
    time_delay = 0;
    // Include vaarious module setups here.
    wifi_setup();
    sensor_setup();
}
void loop() {
    time_now = millis();
    // Include vaarious module loops here.
    wifi_loop();
    sensor_loop();
}
// ### END DBK
