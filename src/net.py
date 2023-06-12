import src.web as web


RESPONSE = 'HTTP/1.1 {}'
STATUS_OK = '200 OK'
STATUS_404 = '404 Not Found'

HEADER_CONTENT = 'Content-Type: text/{}'
CONTENT_HTML = 'html'
CONTENT_CSS = 'css'

HEADER_CLOSE = 'Connection: close'


def scramble(*args: str) -> bytes:
    return ('\n'.join(args) + "\n\n").encode('utf-8')


def get_param(path: str):
    params = {}
    if "?" in path:
        path, tmp = path.split("?", 1)
        for param in tmp.split("&"):
            key, value = param.split("=")
            params[key] = value.replace("+", " ")
    return path, params


def generate_response(req: str) -> bytes:
    method, path, _ = req.split(" ", 2)
    resp = RESPONSE.format(STATUS_404)
    if method == "GET":
        if path == "/css":
            resp = scramble(
                RESPONSE.format(STATUS_OK),
                HEADER_CONTENT.format(CONTENT_CSS),
                "\n", web.render_template("main.css")
            )
        elif "/sta" in path:
            path, params = get_param(path)
            if params:
                resp = scramble(
                    RESPONSE.format("302 Found"),
                    HEADER_CONTENT.format(CONTENT_HTML),
                    "Location: /sta",
                    "\n", web.handle(path, params)
                )
            else:
                resp = scramble(
                    RESPONSE.format(STATUS_OK),
                    HEADER_CONTENT.format(CONTENT_HTML),
                    HEADER_CLOSE, "\n", web.handle(path, params)
                )
        else:
            path, params = get_param(path)
            resp = scramble(
                RESPONSE.format(STATUS_OK),
                HEADER_CONTENT.format(CONTENT_HTML),
                HEADER_CLOSE, "\n", web.handle(path, params)
            )
    return resp
