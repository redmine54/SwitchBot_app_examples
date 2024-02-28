import time
import threading
from bluepy import btle
from lib.switchbot import SwitchbotScanDelegate

macaddr='D1:E0:78:0E:BA:00'
scanner=btle.Scanner().withDelegate(SwitchbotScanDelegate(macaddr))

def worker():
    scanner.scan(4.0)
    current_time = time.localtime(time.time())
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    sensorValue=scanner.delegate.sensorValue
    Temperature=f"{sensorValue['Temperature']:6.1f} "
    Humidity=f"{sensorValue['Humidity']:6.1f} "
    BatteryVoltage=f"{sensorValue['BatteryVoltage']:6.1f} "
    payload={
        "localtime":formatted_time,
        "Temperature":Temperature,
        "Humidity":Humidity,
        "BatteryVoltage":BatteryVoltage,
    }
    print(f"{formatted_time}  {Temperature} degC {Humidity} % {BatteryVoltage} %")

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
