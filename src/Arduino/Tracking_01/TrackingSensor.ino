/* FILE:    ARD_Line_Hunting_Sensor_HCARDU0005_Example.pde
   DATE:    03/07/12
   VERSION: 0.1

This is a simple example of how to use the HobbyComponents Arduino Line hunting
sensor module (HCARDU0005). It is a very simple module that requires only one DIO
pin (defined as an input) to operate. When the sensor detects a reflective object 
in close proximity it will pull a DIO pin that it has been connected to LOW. A 
non reflective or no object in close proximity will cause the DIO pin to go high.

You may copy, alter and reuse this code in any way you like but please leave 
reference to HobbyComponents.com in your comments if you redistribute this code.




1
GND
2
OUT
3
VCC (+5V)




 */



/* Define the DIO pin that will be used to communicate with the sensor */
#define LINEHUNTSENS_DIO 2

/* Initialise serial and DIO */
void setup()
{
  /* Setup the serial port for displaying the status of the sensor */
  Serial.begin(9600);
  
  /* Configure the DIO pin the sensor will be connected to as an input */
  pinMode(LINEHUNTSENS_DIO, INPUT); 
}


/* Main program loop */
void loop()
{
  /* If the DIO pin is pulled low then an object has been detected */
  if (!digitalRead(LINEHUNTSENS_DIO))
    Serial.println("Object detected !");
    
}
  