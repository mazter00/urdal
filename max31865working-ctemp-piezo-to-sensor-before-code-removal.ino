// #include <Time.h>
// #include <TimeLib.h>

/***************************************************
  This is a library for the Adafruit PT100/P1000 RTD Sensor w/MAX31865

  Designed specifically to work with the Adafruit RTD Sensor
  ----> https://www.adafruit.com/products/3328

  This sensor uses SPI to communicate, 4 pins are required to
  interface
  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Adafruit_MAX31865.h>

// Use software SPI: CS, DI, DO, CLK
Adafruit_MAX31865 max = Adafruit_MAX31865(10, 11, 12, 13);
// use hardware SPI, just pass in the CS pin
//Adafruit_MAX31865 max = Adafruit_MAX31865(10);

// The value of the Rref resistor. Use 430.0 for PT100 and 4300.0 for PT1000
#define RREF      430.0
// The 'nominal' 0-degrees-C resistance of the sensor
// 100.0 for PT100, 1000.0 for PT1000
#define RNOMINAL  100.0

void setup() {
  Serial.begin(115200);
  Serial.println("Adafruit MAX31865 PT100 Sensor Test!");

  max.begin(MAX31865_4WIRE);  // set to 2WIRE or 4WIRE as necessary
}

// For tid
int counter;
int maxcounter = 350;

// Note: Counter = 100 og Delay = 30 -> 19 sekunder
// Counter = 350 og Delay = 20 -> 64 sekunder (håper på ca. 60 sekunder)


// For sammenligning
int compare = 0;
char bevegelse[4];
int debug = 0;


// Brukes for [2][3][.][4] som er 4 + 1 for [\n] = 5
char outtemp[5] = "99.9";
char outtemp2[5] = "99.8";
char outtemp3[5] = "99.7";

// Setter global var, setter egen verdi først. ctemp trengs ikke fordi den settes straks.
float ctemp2 = 99.8;
float ctemp3 = 99.7;

void loop() {
  uint16_t rtd = max.readRTD();

  // Serial.print("RTD value: "); Serial.println(rtd);
  float ratio = rtd;
  ratio /= 32768;
  // Serial.print("Ratio = "); Serial.println(ratio,8);
  // Serial.print("Resistance = "); Serial.println(RREF*ratio,8);

  // Flyttet!
  // Serial.print("Temperature = ");

  // Deklarerer current temp
  float ctemp = max.temperature(RNOMINAL, RREF);

  // d2str gjøres hver gang, 4 i total length, 1 desimal
  dtostrf(ctemp, 4, 1, outtemp);

  // Note to self: ctemp er float og outtemp er char array(?) på 5 med current temp

  compare = strcmp(outtemp, outtemp2);

  if (debug == 1) {
    Serial.print("DEBUG Compare: ");
    Serial.println(compare);

    Serial.println(outtemp);
    Serial.println(outtemp2);
  }

  if (compare != 0) {
    // Wow, ulik betyr utsendelse

    if (compare > 0) {
      strcpy(bevegelse, "OPP");
    }   else if (compare < 0) {
      strcpy(bevegelse, "NED");
    }

    Serial.print("Gikk ");
    Serial.print(bevegelse);
    Serial.print(" fra ");
    Serial.print(outtemp2);
    Serial.print(" til ");
    Serial.println(outtemp);

    // Dette er float, current temp
    Serial.print("Temperature (med float) = ");
    // Gammel: Serial.println(ctemp);
    // Nå med en desimal, current temp, som skal bli snappet opp av Python
    Serial.println(outtemp);

    //    Serial.println("Before strcopy");
    //    Serial.println(outtemp);
    //    Serial.println(outtemp2);
    //

    strcpy(outtemp2, outtemp);
    counter = 0;
    compare = 0;

    //
    //    Serial.println("Etter strcopy");
    //    Serial.println(outtemp);
    //    Serial.println(outtemp2);

    // Serial.println("After strcopy, are they similar?!");
    //    if (outtemp != outtemp2) {
    //      Serial.println("Un-equal");
    //    }
    //    if (outtemp == outtemp2) {
    //      Serial.println("Equal, as it should be");
    //    }
  }


  // Check and print any faults
  uint8_t fault = max.readFault();
  if (fault) {
    Serial.print("Fault 0x"); Serial.println(fault, HEX);
    if (fault & MAX31865_FAULT_HIGHTHRESH) {
      Serial.println("RTD High Threshold");
    }
    if (fault & MAX31865_FAULT_LOWTHRESH) {
      Serial.println("RTD Low Threshold");
    }
    if (fault & MAX31865_FAULT_REFINLOW) {
      Serial.println("REFIN- > 0.85 x Bias");
    }
    if (fault & MAX31865_FAULT_REFINHIGH) {
      Serial.println("REFIN- < 0.85 x Bias - FORCE- open");
    }
    if (fault & MAX31865_FAULT_RTDINLOW) {
      Serial.println("RTDIN- < 0.85 x Bias - FORCE- open");
    }
    if (fault & MAX31865_FAULT_OVUV) {
      Serial.println("Under/Over voltage");
    }
    max.clearFault();
  }

  // 09.04.2018: Sende PONG for hver 350. utsendelse

  counter = counter + 1;
  // max counter er satt i starten av scriptet. Angir max counter før PONG
  if (counter >= maxcounter) {
    Serial.print("PONG - ");
    Serial.print("Counter: ");
    Serial.print(counter);

    Serial.print(" Maxcounter: ");
    Serial.print(maxcounter);

    Serial.print(" Last known Temperature: = ");
    Serial.println(outtemp);

    counter = counter - maxcounter;
    if (counter != 0) {
      Serial.print("Counter satt til: ");
      Serial.println(counter);
    }
  }

  // I gamle dager satte vi delay på flere sekunder, nå sender vi bare ved hver endring + minimum 10ms
  delay(20);
}
