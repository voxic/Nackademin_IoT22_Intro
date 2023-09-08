# -*- coding: utf-8 -*-
import paho.mqtt.client as paho
import json


running = True
configDone = False
connected = False


name = input('What is your name? : ')
topic = input('Enter a chatroom : ')


def on_message(client, userdata, msg):
    messageObj = json.loads(str(msg.payload.decode("utf-8")))
    if(messageObj["name"] != name):
        print("\n" + messageObj["name"] + " said: " + messageObj["message"])

def on_connect(client, userdata, flags, rc):
    print("\n" + "Connected, start chatting!")
    client.subscribe("nackademinchat/"+topic)

# Connect to MQTT and report in
client = paho.Client(name,True, None, paho.MQTTv31)
client.will_set("nackademinchat/"+topic, payload=json.dumps({"name": name, "message" : "Disconnected"}), qos=0, retain=False)
client.connect("test.mosquitto.org", 1883)
client.on_message = on_message 
client.on_connect = on_connect
client.loop_start()



while True:
    message = input()
    tempMess = {"name" : name, "message":message}
    client.publish("nackademinchat/"+topic, json.dumps(tempMess), qos=1)



