import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp

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
message_interval = 5
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

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      client.publish(topic_pub, msg)
      #print ("publish msg ", msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
      print ("OSError:", e)
      restart_and_reconnect()


