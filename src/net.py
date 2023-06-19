import network

import src.web as web


HEADER = """\
HTTP/1.1 {}
Content-Type: text/{}
Connection: close
"""

STATUS_OK = '200 OK'
STATUS_FOUND = '302 Found'
STATUS_404 = '404 Not Found'


def scramble(*args: str) -> bytes:
    return ('\n'.join(args) + "\n\n").encode('utf-8')


def parse_query(query: str) -> dict:
    params = {}
    for param in query.split("&"):
        key, value = param.split("=")
        params[key] = value.replace("+", " ").replace("%40", "@")
    return params


def get_params(path: str):
    path, query = path.split("?", 1)
    return path, parse_query(query)


def post_params(req: str):
    query = req.split("\r\n\r\n", 1)[1]
    return parse_query(query)


def generate_response(path: str, params: dict):
    status = STATUS_OK
    content = 'html'
    headers = []

    if path == '/css':
        content = 'css'
        body = web.css()
    elif path == '/sta':
        if 'ssid' in params and 'pw' in params:
            status = STATUS_FOUND
            headers.append('Location: /')
        else:
            sta = network.WLAN(network.STA_IF)
            sta.active(True)
            essid = sta.config('essid') or "None"
            networks = sta.scan()
            ssids = set(network[0].decode() for network in networks) 
            body = web.sta(essid, ssids)
    elif path == '/led':
        if 'v' in params:
            v = int(params['v'])
            web.led(v)
        body = web.led()
    elif path == '/fav':
        body = web.fav()
    else:
        sta = network.WLAN(network.STA_IF)
        ip = sta.ifconfig()[0] if sta.isconnected() else ""
        body = web.index(ip)

    header = HEADER.format(status, content)
    resp = scramble(header, *headers, '\r\n', body)
    
    return resp

def handle_request(req: bytes):
    req = str(req, 'utf-8')

    path = req.split(" ", 2)[1]

    # get parameters
    params = {}
    if req.startswith('GET'):
        if '?' in path:
            path, params = get_params(path)
    elif req.startswith('POST'):
        params = post_params(req)

    resp = generate_response(path, params)

    return path, params, resp
