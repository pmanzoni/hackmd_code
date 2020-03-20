# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
from LIS2HH12 import LIS2HH12           # 3-Axis Accelerometer
from SI7006A20 import SI7006A20         # Humidity and Temperature Sensor
from LTR329ALS01 import LTR329ALS01     # Digital Ambient Light Sensor
from raw2lux import raw2Lux             # ... additional library for the light sensor
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE  # Barometric Pressure Sensor with Altimeter 

py = Pysense()

# Digital Ambient Light Sensor
lite_s = LTR329ALS01(py)
print("Light raw (channel Blue lux, channel Red lux): " + str(lite_s.light()))
print("Light (raw2lux): " + str(raw2Lux(lite_s.light())))


# Barometric Pressure Sensor with Altimeter
bara_s = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters.
barp_s = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pascals.
print("MPL3115A2 temperature: " + str(bara_s.temperature()))
print("Altitude: " + str(bara_s.altitude()))
print("Pressure: " + str(barp_s.pressure()))

# Humidity and Temperature Sensor
temp_s = SI7006A20(py)
print("Temperature: " + str(temp_s.temperature())+ " deg C and Relative Humidity: " + str(temp_s.humidity()) + " %RH")
print("Dew point: "+ str(temp_s.dew_point()) + " deg C")

# 3-Axis Accelerometer
acel_s = LIS2HH12(py)
print("Acceleration: " + str(acel_s.acceleration()))
print("Roll: " + str(acel_s.roll()))
print("Pitch: " + str(acel_s.pitch()))

# ... and also..
print("Battery voltage: " + str(py.read_battery_voltage()))