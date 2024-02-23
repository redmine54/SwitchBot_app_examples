import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Subscriber: Connected with result code {rc}")
    client.subscribe("raspberry/topic")

def on_message(client, userdata, msg):
    print(f"Subscriber: msg:{msg.topic} {msg.payload}")

client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

client.will_set("raspberry/status",b'{"status":"off"}')
client.connect("broker.emqx.io",1883,60)

client.loop_forever()

