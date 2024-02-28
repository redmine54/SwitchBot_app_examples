import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Publisher: Connected with result code {rc}")
    #for i in range(5):
    #    client.publish('raspberry/topic', payload=i, qos=0, retain=False)
    #    print(f"Publisher: Send {i} to raspberry/topic")

client=mqtt.Client()
client.on_connect=on_connect
client.connect("broker.emqx.io", 1883, 60)
client.loop_start()
i=0
#rc=True
topic='raspberry/topic'
cycle_time=1
while i<10:
    client.publish(topic, payload=i, qos=0, retain=False)
    print(f"Publisher: Send {i} to {topic}")
    time.sleep(cycle_time)
    i+=1

client.disconnect()
client.loop_stop()
#client.loop_forever()
