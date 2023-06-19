import re


# pseudoflask
def render_template(name: str, **ctx: dict) -> str:
    def f(m):
        key = m.group(1)
        if key in ctx:
            return ctx[key] 
        return m.group()
    return re.sub(r"\{\{(.+?)\}\}", f, open('templates/' + name).read())


def index(sta_addr: str) -> str:
    return render_template('index.html', sta_addr=sta_addr)


def sta(essid: str = None, ssids: set = set()) -> str:
    options = "".join(f"<option value='{ssid}'>{ssid}</option>" for ssid in ssids)
    return render_template('sta.html', essid=essid, options=options)


def css() -> str:
    return render_template('main.css')


def led(value: int = 0) -> str:
    state = "ON" if value else "OFF"
    return render_template('led.html', state=state)


def fav() -> str:
    return render_template('fav.html')
