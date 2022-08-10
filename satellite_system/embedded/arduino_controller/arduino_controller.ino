#include <Servo.h>
Servo myservo;  // create servo object to control a servo

String serial_in;
const uint8_t led_pin = 8;

// Global temp variables
uint8_t temp_sensors[] = {A0, A1};  //, A2, A3, A4, A5};
double prev_temps[] = {0.0, 0.0};   //, 0.0, 0.0, 0.0, 0.0};
double temps[] = {0.0, 0.0};        //, 0.0, 0.0, 0.0, 0.0};
uint8_t num_temp_sensors = 2;

static unsigned long TELEMETRY_PERIOD = 1000; // 1000 ms default between telemetry grabs

// Servo & Fan Global variables
int fullpos = 0; // ***Update based on final model setup!
int halfpos = 90; // ***Update based on final model setup!
int closepos = 180; // ***Update based on final model setup!
int currentservopos = 180; // ***Update based on final model setup!
int fan_speed = 0;
int fan_level = 0;
int fancontrol_pin = 11;
const int fanfeedback_pin = 2; // define the interrupt pin (must be pin 2 or 3)
int InterruptCounter;

double updateTempData(uint8_t sensor_id);
void sendTelemetry();
void runCommand(String serial);
void refreshTelemetryData();

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(led_pin, OUTPUT);
  pinMode(fancontrol_pin, INPUT);
  myservo.attach(9); // attaches the servo on pin 9 to the servo object
  myservo.write(currentservopos);
  analogWrite(fancontrol_pin,fan_level);
}

void loop() {
  static unsigned long last_refresh_time = 0;

  // Check if commands are available and run them
  if(Serial.available())
  {
    serial_in = Serial.readString();
    runCommand(serial_in);
  }

  // Check if 1 second has passed, and if so send telemetry data
  if(millis() - last_refresh_time >= TELEMETRY_PERIOD)
  {
    last_refresh_time += TELEMETRY_PERIOD;
    sendTelemetry();
  }

  // Telemetry is being updated all the time in the background
  refreshTelemetryData();
}

void runCommand(String serial)
{
  uint8_t cmd = serial.substring(0,1).toInt(); // Grabs just the first character
  String args = serial.substring(2); // Grabs everything past the first comma
  if(cmd == 0)  // Config Parameters
  {
    double freq = args.substring(0,4).toDouble();
    TELEMETRY_PERIOD = (1.0/freq)*1000; // convert freq to period in millis
  }
  if(cmd == 1)  // SetServoPosition
  {
    uint8_t servo_pos = args.substring(0,3).toInt(); // Grabs the first substring within "args" string
    if (servo_pos == 2)
    {
      myservo.write(fullpos);
      currentservopos = 0; // this will be adjusted once final model is built
      //Serial.println("full cmd received");
    }
    else if (servo_pos == 1)
    {
      myservo.write(halfpos);
      currentservopos = 90; // this will be adjusted once final model is built
      //Serial.println("half cmd received");
    }
    else if (servo_pos == 0)
    {
      myservo.write(closepos);
      currentservopos = 180; // this will be adjusted once final model is built
      //Serial.println("clse cmd received");
    } 
  }
  if(cmd == 2)  // SetFanSpeed
  {
    for(int i = 0; i < 10; i++){
      digitalWrite(led_pin, HIGH);
      delay(1000);
      digitalWrite(led_pin, LOW);
      delay(1000);
    }
    int fan_speed = args.substring(0,3).toInt(); // Grabs the first substring within "args" string
    fan_level = map(fan_speed, 0, 100, 0, 255); // Below 40% the fanspeed doesn't seem to change
    analogWrite(fancontrol_pin,fan_level);
    // Serial.println("fan cmd received"); TODO: remove when done testing
  }
}

void sendTelemetry()
{
  // Telemetry is sent in a csv format and parsing must be implemented in the HAL
  // E.g. temp = 1,26.30 translates into telemetry type 1 and 26.30 degrees C
  
  // Send temperature data
  double temp = 0;
  for(int i = 0; i < num_temp_sensors; i++){
    String serial_data = "0," + String(i) + "," + String(temps[i], 2);
    Serial.println(serial_data);
  }
/*
  // Send servo position
  String serial_servo = "1," + String(currentservopos);
  Serial.println(serial_servo); // Send servomotor position

  // Send the current fan speed
  double fanspeed;
  // Interrupt counter to read tachometer signal pulses
  InterruptCounter = 0;
  attachInterrupt(digitalPinToInterrupt(fanfeedback_pin), counter, RISING);
  delay(500); // This pauses all execution, we need to swap out with non blocking version or reduce time
  detachInterrupt(digitalPinToInterrupt(fanfeedback_pin));
  fanspeed = (InterruptCounter / 2) * 120; // calculates fan speed from tachometer pulses
  String serial_fan = "2," + String(fanspeed);
  Serial.println(serial_fan); // Send fan speed
*/
}

void refreshTelemetryData(){
  // TODO: Include other data updates here
  updateTempData();
}

double updateTempData()
{
  for(int i = 0; i < num_temp_sensors; i++){
    temps[i] = analogRead(temp_sensors[i])*(5000/1024.0);  // Averaging filter
    temps[i] = (temps[i]-110)/10;     // 110 is magic offset for TMP35
    prev_temps[i] = temps[i];
    temps[i] = (temps[i] + prev_temps[i])/2.0;
  }
}

void counter()
{
  InterruptCounter++;
}
