import time
import threading
from bluepy import btle
from lib.switchbot import SwitchbotScanDelegate

macaddr='D1:E0:78:0E:BA:00'
scanner=btle.Scanner().withDelegate(SwitchbotScanDelegate(macaddr))

def worker():
    scanner.scan(4.0)
    sensorValue=scanner.delegate.sensorValue
    Temperature=f"{sensorValue['Temperature']:6.1f} "
    Humidity=f"{sensorValue['Humidity']:6.1f} "
    BatteryVoltage=f"{sensorValue['BatteryVoltage']:6.1f} "
    print(f"{time.time():.0f}  {Temperature} degC {Humidity} % {BatteryVoltage} %")

def schedule(interval, f, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

if __name__=="__main__":
    print('start')
    schedule(5, worker, True)
