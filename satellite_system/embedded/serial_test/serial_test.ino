uint8_t serial_in;
const uint8_t led_pin = 8;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(led_pin, OUTPUT);
}

void loop() {
  while (!Serial.available());
  serial_in = Serial.readString().toInt();
  Serial.print(serial_in);

  if(serial_in == 1)
  {
    digitalWrite(led_pin, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                       // wait for a second
    digitalWrite(led_pin, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);     
  }
}
