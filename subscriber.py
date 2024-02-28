import paho.mqtt.client as mqtt
import time
import json
global var
var=0

def on_connect(client, userdata, flags, rc):
    print(f"Subscriber: Connected with result code {rc}")
    client.subscribe("raspberry/+/topic")

def on_message(client, userdata, msg):
    global var
    var+=1
    topic=msg.topic
    # バイトオブジェクトをutf-8でデコードして文字列後jsonオブジェクトに変換する
    payload = json.loads(msg.payload.decode("utf-8").replace("'", '"'))
    print(f"Subscriber: {var} msg:{topic} {payload}")

client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

client.will_set("raspberry/status",b'{"status":"off"}')
client.connect("broker.emqx.io",1883,60)

client.loop_forever()
