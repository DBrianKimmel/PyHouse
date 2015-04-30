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



// Include various modules here
#include <Ethernet.h>    // C:\Program Files (x86)\Arduino\libraries\Ethernet
#include <SPI.h>    // C:\Users\briank\AppData\Roaming\Arduino15\packages\arduino\hardware\avr\1.6.2\libraries\SPI

// Network Settings
// MAC address of ethernet shield
// Look for it on a sticket at the bottom of the shield. 
// Old Arduino Ethernet Shields or clones may not have a dedicated MAC address. Set any hex values here.
byte MAC_ADDRESS[] = {  0xFE, 0xED, 0xDE, 0xAD, 0xBE, 0xEF };

EthernetClient ethClient;

void ethernet_dhcp_setup() {  
    Serial.println("About to set up Ethernet via DHCP.");
    int l_ret = Ethernet.begin(MAC_ADDRESS);
    if (l_ret == 0) {
      Serial.println("Failed to configure Ethernet using DHCP");
      return;
    } else {
        Serial.println("Ethernet Configured: ");
    }
}
byte STATIC_IP[] = { 192, 168, 1, 91 };
byte DNS_SERVER[] = { 192, 168, 1, 1 };
byte GATEWAY_ADDR[] = { 192, 168, 1, 1};
byte SUBNET_MASK[] = { 255, 255, 255, 0};
void ethernet_static_setup() {  
    Serial.println("About to set up Ethernet Static IP.");
    // Everything after the StaticIP is optional
    Ethernet.begin(MAC_ADDRESS, STATIC_IP, DNS_SERVER, GATEWAY_ADDR, SUBNET_MASK);
    Serial.println("Ethernet Configured: ");
}

void ethernet_debug() {
    Serial.print("IP Address: ");
    Serial.println(Ethernet.localIP());
    Serial.print("Netmask: ");
    Serial.println(Ethernet.subnetMask());
    Serial.print("Gateway Address: ");
    Serial.println(Ethernet.gatewayIP());
    Serial.print("Dns Server: ");
    Serial.println(Ethernet.dnsServerIP());
}

void ethernet_loop() {
}




// Standard setup and loop
void setup() {
    monitor.begin(9600);
    Serial.begin(9600);
    Serial.println("Home_Base_01 - Framework");
    Serial.println();
    // Include vaarious module setups here.
    ethernet_static_setup();
    ethernet_debug();
}
void loop() {
    // Include various module loops here.
    ethernet_loop();
}
// ### END DBK

