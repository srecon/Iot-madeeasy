from machine import Pin
from time import sleep
try:
    import usocket as socket
except:
    import socket
import network

#  import email
#import pprint
#from io import StringIO

led = Pin(2, Pin.OUT)

def web_page():
  html = """<html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body>
    <h1>ESP Web Server, use the button below to control the led ligh connected to GPIO2</h1>
      <a href=\"?led=on\"><button>ON</button></a>&nbsp;
      <a href=\"?led=off\"><button>OFF</button></a></body>
    </html>"""
  return html

#def parse_http_header(httprequest):
    # pop the first line so we only process headers
#    _, headers = httprequest.split('\r\n', 1)

    # construct a message from the request string
#    message = email.message_from_file(StringIO(headers))

    # construct a dictionary containing the headers
#    headers = dict(message.items())
    
#    url = headers['Referer']
#    print ("URL:", url)
#    return url

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80)) #listning on local IP address on Port 80
s.listen(5) #five parallel connection
print ("Init webpage for controling led")
while True:
  try:
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    
    request = str(request)
    print('HTTP Request = %s' % request)
    #url = parse_http_header(request)
    #print ("URL:", url)
    
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    
    if led_on == 6:
      print('LED ON')
      led.value(1)
    if led_off == 6:
      print('LED OFF')
      led.value(0)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')
