# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import time
import network
#esp.osdebug(None)
#import webrepl
#webrepl.start()
routerSSID = 'Keenetic-8913'
routerPassword = 'MQmfpZbW'

def station_setup(routerSSID, routerPass):
    print ("Init station mode setup")
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print ('Connecting to router...', routerSSID)       
        sta_if.active(True)
        sta_if.connect(routerSSID, routerPass)
        while not sta_if.isconnected():
            pass
    print ('Connected to router:', routerSSID, 'IP address:', sta_if.ifconfig())    
    print ("Setup end.")   
try:
    station_setup (routerSSID, routerPassword)
except:
    sta_if.disconnect()