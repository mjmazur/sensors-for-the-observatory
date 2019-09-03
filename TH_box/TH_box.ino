#include <Adafruit_Sensor.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library
#include <DallasTemperature.h>
#include <OneWire.h>
#include <SPI.h>
#include "DHT.h"

#define DHT1PIN 2     // what digital pin we're connected to
#define DHT2PIN 3

// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11
//#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

#define ONE_WIRE_BUS 4

#define RELAY1 6
#define RELAY2 7

#define LCD_LIGHT_PIN A4
#define buttonPin 5

// For the breakout, you can use any 2 or 3 pins
// These pins will also work for the 1.8" TFT shield
#define TFT_CS     10
#define TFT_RST    9  // you can also connect this to the Arduino reset
                      // in which case, set this #define pin to 0!
#define TFT_DC     8

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Option 1 (recommended): must use the hardware SPI pins
// (for UNO thats sclk = 13 and sid = 11) and pin 10 must be
// an output. This is much faster - also required if you want
// to use the microSD card (see the image drawing example)
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS,  TFT_DC, TFT_RST);

// Option 2: use any pins but a little slower!
#define TFT_SCLK 13   // set these to be whatever pins you like!
#define TFT_MOSI 11   // set these to be whatever pins you like!
//Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

// Initialize DHT sensor.
// Note that older versions of this library took an optional third parameter to
// tweak the timings for faster processors.  This parameter is no longer needed
// as the current DHT reading algorithm adjusts itself to work on faster procs.
DHT dht1(DHT1PIN, DHTTYPE);
DHT dht2(DHT2PIN, DHTTYPE);

int buttonState = 0, cycleCnt = 0;
float T0, T1, T2, T3;

void setup(void) {
  Serial.begin(9600);
  
  Serial.println("Fluid\tShed\tF_t\tF_h\tG_t\tG_h");
  sensors.begin();

  // Use this initializer if you're using a 1.8" TFT
  //tft.initR(INITR_BLACKTAB);   // initialize a ST7735S chip, black tab

  // Use this initializer (uncomment) if you're using a 1.44" TFT
  tft.initR(INITR_144GREENTAB);   // initialize a ST7735S chip, black tab
  tft.setRotation(1);
  dht1.begin();
  dht2.begin();
  
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  digitalWrite(RELAY1, HIGH);
  digitalWrite(RELAY2, HIGH);
  
  pinMode(buttonPin, INPUT);
  pinMode(LCD_LIGHT_PIN, OUTPUT);
  
  digitalWrite(LCD_LIGHT_PIN, LOW);
}

void loop() {
  tftPrintTest();
}

void tftPrintTest() {
  sensors.requestTemperatures();
  
  T0 = sensors.getTempCByIndex(0);
  if (T0 == -127.00) T0 = 99.99;
  T1 = sensors.getTempCByIndex(1);
  if (T1 == -127.00) T1 = 99.99;
  T2 = sensors.getTempCByIndex(2);
  if (T2 == -127.00) T2 = 99.9;
  T3 = sensors.getTempCByIndex(3);
  if (T3 == -127.00) T3 = 99.9;

  float t1 = dht1.readTemperature();
  float h1 = dht1.readHumidity();
  float t2 = dht2.readTemperature();
  float h2 = dht2.readHumidity();

  // Check to see if a T/H is below some limit.
  // If so, keep relay closed. If not, open relay. 
  if (h1 < 50.0) digitalWrite(RELAY1, HIGH);
  else digitalWrite(RELAY1, LOW);
  
  if (h2 < 50.0) digitalWrite(RELAY2, HIGH);
  else digitalWrite(RELAY2, LOW);
  
  // Check to make sure the humidity is a number.
  // If not, set it to 0.0.
  if (isnan(h1)) 
    h1 = 0.0;
  if (isnan(h2))  
    h2 = 0.0;

  Serial.print(T0);
  Serial.print("\t");
  Serial.print(T1);
  Serial.print("\t");
  Serial.print(T2);
  Serial.print("\t");
  Serial.print(h1);
  Serial.print("\t");
  Serial.print(T3);
  Serial.print("\t");
  Serial.println(h2);
  
  if (cycleCnt > 0)
    cycleCnt--;
  
  // Turn on LCD backlight when button is pushed.
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH && cycleCnt < 2) {
    digitalWrite(LCD_LIGHT_PIN, HIGH);
    cycleCnt = 2;
  }
  else if (cycleCnt > 0)
    digitalWrite(LCD_LIGHT_PIN, HIGH);
  else {
    digitalWrite(LCD_LIGHT_PIN, LOW);
    cycleCnt = 0;
  }
  
  tft.setTextWrap(false);
  tft.fillScreen(ST7735_BLACK);
  tft.setCursor(5, 0);
  tft.setTextColor(ST7735_RED);
  tft.setTextSize(2);
  tft.print("T");
  tft.setTextSize(1);
  tft.setCursor(18,8);
  tft.print("Fluid");
  tft.setCursor(47,0);
  tft.setTextSize(2);
  tft.print(":");
  tft.print(T0, 1);
  tft.println((char)247);
  //tft.println("C");
  //tft.setTextColor(ST7735_GREEN);
  tft.setTextSize(2);
  tft.setCursor(5,18);
  tft.print("T");
  tft.setTextSize(1);
  tft.setCursor(18,24);
  tft.print("Shed");
  tft.setTextSize(2);
  tft.setCursor(47,18);
  tft.print(":");
  tft.print(T1, 1);
  tft.println((char)247);

  tft.setCursor(5, 46);
  tft.setTextColor(ST7735_GREEN);
  tft.setTextSize(2);
  tft.print("T");
  tft.setTextSize(1);
  tft.setCursor(18,54);
  tft.print("FCAM");
  tft.setTextSize(2);
  tft.setCursor(47,46);
  tft.print(":");
  tft.print(T2, 1);
  tft.println((char)247);
  //tft.setTextColor(ST7735_GREEN);
  tft.setTextSize(2);
  tft.setCursor(5,64);
  tft.print("H");
  tft.setTextSize(1);
  tft.setCursor(18,70);
  tft.print("FCAM");
  tft.setTextSize(2);
  tft.setCursor(47,64);
  tft.print(":");
  tft.print(h1, 1);
  tft.println("%");

  tft.setCursor(5, 90);
  tft.setTextColor(ST7735_BLUE);
  tft.setTextSize(2);
  tft.print("T");
  tft.setTextSize(1);
  tft.setCursor(18,98);
  tft.print("GCAM");
  tft.setTextSize(2);
  tft.setCursor(47,90);
  tft.print(":");
  tft.print(T3, 1);
  tft.println((char)247);
  //tft.setTextColor(ST7735_GREEN);
  tft.setTextSize(2);
  tft.setCursor(5,108);
  tft.print("H");
  tft.setTextSize(1);
  tft.setCursor(18,114);
  tft.print("GCAM");
  tft.setTextSize(2);
  tft.setCursor(47,108);
  tft.print(":");
  tft.print(h2, 1);
  tft.println("%");

  // Turn on TFT backlight when button is pushed.
  // Delay for 200ms and loop 10 times.
  for (int i=0; i<10; i++){
  delay(200);
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH && cycleCnt < 2) {
    digitalWrite(LCD_LIGHT_PIN, HIGH);
    cycleCnt = 2;
  }
  }
  //delay(5000);
}
