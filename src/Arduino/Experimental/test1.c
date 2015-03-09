/*
  433 MHz RF REMOTE REPLAY sketch
     Written by ScottC 24 Jul 2014
     Arduino IDE version 1.0.5
     Website: http://arduinobasics.blogspot.com
     Receiver: XY-MK-5V      Transmitter: FS1000A/XY-FST
     Description: Use Arduino to receive and transmit RF Remote signal
 ------------------------------------------------------------- */

 #define rfReceivePin A0     //RF Receiver data pin = Analog pin 0
 #define rfTransmitPin 4  //RF Transmitter pin = digital pin 4
 #define button 6           //The button attached to digital pin 6
 #define ledPin 13        //Onboard LED = digital pin 13

 const int dataSize = 500;  //Arduino memory is limited (max=1700)
 byte storedData[dataSize];  //Create an array to store the data
 const unsigned int threshold = 100;  //signal threshold value
 int maxSignalLength = 255;   //Set the maximum length of the signal
 int dataCounter = 0;    //Variable to measure the length of the signal
 int buttonState = 1;    //Variable to control the flow of code using button presses
 int buttonVal = 0;      //Variable to hold the state of the button
 int timeDelay = 105;    //Used to slow down the signal transmission (can be from 75 - 135)

 void setup(){
   Serial.begin(9600);    //Initialise Serial communication - only required if you plan to print to the Serial monitor
   pinMode(rfTransmitPin, OUTPUT);
   pinMode(ledPin, OUTPUT);
   pinMode(button, INPUT);
 }

 void loop(){
   buttonVal = digitalRead(button);

   if(buttonState>0 && buttonVal==HIGH){
     //Serial.println("Listening for Signal");
     initVariables();
     listenForSignal();
   }

   buttonVal = digitalRead(button);

   if(buttonState<1 && buttonVal==HIGH){
     //Serial.println("Send Signal");
     sendSignal();
   }

   delay(20);
 }


 /* ------------------------------------------------------------------------------
     Initialise the array used to store the signal
    ------------------------------------------------------------------------------*/
 void initVariables(){
   for(int i=0; i<dataSize; i++){
     storedData[i]=0;
   }
   buttonState=0;
 }


 /* ------------------------------------------------------------------------------
     Listen for the signal from the RF remote. Blink the RED LED at the beginning to help visualise the process
     And also turn RED LED on when receiving the RF signal
    ------------------------------------------------------------------------------ */
 void listenForSignal(){
   digitalWrite(ledPin, HIGH);
   delay(1000);
   digitalWrite(ledPin,LOW);
   while(analogRead(rfReceivePin)<threshold){
     //Wait here until an RF signal is received
   }
   digitalWrite(ledPin, HIGH);

   //Read and store the rest of the signal into the storedData array
   for(int i=0; i<dataSize; i=i+2){

      //Identify the length of the HIGH signal---------------HIGH
      dataCounter=0; //reset the counter
      while(analogRead(rfReceivePin)>threshold && dataCounter<maxSignalLength){
        dataCounter++;
      }
      storedData[i]=dataCounter;    //Store the length of the HIGH signal


      //Identify the length of the LOW signal---------------LOW
      dataCounter=0;//reset the counter
      while(analogRead(rfReceivePin)<threshold && dataCounter<maxSignalLength){
        dataCounter++;
      }
      storedData[i+1]=dataCounter;  //Store the length of the LOW signal
   }

     storedData[0]++;  //Account for the first AnalogRead>threshold = lost while listening for signal
     digitalWrite(ledPin, LOW);
 }


 /*------------------------------------------------------------------------------
    Send the stored signal to the FAN/LIGHT's RF receiver. A time delay is required to synchronise
    the digitalWrite timeframe with the 433MHz signal requirements. This has not been tested with different
    frequencies.
    ------------------------------------------------------------------------------ */
 void sendSignal(){
   digitalWrite(ledPin, HIGH);
   for(int i=0; i<dataSize; i=i+2){
       //Send HIGH signal
       digitalWrite(rfTransmitPin, HIGH);
       delayMicroseconds(storedData[i]*timeDelay);
       //Send LOW signal
       digitalWrite(rfTransmitPin, LOW);
       delayMicroseconds(storedData[i+1]*timeDelay);
   }
   digitalWrite(ledPin, LOW);
   delay(1000);


   /*-----View Signal in Serial Monitor
   for(int i=0; i<dataSize; i=i+2){
       Serial.println("HIGH,LOW");
       Serial.print(storedData[i]);
       Serial.print(",");
       Serial.println(storedData[i+1]);
   }
   ---------------------------------- */
 }

