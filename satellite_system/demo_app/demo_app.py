# Test application using python
import RPi.GPIO as GPIO
import time


if __name__=='__main__':
    print("Starting demo app... Go team insects!")

    # GPIO Pin setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)

    # Blink LED on and off 10 times
    for i in range(0,10):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)
