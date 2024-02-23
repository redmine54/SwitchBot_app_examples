import RPi.GPIO as GPIO
import time
import sys

Sw_pin=23
Led_pin=24

Status=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(Sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Led_pin, GPIO.OUT)
print("start ")
GPIO.setup(Sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while True:
    try:
        print(f"{GPIO.input(Sw_pin)}")
        if(Status==0):
            GPIO.output(Led_pin, GPIO.HIGH)
            Status=1
        else:
            GPIO.output(Led_pin, GPIO.LOW)
            Status=0
        while(GPIO.input(Sw_pin)==0):
            time.sleep(0.1)
            GPIO.output(Led_pin, GPIO.LOW)
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()


 
