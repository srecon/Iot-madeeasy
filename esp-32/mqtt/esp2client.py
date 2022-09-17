
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp


mqtt_server = "192.168.1.88"
port = 1883
mqtt_username= "mosquitto"
mqtt_password = "mosquitto"

client_id = ubinascii.hexlify(machine.unique_id())

topic_sub = b"notification"
topic_pub = b"hello"

#last_message = 0
#message_interval = 5
#counter = 0

def sub_cb(topic, msg):
  print((topic, msg))

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server, port, mqtt_username, mqtt_password)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected client 2 to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  #machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    new_message = client.check_msg()
    if new_message != 'None':
      client.publish(topic_pub, b'received')
    time.sleep(1)
  except OSError as e:
    restart_and_reconnect()