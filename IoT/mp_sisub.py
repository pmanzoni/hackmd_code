# file: mp_sisub.py

from mqtt import MQTTClient
import pycom
import sys
import time

import ufun

wifi_user   = 'IOTPMxxx'
wifi_passwd = 'VOID'

THE_BROKER = "iot.eclipse.org"
THE_TOPIC = "test/RSElab"
CLIENT_ID = ""

def settimeout(duration):
   pass

def on_message(topic, msg):
    print("Received msg: ", str(msg), "with topic: ", str(topic))

### if __name__ == "__main__":

ufun.connect_to_wifi_UPVIoT(wifi_user, wifi_passwd)

client = MQTTClient(CLIENT_ID, THE_BROKER, 1883)
client.set_callback(on_message)

print ("Connecting to broker: " + THE_BROKER)
try:
	client.connect()
except OSError:
	print ("Cannot connect to broker: " + THE_BROKER)
	sys.exit()	
print ("Connected to broker: " + THE_BROKER)

client.subscribe(THE_TOPIC)

print('Waiting messages...')
while 1:
    client.check_msg()
