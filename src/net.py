import network

import src.web as web


HEADER = """\
HTTP/1.1 {}"""

STATUS_OK = '200 OK'
STATUS_FOUND = '302 Found'
STATUS_404 = '404 Not Found'

HEADER_TYPE = 'Content-Type: text/{}'
HEADER_LOCATION = 'Location: {}'
HEADER_CLOSE = 'Connection: close'


def scramble(*args: str) -> bytes:
    h = ('\n'.join(args) + "\r\n").encode('utf-8')
    # print(str(h)) # debug
    return h


def parse_query(query: str) -> dict:
    params = {}
    for param in query.split("&"):
        key, value = param.split("=")
        params[key] = value.replace("+", " ").replace("%40", "@")
    print(params) # debug
    return params


def get_params(path: str):
    path, query = path.split("?", 1)
    # print(path, query) # debug
    return path, parse_query(query)


def post_params(req: str):
    query = req.split("\r\n\r\n", 1)[1]
    return parse_query(query)


def generate_response(path: str, params: dict):
    status = STATUS_OK
    headers = []
    body = ""

    if path == '/css':
        headers.append(HEADER_TYPE.format('css'))
        body = web.css()
    elif path == '/sta':
        if 'ssid' in params and 'pw' in params:
            status = STATUS_FOUND
            headers.append(HEADER_LOCATION.format('/'))
        else:
            headers.append(HEADER_TYPE.format('html'))
            sta = network.WLAN(network.STA_IF)
            sta.active(True)
            essid = sta.config('essid') or "None"
            networks = sta.scan()
            ssids = set(network[0].decode() for network in networks) 
            body = web.sta(essid, ssids)
    elif path == '/led':
        headers.append(HEADER_TYPE.format('html'))
        v = 0
        if 'v' in params:
            v = int(params['v'])
        body = web.led(v)
    elif path == '/fav':
        headers.append(HEADER_TYPE.format('html'))
        body = web.fav()
    else:
        headers.append(HEADER_TYPE.format('html'))
        sta = network.WLAN(network.STA_IF)
        ip = sta.ifconfig()[0] if sta.isconnected() else ""
        body = web.index(ip)

    headers.append(HEADER_CLOSE)

    header = HEADER.format(status)
    resp = scramble(header, *headers, "\r\n" + body)
    
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
