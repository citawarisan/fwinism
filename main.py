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


# functions
def collect_garbage(limit: int = 50000) -> None:
    mem = gc.mem_free()
    # print("\nFree Memory:", mem)
    if mem < limit:
        print('Collecting garbage...')
        gc.collect()


# logic
esp.osdebug(None)
collect_garbage()

ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=3)

print('\nAccess Point created')
print("SSID:", AP_SSID)
print("Password:", AP_PASSWORD)
print("IP:", ap.ifconfig()[0])

s.bind(('', 80))
s.listen(5)

while True:
    collect_garbage()

    # handle connection
    conn, addr = s.accept()
    print('\nConnection:', addr)
    req = str(conn.recv(1024), 'utf-8')
    print(req)

    # screw favicon
    if "/favicon.ico" in req:
        continue

    # process request
    resp = net.generate_response(req)
    # print(str(resp, 'utf-8'))

    conn.sendall(resp)
    conn.close()
