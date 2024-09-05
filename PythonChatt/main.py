# -*- coding: utf-8 -*-
import paho.mqtt.client as paho
import json

running = True
configDone = False
connected = False

name = input('What is your name? : ')
topic = input('Enter a chatroom : ')

# Callback when a message is received
def on_message(client, userdata, msg):
    messageObj = json.loads(msg.payload.decode("utf-8"))
    if messageObj["name"] != name:
        print("\n" + messageObj["name"] + " said: " + messageObj["message"])

# Callback when connection is established
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nConnected, start chatting!")
        client.subscribe("nackademinchat/" + topic)
    else:
        print(f"Connection failed with code {rc}")

# Initialize the MQTT client
client = paho.Client(client_id=name, clean_session=True, userdata=None, protocol=paho.MQTTv311)

# Set a 'last will' message in case of disconnection
client.will_set("nackademinchat/" + topic, payload=json.dumps({"name": name, "message": "Disconnected"}), qos=0, retain=False)

# Connect to the MQTT broker
client.connect("test.mosquitto.org", 1883)

# Assign the callback functions
client.on_message = on_message
client.on_connect = on_connect

# Start the MQTT loop in a separate thread
client.loop_start()

# Main loop for sending messages
try:
    while True:
        message = input()
        tempMess = {"name": name, "message": message}
        client.publish("nackademinchat/" + topic, json.dumps(tempMess), qos=1)
except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()
    client.loop_stop()
