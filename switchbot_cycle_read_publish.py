import time
import threading
from bluepy import btle
from lib.switchbot import SwitchbotScanDelegate

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Publisher: Connected with result code {rc}")


macaddr='D1:E0:78:0E:BA:00'
scanner=btle.Scanner().withDelegate(SwitchbotScanDelegate(macaddr))

class MyThread(threading.Thread):
    def __init__(self, client, topic, cycle):
        super().__init__()
        self._client = client
        self._topic = topic
        self._cycle = cycle-0.6

    def run(self):
        topic=self._topic
        sensorValue={"type":'switchbot'}
        current_time = time.localtime(time.time())
        sensorValue["localtime"]=time.strftime('%Y-%m-%d %H:%M:%S',current_time)
        # scan switchbot value
        scanner.scan(self._cycle)
        sensorValue.update(scanner.delegate.sensorValue)

        ts=time.time()
        for i in range(20):
            self._client.publish(topic, payload=str(sensorValue), qos=0, retain=False)

        print(f"{time.time():.0f} {(time.time()-ts)/1000:0.6f} sec")

def schedule(interval, worker, wait=True):

    client=mqtt.Client()
    client.on_connect=on_connect
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_start()
    topic='raspberry/11/topic'

    base_time = time.time()
    next_time = 0
    flag=True
    while flag:
        t = worker(client, topic, interval)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

    client.disconnect()
    client.loop_stop()

if __name__=="__main__":
    print('start')
    schedule(5, MyThread, True)
    print('end')
