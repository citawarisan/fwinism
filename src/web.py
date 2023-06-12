import network
import re
from machine import Pin


# pseudoflask
def render_template(name: str, **ctx: dict) -> str:
    def f(match):
        key = match.group(1)
        return ctx[key] if key in ctx else match.group()
    return re.sub(r"\{\{(.+?)\}\}", f, open('templates/' + name).read())


def index() -> str:
    return render_template('index.html')


def wifi() -> str:
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    networks = wifi.scan()
    ssids = [network[0].decode() for network in networks]
    option = ""
    for ssid in ssids:
        option += "<option value='" + ssid + "'>" + ssid + "</option>"
    return render_template('wifi.html', option=option)


def led(value: int = 0) -> str:
    state = "ON" if value else "OFF"
    return render_template('led.html', state=state)


def handle(path: str, params: dict) -> str:
    if re.match(r'^/led(\?v=(0|1))?$', path):
        v = 0
        if 'v' in params:
            v = int(params['v'])
            Pin(2, Pin.OUT).value(v)
        return led(v)
    else:
        return index()
