import esp
import gc
import usocket as socket
from machine import Pin
import network
import time

import src.net as net


# variables
AP_SSID = 'citawarisan'
AP_PASSWORD = 'citawarisan'

led = Pin(2, Pin.OUT)
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IGNORE = ['favicon.ico']


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
            print('\nStation')
            if sta.isconnected():
                print("IP:", sta.ifconfig()[0])
            else:
                sta.disconnect()
                print("Failed to connect")
        elif path == "/led":
            v = 0
            if 'v' in params:
                v = int(params['v'])
            led.value(v)


# logic
esp.osdebug(None)
gc.threshold(50000)

ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=3)

print('\nAccess Point')
print("SSID:", AP_SSID)
print("Password:", AP_PASSWORD)
print("IP:", ap.ifconfig()[0])

s.bind(('0.0.0.0', 80))
s.listen(5)

while True:
    # handle connection
    conn, addr = s.accept()
    req = str(conn.recv(1024), 'utf-8')

    # ignore irrelevant requests
    if any(path in req for path in IGNORE):
        continue

    print('\nConnection:', addr)
    print(req.splitlines()[0])

    # handle request
    path, params, resp = net.handle_request(req)

    conn.sendall(resp)
    conn.close()

    wrap_up(path, params)
