import network
import re


# pseudoflask
def render_template(name: str, **ctx: dict) -> str:
    def f(m):
        key = m.group(1)
        if key in ctx:
            return ctx[key] 
        return m.group()
    return re.sub(r"\{\{(.+?)\}\}", f, open('templates/' + name).read())


def index() -> str:
    return render_template('index.html')


def wifi() -> str:
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    essid = sta.config('essid') or "None"
    networks = sta.scan()
    ssids = [network[0].decode() for network in networks]
    options = ""
    for ssid in ssids:
        options += "<option value='" + ssid + "'>" + ssid + "</option>"
    return render_template('sta.html', essid=essid, options=options)


def css() -> str:
    return render_template('main.css')


def led(value: int = 0) -> str:
    state = "ON" if value else "OFF"
    return render_template('led.html', state=state)
