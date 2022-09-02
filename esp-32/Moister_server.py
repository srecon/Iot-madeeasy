from machine import ADC, Pin
from time import sleep
try:
    import usocket as socket
except:
    import socket
import network


SENSOR_PIN = 36 # ESP32 pin GIOP36 (ADC0) that connects to AOUT pin of moisture sensor
adc = ADC(Pin(SENSOR_PIN))

adc.atten(ADC.ATTN_11DB)    # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
adc.width(ADC.WIDTH_9BIT)   # set 9 bit return values (returned range 0-511)


def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body>
  <h1>First Sensor telemetry on Web!</h1>
  <p>Soil moisture value: <strong>""" + str(val) + """</strong></p>
  </body>
  </html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  val = adc.read() # read value, 0-4095 across voltage range 0.0v - 1.0v             
  print("Soil moisture value:", val)
  
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  
  response = web_page() # call the webpage function and return the html webpage
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()