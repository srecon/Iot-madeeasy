from machine import ADC, Pin
from time import sleep


SENSOR_PIN = 36 # ESP32 pin GIOP36 (ADC0) that connects to AOUT pin of moisture sensor
adc = ADC(Pin(SENSOR_PIN))

adc.atten(ADC.ATTN_11DB)    # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
adc.width(ADC.WIDTH_9BIT)   # set 9 bit return values (returned range 0-511)

while True:
    val = adc.read() # read value, 0-4095 across voltage range 0.0v - 1.0v             
    print("Soil moisture value:", val)
    print ("raw analog value:", adc.read_u16()) # read a raw analog value in the range 0-65535
    print ("analog value in microvolts:", adc.read_uv()) # read an analog value in microvolts
    #delay for 1 second
    sleep(1)