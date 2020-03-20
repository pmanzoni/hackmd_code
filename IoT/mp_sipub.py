# file: mp_sipub.py

from mqtt import MQTTClient
import pycom
import sys
import time

import ufun

wifi_user   = 'IOTPMxxx'
wifi_passwd = 'VOID'

THE_BROKER = "iot.eclipse.org"
THE_TOPIC = "test/SRM2018"
CLIENT_ID = ""

def settimeout(duration):
   pass

def get_data_from_sensor(sensor_id="RAND"):
    if sensor_id == "RAND":
        return ufun.random_in_range()

### if __name__ == "__main__":

ufun.connect_to_wifi_UPVIoT(wifi_user, wifi_passwd)

client = MQTTClient(CLIENT_ID, THE_BROKER, 1883)

print ("Connecting to broker: " + THE_BROKER)
try:
    client.connect()
except OSError:
    print ("Cannot connect to broker: " + THE_BROKER)
    sys.exit()  
print ("Connected to broker: " + THE_BROKER)

print('Sending messages...')
while True:
    # creating the data
    the_data = get_data_from_sensor()
    # publishing the data
    client.publish(THE_TOPIC, str(the_data))
    print("Published message with value: {}".format(the_data))
    time.sleep(1)
