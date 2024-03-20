#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import time
import datetime as dt
from datetime import timezone
from zoneinfo import ZoneInfo
from tzlocal import get_localzone

import threading
from bluepy import btle
from lib.switchbot import SwitchbotScanDelegate
import random

import paho.mqtt.client as mqtt
global tss
tss=time.time()

def on_connect(client, userdata, flags, rc):
    print(f"Publisher: Connected with result code {rc}")

load_dotenv(".env")
broker_host=os.environ.get("broker_host")
broker_port=int(os.environ.get("broker_port"))
broker_timeout=int(os.environ.get("broker_timeout"))
broker_topic=os.environ.get("broker_topic")
broker_qos=int(os.environ.get("broker_qos"))

time_format=os.environ.get('time_format')
macaddr=os.environ.get('macaddr')
topicbase=os.environ.get("topic_base")
retain = False if os.environ.get("retain") == 'False' else True

copycount=int(os.environ.get("copycount"))
cycle=int(os.environ.get("cycle"))

scanner=btle.Scanner().withDelegate(SwitchbotScanDelegate(macaddr))

class MyThread(threading.Thread):

    def __init__(self, client, topic, cycle):
        super().__init__()
        self._client = client
        self._topic = topic
        self.scan_timeout = cycle-2.0

    def scan_switchbot(self):
        global tss
        sensorValues={}
        TZ = str(get_localzone())  # TimeZone
        now_utc = dt.datetime.now(timezone.utc)  # UTC
        str_utc=str(now_utc.strftime(time_format))
        sensorValue={}
        sensorValue["tzLocal"]=TZ
        sensorValue["utctime"]=str_utc
        sensorValue["timeformat"]=time_format
        scanner.scan(self.scan_timeout)
        sensorValue.update(scanner.delegate.sensorValue)

        for i in range(copycount):
            # 各センサー値を乱数使用して変動させる（シミュレーション）
            topic=self._topic.replace("[x]",f"A{(i+1):03}")
            sensorValues[topic]=sensorValue.copy()
            sensorValues[topic]['Temperature']=round(sensorValues[topic]['Temperature']+(random.random()*10),1)
            sensorValues[topic]['Humidity']=round(sensorValues[topic]['Humidity']+(random.random()*20))
            sensorValues[topic]['BatteryVoltage']=round(sensorValues[topic]['BatteryVoltage']+(random.random()*5))
        return sensorValues

    def run(self):
        global tss
        ts=time.time()
        now=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # センサーのデータスキャン
        sensorValues=self.scan_switchbot()
        ts1=time.time()
        for topic in sensorValues.keys():
            # スキャンデータを送信
            self._client.publish(topic, payload=str(sensorValues[topic]), qos=broker_qos, retain=retain)

        print(f"{now} cycle:{(ts-tss):.6f}  SwitchBot Scan:{(ts1-ts):.3f} sec")
        tss=ts

def schedule(interval, worker, wait=True):

    client=mqtt.Client()
    client.on_connect=on_connect
    client.connect(broker_host, broker_port, broker_timeout)
    client.loop_start()

    base_time = time.time()
    next_time = 0
    flag=True
    while flag:
        t = worker(client, topicbase, interval)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

    client.disconnect()
    client.loop_stop()

if __name__=="__main__":
    print('start')
    schedule(cycle, MyThread, True)
    print('end')
