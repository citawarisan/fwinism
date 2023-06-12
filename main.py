import esp
import gc
import usocket as socket
from machine import Pin
import network

import src.net as net


# variables
AP_SSID = 'citawarisan'
AP_PASSWORD = 'citawarisan'

led = Pin(2, Pin.OUT)
ap = network.WLAN(network.AP_IF)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# logic
esp.osdebug(None)
gc.threshold(50000)

ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=3)

print('\nAccess Point created')
print("SSID:", AP_SSID)
print("Password:", AP_PASSWORD)
print("IP:", ap.ifconfig()[0])

s.bind(('', 80))
s.listen(5)

while True:
    # handle connection
    conn, addr = s.accept()
    req = str(conn.recv(1024), 'utf-8')

    # screw favicon
    if "/favicon.ico" in req:
        continue

    print('\nConnection:', addr)
    print(req)

    # process request
    resp = net.generate_response(req)
    # print(str(resp, 'utf-8'))

    conn.sendall(resp)
    conn.close()
