import src.web as web


STATUS_OK = "200 OK"
DEFAULT = """HTTP/1.1 {}
Content-Type: text/html
Connection: close
{}

{}"""


def get_param(path: str):
    params = {}
    if "?" in path:
        path, tmp = path.split("?", 1)
        for param in tmp.split("&"):
            key, value = param.split("=")
            params[key] = value
    # print(params)
    return path, params


def generate_response(req: str) -> bytes:
    method, path, _ = req.split(" ", 2)
    resp = DEFAULT
    if method == "GET":
        path, params = get_param(path)
        doc = web.handle(path, params)
        resp = resp.format(STATUS_OK, "", doc)
    # print(resp)
    return resp.encode('utf-8')
