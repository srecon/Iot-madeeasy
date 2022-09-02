from machine import Pin
from time import sleep

# use GPIO2 onboard led light
led = Pin(2, Pin.OUT)

while True:
    print("Blink the blue led by 0.5 second")
    led.value (not led.value())
    sleep(0.5)
