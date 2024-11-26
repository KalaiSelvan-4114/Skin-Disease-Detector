#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16x2 LCD (adjust the address if needed)
LiquidCrystal_I2C lcd(0x27, 16, 2);  // adjust to 0x3F if necessary

void setup() {
  // Initialize the LCD
  lcd.init();
  
  // Turn on the backlight
  lcd.backlight();
  
  // Clear any previous content
  lcd.clear();
  
  // Set up serial communication at a baud rate of 115200 (same as ESP32-CAM)
  Serial.begin(115200);
  
  // Display a startup message
  lcd.setCursor(0, 0);
  lcd.print("Waiting for");
  lcd.setCursor(0, 1);
  lcd.print("ESP32 data...");
}

void loop() {
  // Check if data is available on the serial monitor
  if (Serial.available()) {
    // Read the incoming string from the serial monitor
    String incomingData = Serial.readStringUntil('\n'); // Read until newline
    
    // Clear the LCD to update with new data
    lcd.clear();
    
    // If the data is 16 characters or less, display it on the first row
    if (incomingData.length() <= 16) {
      lcd.setCursor(0, 0); // Start at the first row, first column
      lcd.print(incomingData); // Display the incoming data
    } 
    // If the data is longer than 16 characters, split it across both rows
    else {
      lcd.setCursor(0, 0); // First row
      lcd.print(incomingData.substring(0, 16)); // Display the first 16 characters
      lcd.setCursor(0, 1); // Second row
      lcd.print(incomingData.substring(16)); // Display the remaining characters
    }
  }
}
