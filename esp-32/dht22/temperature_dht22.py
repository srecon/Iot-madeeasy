import dht
from machine import Pin, SoftI2C
from time import sleep
import oled_ssd1306

# use GPIO14 for DHT22
sensor = dht.DHT22(Pin(14))
# ESP32 Pin assignment for OLED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

while True:
  try:
    sleep(2) #sleep for 2 second which essential for DHT22
    
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    
    print('Temperature: %3.1f C' %temp)
    print('Humidity: %3.1f %%' %hum)
    print('===========')
    
    oled_width = 128
    oled_height = 64
    oled = oled_ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    
    oled.text('Temperature: %3.1f C' %temp, 0, 0)
    oled.text('Humidity: %3.1f %%' %hum, 0, 20)
    
    oled.show()
    
  except OSError as e:
    print('Failed to read sensor.')