import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
count = 0
while True:
    GPIO.output(18,0)
    time.sleep(0.3)
    GPIO.output(18,1)
    time.sleep(0.3)
    count = count + 1
    if count>=105:
        GPIO.output(18,0)
        break



