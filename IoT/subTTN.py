import sys
import time
import base64

import json
import struct

import paho.mqtt.client as mqtt

THE_BROKER = "eu.thethings.network"
THE_TOPIC = "+/devices/+/up"

# SET HERE THE VALUES OF YOUR APP AND DEVICE:
# TTN_USERNAME is the Application ID
TTN_USERNAME = "VOID"
# TTN_PASSWORD is the Application Access Key, in the bottom part of the Overview section of the  "Application"  window.
TTN_PASSWORD = "VOID"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "return code: ", rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(THE_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    themsg = json.loads(msg.payload.decode("utf-8"))

    payload_raw = themsg["payload_raw"]
    payload_plain = base64.b64decode(payload_raw)
    vals = struct.unpack(">fff", payload_plain)

    gtw_id = themsg["metadata"]["gateways"][0]["gtw_id"]
    rssi = themsg["metadata"]["gateways"][0]["rssi"]

    print("%s, rssi=%d" % (gtw_id, rssi))
    print("@%s >> temp=%.3f hum=%.3f lux=%.3f" % (time.strftime("%H:%M:%S"), vals[0], vals[1], vals[2]))



client = mqtt.Client()

# Let's see if you inserted the required data
if TTN_USERNAME == 'VOID':
    print("You must set the values of your app and device first!!")
    sys.exit()
client.username_pw_set(TTN_USERNAME, password=TTN_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(THE_BROKER, 1883, 60)

client.loop_forever()
