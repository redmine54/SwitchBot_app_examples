import time
import threading
from bluepy import btle
from lib.switchbot import SwitchbotScanDelegate
import random

import paho.mqtt.client as mqtt
global tss
tss=time.time()

def on_connect(client, userdata, flags, rc):
    print(f"Publisher: Connected with result code {rc}")


macaddr='D1:E0:78:0E:BA:00'
scanner=btle.Scanner().withDelegate(SwitchbotScanDelegate(macaddr))

class MyThread(threading.Thread):

    def __init__(self, client, topic, cycle):
        super().__init__()
        self._client = client
        self._topic = topic
        self.scan_timeout = cycle-0.8

    def scan_switchbot(self):
        global tss
        sensorValues={}
        ts=time.time()
        current_time = time.localtime(ts)
        sensorValue={"type":'switchbot'}
        sensorValue["localtime"]=time.strftime('%Y-%m-%d %H:%M:%S',current_time)
        scanner.scan(self.scan_timeout)
        sensorValue.update(scanner.delegate.sensorValue)

        for i in range(40):
            # 各センサー値を乱数使用して変動させる（シミュレーション）
            topic=self._topic.replace("[x]",f"A{(i+1):03}")
            sensorValues[topic]=sensorValue.copy()
            sensorValues[topic]['Temperature']=round(sensorValues[topic]['Temperature']+(random.random()*10),1)
            sensorValues[topic]['Humidity']=round(sensorValues[topic]['Humidity']+(random.random()*20))
            sensorValues[topic]['BatteryVoltage']=round(sensorValues[topic]['BatteryVoltage']+(random.random()*5))
        #    print(topic, sensorValues[topic]['Temperature'],sensorValues[topic]['Humidity'],sensorValues[topic]['BatteryVoltage'])
        return sensorValues

    def run(self):
        global tss
        ts=time.time()
        # センサーのデータスキャン
        sensorValues=self.scan_switchbot()
        ts1=time.time()
        for topic in sensorValues.keys():
            # スキャンデータを送信
            self._client.publish(topic, payload=str(sensorValues[topic]), qos=0, retain=False)

        print(f"{ts:.0f} cycle:{(ts-tss):.6f}  SwitchBot Scan:{(ts1-ts):.3f} sec")
        tss=ts

def schedule(interval, worker, wait=True):

    client=mqtt.Client()
    client.on_connect=on_connect
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_start()
    topic='raspberry/[x]/topic'

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
