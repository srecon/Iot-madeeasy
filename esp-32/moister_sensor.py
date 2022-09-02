from machine import Pin
from time import sleep

# ESP32 pin GIOP36 (ADC0) that connects to AOUT pin of moisture sensor
AOUT_PIN = 36
Sensor_Pin = Pin(AOUT_PIN, Pin.IN)

while True:
    print("Soil moisture sensor test, value:", Sensor_Pin.value())
    #delay for 1 second
    sleep(1)
