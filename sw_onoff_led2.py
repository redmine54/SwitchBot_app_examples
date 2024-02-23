import RPi.GPIO as GPIO
import time
import sys
import threading

Sw_pin=23
Led_pin=24
Led_pin_w=12
Led_pin_b=16
Led_pin_y=20
Led_pin_g=21
GPIO_Leds=[Led_pin,Led_pin_w,Led_pin_b,Led_pin_y,Led_pin_g]

GPIO.setmode(GPIO.BCM)
GPIO.setup(Led_pin, GPIO.OUT)
GPIO.setup(Led_pin_w, GPIO.OUT)
GPIO.setup(Led_pin_b, GPIO.OUT)
GPIO.setup(Led_pin_y, GPIO.OUT)
GPIO.setup(Led_pin_g, GPIO.OUT)
GPIO.setup(Sw_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def countup(GPIO_Leds):
    global Count
    while True:
        if Status!=0:
            n = Count % 32
            Count = Count + 1
            bitmasks=[0b10000, 0b1000, 0b100, 0b10, 0b1]
            for i,(bitmask, GPIO_Led) in enumerate(zip(bitmasks, GPIO_Leds)):
                if bin(n & bitmask) != '0b0':
                    GPIO.output(GPIO_Led, GPIO.HIGH)
                else:
                    GPIO.output(GPIO_Led, GPIO.LOW)
        time.sleep(1)
def main():
    global Status
    global Count
    Status=0
    Count =0

    print(f"start {GPIO_Leds}")

    thread1 = threading.Thread(name='thread1', target=countup, args=(GPIO_Leds,))
    print(f"thread={thread1}")
    thread1.start()

    while True:
        try:
            sw = GPIO.input(Sw_pin)
            if sw==1:
                Status = abs(Status - 1)
                print(f"sw={sw} Status={Status}")
                while GPIO.input(Sw_pin):
                    time.sleep(0.1)
            time.sleep(0.1)

        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()

if __name__=='__main__':
    main()
