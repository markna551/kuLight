from machine import Pin
import json
import time 
import network
from umqtt.robust import MQTTClient
from config import WIFI_PASS, WIFI_SSID
import kidbright as kb



def time_in_range(start, end, time_now):
    """Return true if time_now is in the range [start, end]"""
    if start <= end:
        return start <= time_now <= end
    else:
        return start <= time_now or time_now <= end

    
# Initialize
red_led = Pin(2, Pin.OUT)
green_led = Pin(12, Pin.OUT)
time_start = 18
time_end = 5
kb.init()
# Connect to the wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("*** Connecting to WiFi...")
wlan.connect(WIFI_SSID,WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
print("*** Wifi connected")
red_led.value(0)
# Connect to the broker topic...
mqtt = MQTTClient("auttakrit-6455", "iot.cpe.ku.ac.th")
print("*** Connecting to MQTT broker...")
mqtt.connect()
print("*** MQTT broker connected")
green_led.value(0)


while True:
    result = time.localtime()
    time_now = str(result[3]) + ":" + str(result[4]) + ":"+ str(result[5])

    if time_in_range(time_start,time_end,result[3]):
        print(time_now)
        data = {
            'light': kb.light(),
            'lat': 100.20,
            'lon':103.23
            }
        mqtt.publish('ku/daq2021/6210546455/IJM01', json.dumps(data))
        time.sleep(600)
    else :
        pass
