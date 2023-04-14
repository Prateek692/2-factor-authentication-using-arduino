/*
  Matrix Keypad Demo
  keypad-demo.ino
  Demonstrates use of 4x4 matrix membrane keypad with Arduino
  Results on serial monitor

  DroneBot Workshop 2020
  https://dronebotworkshop.com
*/

// Include the Keypad and Servo library
#include <Keypad.h>
#include <Servo.h>

//Servo variable created

Servo myservo;

// Constants for row and column sizes
const byte ROWS = 4;
const byte COLS = 4;

// Array to represent keys on keypad
char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

// Connections to Arduino
byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};

// Create keypad object
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

void setup() {
  // Setup serial monitor
  Serial.begin(9600);
  myservo.attach(10); //Pin no for servo motor
}

void loop() {
  // Get key value if pressed
  char customKey = customKeypad.getKey();

  if (customKey) {
    // Print key value to serial monitor
    Serial.println(customKey);
  }x
  // Servo code
  if (Serial.available() > 0) {
    int pos = 180;
    myservo.write(pos);
    // Serial.println(pos);
  }
}
