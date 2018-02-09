import urllib.request as request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

def POST(url, headers=dict(), data=dict()):
    request = Request(url, urlencode(data).encode())
    for k in headers:
        request.add_header(k, headers[k])
    return urlopen(request)

def GET(url, headers=dict()):
    request = Request(url)
    for k in headers:
        request.add_header(k, headers[k])
    return urlopen(request)

# http://www.pixiv.net/img-original/img/<time>/<pid>_p<page>.png
def GET_json(url, headers=dict()):
    return json.loads(GET(url, headers).read().decode("unicode-escape").replace('\r\n', ''), strict=False)

def POST_json(url, headers=dict(), data=dict()):
    return json.loads(POST(url, headers, data).read().decode("unicode-escape").replace('\r\n', ''), strict=False)
