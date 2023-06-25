# """
# --------------------------------------------------------------------------------
# FWINISM, Front-end Web-based IOT Networking Included System Module
# --------------------------------------------------------------------------------
# A simple web server for ESP32. This was going to be a module, but we ran out of budget (time).
# """


import esp
import gc
import usocket as socket
from machine import Pin, ADC
import network
import time
from umqtt.simple import MQTTClient
import _thread

import src.net as net


# variables
AP_SSID = 'citawarisan'
AP_PASSWORD = 'citawarisan'

led = Pin(2, Pin.OUT)
led_pin = Pin(16, Pin.OUT)
adc_pin = Pin(36, Pin.IN)
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IGNORE = ['favicon.ico']


def measure_light():
    # Reverse-bias the LED by setting the pin to LOW
    led_pin.off()
    time.sleep_ms(100)  # Allow time for the LED to discharge

    # Measure the voltage across the LED using the ADC
    adc = ADC(adc_pin)
    reading = adc.read()

    # Forward-bias the LED again by setting the pin to HIGH
    led_pin.on()

    return reading


def start_measure(client, TOKEN, ID):
    # print('Start measure')
    for i in range(10):
        # print('Loop', i)
        level = str(measure_light())
        json = '{ "device_developer_id": "' + ID + '", "data": {"light-level": "' + level + '"} }'
        # print(level)
        try:
            client.connect()
            client.publish(TOKEN + '/v2/streams', json)
            client.disconnect()
        except Exception as e:
            print("Failed to publish")
            print(e)
    else:
        print("Done!")


def wrap_up(path: str, params: dict) -> None:
    if params:
        if path == "/sta":
            ssid = params['ssid']
            password = params['pw']
            sta.disconnect()
            sta.connect(ssid, password)
            for _ in range(20):
                if sta.isconnected():
                    break
                time.sleep(0.5)
            if sta.isconnected():
                print('\nStation', 'IP:', sta.ifconfig()[0], '\n')
            else:
                sta.disconnect()
                print('Failed to connect')
        elif path == "/led":
            v = 0
            if 'v' in params:
                v = int(params['v'])
            led.value(v)
        elif path == "/fav":
            if 'token' in params and 'id' in params and 'data' in params:
                TOKEN, ID, DATA = params['token'], params['id'], params['data']
                client = MQTTClient(
                    "umqtt_client", "mqtt.favoriot.com", user=TOKEN, password=TOKEN)
                try:
                    client.connect()
                    client.publish(
                        TOKEN + "/v2/streams", '{ "device_developer_id": "' + ID + '", "data": {"test": "' + DATA + '"} }')
                    client.disconnect()
                except Exception as e:
                    print("Failed to publish")
                    print(e)
        elif path == "/req":
            if 'token' in params and 'id' in params:
                TOKEN, ID = params['token'], params['id']
                client = MQTTClient("umqtt_client", "mqtt.favoriot.com", user=TOKEN, password=TOKEN)
                _thread.start_new_thread(start_measure, (client, TOKEN, ID))


# logic
esp.osdebug(None)
gc.threshold(50000)

ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=3)

print('\nAccess Point', 'SSID:', AP_SSID, 'Password:',
      AP_PASSWORD, 'IP:', ap.ifconfig()[0], '\n')

s.bind(('', 80))
s.listen(5)

while True:
    # handle connection
    conn, addr = s.accept()
    req = str(conn.recv(1024), 'utf-8')

    # skip empty request
    if not req or any(path in req for path in IGNORE):
        continue

    # print('\nConnection:', addr)
    print(req.splitlines()[0])

    # handle request
    path, params, resp = net.handle_request(req)

    conn.sendall(resp)
    conn.close()

    # perform iot related task
    wrap_up(path, params)
