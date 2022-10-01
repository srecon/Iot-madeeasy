import time
from umqttsimple import MQTTClient
import ubinascii
from machine import Pin, SoftI2C
import micropython
import network
import esp
import machine

import dht
from time import sleep
import oled_ssd1306

# use GPIO14 for DHT22
sensor = dht.DHT22(Pin(14))
# ESP32 Pin assignment for OLED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

esp.osdebug(None)
import gc

gc.collect()

mqtt_server = "192.168.1.88"
port = 1883
mqtt_username= "mosquitto"
mqtt_password = "mosquitto"

client_id = ubinascii.hexlify(machine.unique_id())

topic_sub = b"notification"
topic_pub = b"hello"

last_message = 0
message_interval = 2
counter = 0


def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server, port, mqtt_username, mqtt_password)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected client 1 to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))

  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  #machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

# collect & sending the metrics
while True:
  try:
    client.check_msg()
    ## collecting DHT22 metrics
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
    ### sending the metrics to MQTT
    if (time.time() - last_message) > message_interval:
      msg = b'weather,location=Moscow temperature=%3.1f,Humidity=%3.1f' %(temp, hum)
      client.publish(topic_pub, msg)
      print ("publish msg ", msg)
      last_message = time.time()

  except OSError as e:
      print ("OSError:", e)
      restart_and_reconnect()
