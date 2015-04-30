/*
 * Home_Base project 01
 *
 * Arduino Uno
 * 
 *This is a base line project 
 */
#include<stdlib.h>
#include <SoftwareSerial.h>    // C:\Users\briank\AppData\Roaming\Arduino15\packages\arduino\hardware\avr\1.6.2\libraries\SoftwareSerial
SoftwareSerial monitor(0, 1);  // RX, TX

// Include various modules here

// Module - Ethernet
#include <SPI.h>    // C:\Users\briank\AppData\Roaming\Arduino15\packages\arduino\hardware\avr\1.6.2\libraries\SPI
#include <Ethernet.h>    // C:\Program Files (x86)\Arduino\libraries\Ethernet
  
// Network Settings
byte MAC_ADDRESS[] = {  0xFE, 0xED, 0xDE, 0xAD, 0xBE, 0xEF };

EthernetClient ethClient;
 
void ethernet_setup() {  
    Serial.println("About to set up Ethernet.");
    int l_ret = Ethernet.begin(MAC_ADDRESS);
    if (l_ret == 0) {
      Serial.println("Failed to configure Ethernet using DHCP");
      return;
    } else {
        Serial.print("Ethernet Configured: ");
        Serial.println(l_ret);
    }
}


// Module - MQTT
#include <PubSubClient.h>    // C:\Users\briank\Downloads\Projects\libraries\PubSubClient (legacy)

// Variables
unsigned long time;
char message_buffer[100];
int QOS1 = 1;

// IP address of MQTT server
byte MQTT_SERVER_IP[] = { 192, 168, 1, 72 };
char* tempC = "78.9";

// Create the client.
PubSubClient client(MQTT_SERVER_IP, 1883, mqtt_callback, ethClient);

void mqtt_setup() {
    Serial.println("MQTT Setup.");
}

void connect_subscribe() {
    char* client_id = "Node-Arduino_001";
    Serial.println("Connecting MQTT now...");
    // client.connect("clientID", "mqtt_username", "mqtt_password");
    client.connect(client_id);
    client.subscribe("pyhouse/#");
    int l_ret = client.publish("pyhouse/arduino/alive", "I'm alive!");
    Serial.print("  Alive message sent. ");
    Serial.println(l_ret);
}

void debug_print_message() {
}

void mqtt_loop() {
    if (!client.connected()) {
        connect_subscribe();
    }
    // Publish sensor reading every X milliseconds
    if (millis() > (time + 10*1000)) {
        Serial.println("Sending Mqtt message.");
        time = millis();
        client.publish("pyhouse/arduino/temperature", tempC);
    }
    // MQTT client loop processing
    client.loop();
}
 
// Handles messages arrived on subscribed topic(s)
void mqtt_callback(char* p_topic, byte* p_payload, unsigned int p_length) {
    Serial.print("Got message back. ");
    Serial.print(p_topic);
    Serial.print("  ");
    Serial.print(p_length);
    Serial.print(" >>");
    Serial.write(p_payload, p_length);    // print a byte array
    Serial.println("<<");
}


// Standard setup and loop
void setup() {
    monitor.begin(9600);
    Serial.begin(9600);
    Serial.println("Home_Base_01 - Framework");
    Serial.println();
    // Include vaarious module setups here.
    ethernet_setup();
    mqtt_setup();
}
void loop() {
    // Include various module loops here.
    mqtt_loop();
}
// ### END DBK

