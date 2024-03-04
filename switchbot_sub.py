import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import json
from datetime import datetime as dt

load_dotenv(".env")
broker_host=os.environ.get("broker_host")
broker_port=int(os.environ.get("broker_port"))
broker_timeout=int(os.environ.get("broker_timeout"))
broker_topic=os.environ.get("broker_topic")

global count, record, key
count=0
record={}
key=''

def update_db(var, point, payload):
    print(f"{payload['localtime']} {var} {point} {payload['SensorType']} {payload['Temperature']} {payload['Humidity']} {payload['BatteryVoltage']} :Subscriber")

def countup(var, point, payload):
    global record, key
    if not any(record):
        key=payload['localtime']
        record[key]=1
    elif key == payload['localtime']:
        record[key]+=1
    else:
        now = dt.strptime(payload['localtime'], '%Y-%m-%d %H:%M:%S')
        pre = dt.strptime(key, '%Y-%m-%d %H:%M:%S')
        strdt=f"{now-pre}"
        print(key, point,record[key], strdt , \
            f"{payload['SensorType']} {payload['Temperature']} {payload['Humidity']} {payload['BatteryVoltage']}" )

        del record[key]
        key=payload['localtime']
        record[key]=1

def on_connect(client, userdata, flags, rc):
    print(f"Subscriber: Connected with result code {rc}")
    client.subscribe(broker_topic)

def on_message(client, userdata, msg):
    global count
    count+=1
    try:
        topic=msg.topic
        point=topic.split('/')[1]

        # バイトオブジェクトをutf-8でデコードして文字列後jsonオブジェクトに変換する
        payload = json.loads(msg.payload.decode("utf-8").replace("'", '"'))
        #print(f'>> {msg.payload.decode("utf-8")}')
        countup(count, point, payload)

        if point=='A001':
            pass
            #update_db(count, point, payload)
        if point=='A040':
            pass
            #update_db(count, point, payload)
    except :
        #print(f"{count} {msg.topic} {msg.payload}")
        #print(f'>> {msg.payload.decode("utf-8")}')
        pass

print(broker_host)
client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

client.will_set("raspberry/status",b'{"status":"off"}')
client.connect(broker_host, broker_port, broker_timeout)

client.loop_forever()
