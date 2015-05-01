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
// Module WiFi_01 - Connect to WiFi access point
#include <ESP8266.h>    // C:\Users\briank\Downloads\Projects\libraries\ITEADLIB_Arduino_WeeESP8266-master (legacy)
// Pins
#define WIFI_TX  7
#define WIFI_RX  5
#define WIFI_SSID        "SID_NAME"
#define WIFI_PASSWORD    "123456789"
ESP8266 wifi(monitor);    // Instantiate
void print_bool(char* p_name, bool p_value) {
	Serial.print(p_name);
	if (p_value)
		Serial.println(" Success.");
	else
		Serial.println(" Failure.");
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

// Standard setup and loop
void setup() {
	monitor.begin(9600);
	Serial.begin(9600);
	Serial.println("WiFi_01\n");
	// Include vaarious module setups here.
	wifi_setup();
}
void loop() {
	// Include various module loops here.
	wifi_loop();
}

// ### END DBK

