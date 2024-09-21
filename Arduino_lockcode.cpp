#include <Servo.h>

Servo myservo;  // Create servo object to control a servo

void setup() {
  myservo.attach(9);  // Attach servo on pin 9 to the servo object
}

void loop() {
  // Example: Unlock the door by rotating the servo to 90 degrees
  myservo.write(90);  // Unlock position
  delay(5000);        // Keep it unlocked for 5 seconds

  // Example: Lock the door by rotating the servo back to 0 degrees
  myservo.write(0);   // Lock position
  delay(5000);        // Wait for 5 seconds
}
