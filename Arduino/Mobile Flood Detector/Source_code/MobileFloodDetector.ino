#include <SoftwareSerial.h> //enables Wifi module functions
#include <Wire.h> //enables I2C commmunication for LCD
#include <LiquidCrystal_I2C.h> //enables LCD library

//*------------------------------------------------------------------- Pins
//IR sensor pins
#define LeftIR_Pin  A0   // A0 input pin for IR sensor signal
#define RightIR_Pin A1
//Motor pins
#define LI1 9
#define LI2 6
#define RI1 3
#define RI2 5
//Ultrasonic sensor pins
#define TRIG 11
#define ECHO 10
//Rain sensor pin
#define RainSensor_Pin 4

//*------------------------------------------------------------------Constants
#define DEBUG false // constant used for debugging wifi module
#define Flood_threshold 4 // constant to represent threshold for flood
#define Ultrasonic_distance_to_ground 11 // constant to represent distance between ultrasonic sensor and ground
const unsigned long Battery_duration = 3600000UL;          // constant to represent 1 hour of battery life
const unsigned long Battery_one_percent = Battery_duration / 100UL; // constant to calculate duration for 1% of battery to deplete
int previous_battery_level = 0;
String CurrentAction = "";
bool rain = false; // Variable to detect rain
int blockage = 0; // Variable to detect blockage
bool RainEvent = false; // Variable to show whether flood level from rain is still there
int current_water_level = 0; // Variable for storing current water level
int previous_water_level = 0; // Variable Previous valid water data from when it was raining.
unsigned long LastSentData = 0;  // Variable to represent duration since data was last sent

//Wifi strings
SoftwareSerial espSerial(12,13); //Pin 12 and 13 act as RX and TX for wifi module.
String mySSID = "...";       // WiFi SSID
String myPWD = "..."; // WiFi Password
String myAPI = "...";   // API Key
String myHOST = "api.thingspeak.com"; // API website
String myPORT = "80"; // 80 is Port used for HTTP
String WaterLevel_Field = "field1"; // Field 1 for sending water level
String DrainBlockage_Field = "field2"; // Field 2 for sending drainage block
//IR values
int Left_Val = 0; // Left IR sensor
int Right_Val = 0; // Right IR sensor
//Custom battery symbols for LCD
uint8_t Full_battery[8] = {0xE,0xE,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F}; // Array to print out symbol for full battery
uint8_t Medium_battery[8] = {0xE,0xE,0x1F,0x11,0x11,0x1F,0x1F,0x1F}; // Array to print out symbol for medium battery
uint8_t Low_battery[8] = {0xE,0xE,0x1F,0x11,0x11,0x11,0x1F,0x1F}; // Array to print out symbol for low battery

//*---------------------------------------------------------- Functions
//Motor functions
void move_forward(void); //Motor move forward
void brake(void); //Motor brakes
void turn_left(void); //Motor turn left
void turn_right(void); //Motor turn right
void path_tracking(); //Car tracks path and move
//Ultrasonic sensor functions
int get_water_level(void); //Returns water level
//Wifi module functions
String espData(String command, const int timeout, boolean debug); //Send command to ESP command prompt
void send_data(int floodVal, int blockage); //Send data to the API
//Rain sensor module
bool detect_rain(void);
//LCD module
void display_battery(void);
void display_action(String action);

LiquidCrystal_I2C lcd(0x27,16,2); // Create lcd object under LiquidCrystal_I2C class, as 0x27 for hardware address. 16 Columns, 2 rows.

//*---------------------------------------------------------- Main Function
void setup() {
  //Serial monitor
  Serial.begin(9600);
  //Ultrasonic sensor
  pinMode(TRIG,OUTPUT);
  pinMode(ECHO,INPUT);
  //LCD:
  //Display what the detector is doing on 1st row
  //Display battery level on 2nd row
  int Battery_level = Battery_duration/Battery_one_percent; // Calculate current battery level
  lcd.init();
  lcd.backlight();
  lcd.createChar(0, Full_battery);
  lcd.createChar(1, Medium_battery);
  lcd.createChar(2, Low_battery);
  lcd.setCursor(0,1);
  lcd.print("Battery: ");
  lcd.print(Battery_level);
  lcd.print("%");
  //Rain Sensor
  pinMode(RainSensor_Pin,INPUT);
  //Wifi    
  espSerial.begin(9600); //Set up ESP communication
  espData("AT+RST", 1000, DEBUG);                      // Reset the ESP8266 module
  espData("AT+CWMODE=1", 1000, DEBUG);                 // Set the ESP mode as station mode
  espData("AT+CWJAP=\""+ mySSID +"\",\""+ myPWD +"\"", 1000, DEBUG);   // Connect to WiFi network   

  delay(200);      
}

void loop()
{
  display_battery(); //display battery on LCD
  path_tracking(); //track path
  current_water_level = get_water_level();

  if (millis() - LastSentData >= 16000) //every 16 seconds interval
  {
    brake();
    delay(2000); //for ease of testing

    current_water_level = get_water_level(); // Get water distance
    rain = detect_rain(); // Detects whether there is rain

    if (!(rain) && (current_water_level >= Flood_threshold)) // No rain and high water level detected --> there is a blockage
    {
      display_action("Blockage!");
      blockage = 1;
      delay(1500); //to show blockage on lcd
    }
    else
    blockage = 0;

    if (rain) //There is rain
    {
    send_data(current_water_level,blockage); //send the current water level, and whether there is a blockage to thingSpeak
    RainEvent = true; //Event of rain occurs
    previous_water_level = current_water_level; //Updates WaterLevel
    }
    else if ((RainEvent) && (!rain) && (current_water_level >= 1)) //Flood level from event of rain hasn't ended
    {
    send_data(current_water_level,blockage); //sends current water level and blockage
    previous_water_level = current_water_level; //Updates waterLevel
    }
    else //No rain & flood from previous rain is gone
    {
      send_data(previous_water_level,blockage); //semds previous water level which is caused by rain event.
      RainEvent = false;
    }
  LastSentData = millis(); //record the time when data is sent
  display_action("Data sent!");
  delay(500);
  move_forward(); //car continues moving forward to initiate path tracking
  }

}

bool detect_rain(void) //detects whether there is rain
{
  return !(digitalRead(RainSensor_Pin)); //when rain, returns 1
}
void display_battery() //displays battery level
{
  int Battery_level;

  if (millis() >= Battery_duration) //Prevent battery level from going negative
  {
    Battery_level = 0;
  }
  else
  {
    Battery_level = (Battery_duration - millis()) / Battery_one_percent; //Calculate battery level
  }
  
  if (Battery_level == previous_battery_level)
    return;

  lcd.setCursor(0,1);
  lcd.print("Battery: ");
  lcd.print("     "); //clear old digits
  lcd.setCursor(9,1);
  lcd.print(Battery_level);
  lcd.print("% ");

  if (Battery_level > 66) //Display full battery symbol
  {
    lcd.write((byte)0);
  }
  else if (Battery_level > 33) //Display medium battery symbol
  {
    lcd.write((byte)1);
  }
  else //Display low battery symbol
  {
    lcd.write((byte)2);
  }

  previous_battery_level = Battery_level;

  return;
}
void display_action(String action)
{
  if (action != CurrentAction)
  {
    lcd.setCursor(0,0);
    lcd.print("                "); //Clear row
    lcd.setCursor(0,0); //Reposition
    lcd.print(action);
    CurrentAction = action;
  }
}
void move_forward() //Moves forward
{
  analogWrite(LI1,174); //Left motor 6 PWM more than right motor
  digitalWrite(LI2,HIGH);
  analogWrite(RI1, 180);
  digitalWrite(RI2,HIGH);
}
void brake() //Stops the car
{
  digitalWrite(LI1,HIGH);
  digitalWrite(LI2,HIGH);
  digitalWrite(RI1,HIGH);
  digitalWrite(RI2,HIGH);
}
void turn_right() //Car turns right
{
  analogWrite(LI1,100);
  digitalWrite(LI2,HIGH);
  analogWrite(RI1,255);
  digitalWrite(RI2,HIGH);
}
void turn_left() //Car turns left
{
  analogWrite(LI1,255);
  digitalWrite(LI2,HIGH);
  analogWrite(RI1,100);
  digitalWrite(RI2,HIGH);
}
void path_tracking() //Track path with IR sensor and move depending on readings
{
  display_action("Tracking path");
  Left_Val = analogRead(LeftIR_Pin); //Detects whether left side of car is black/white
  Right_Val = analogRead(RightIR_Pin); //Detects whether right side of car is black/white

  if (Left_Val > 100 && Right_Val > 100) //left: black, right: black
  {
  move_forward();
  }
  else if (Left_Val < 100 && Right_Val > 100) //left: white, right: black
  {
  turn_right();
  delay(5); //Delay incase car gets off track
  }
  else if (Left_Val > 100 && Right_Val < 100) //left: black, right: white
  {
  turn_left();
  delay(5); //Delay incase car gets off track
  }
  else if (Left_Val < 100 && Right_Val < 100) //left: white, right: white
  {
  delay(5);
  }
}
int get_water_level() //gets water level
{
  //Ultrasonic sensor sends wave and echo to detect pulse duration
  digitalWrite(TRIG,LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG,HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG,LOW);

  long pulseDuration = pulseIn(ECHO, HIGH); //Record duration for which pulse was sent forward and back
  if (pulseDuration == 0) //Ultra sonic sensor is blocked/disabled
  return previous_water_level;

  int distance = pulseDuration/58;

  int water_level = Ultrasonic_distance_to_ground - distance; //calculate water level

  if (water_level < 0)
  return 0;
  else
  return water_level; //distance between Ultrasonic sensor and water
}
String espData(String command, const int timeout, boolean debug) //Prints the command on ESP serial monitor.
{ 
  espSerial.println(command); //Insert command in ESP monitor

  //For debugging wifi module
  String response = "";
  if(debug)
  {
    Serial.print("AT Command ==> ");
    Serial.print(command);
    Serial.println("     ");
    long int time = millis();
  while ( (time + timeout) > millis())
  {
    while (espSerial.available())
    {
      char c = espSerial.read();
      response += c;
    }
    Serial.print(response);
    break;
  }
  }

  return response;
}
void send_data(int floodVal, int blockage){ //Send data to thingSpeak
 
  display_action("Sending data");
  String sendData = "GET /update?api_key="+ myAPI +"&"+ WaterLevel_Field +"="+String(floodVal) + "&" + DrainBlockage_Field +"="+String(blockage); //HTTP get request string

  espData("AT+CIPMUX=1", 10, DEBUG);       //Allow multiple connections, since wifi module has 5 connections (0-4)  
  delay(100);
 
  espData("AT+CIPSTART=0,\"TCP\",\""+ myHOST +"\","+ myPORT, 10, DEBUG); //Send command to establish TCP connection to specified host & port
  delay(2500); //Long delay due to HTTP traffic

  espData("AT+CIPSEND=0," +String(sendData.length()+4),10,DEBUG); //tell wifi module I am about to send data through connection 0. The extra 4 string length is for HTTP termination
  delay(300);

  espSerial.println(sendData); //Enter the API key value to send to website
  delay(300);

  espData("AT+CIPCLOSE=0",10,DEBUG); //Close the communication
}
