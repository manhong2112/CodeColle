import urllib.request as request
from urllib.error import HTTPError
import re
import sys

GET = lambda url: request.urlopen(url)
# http://www.pixiv.net/img-original/img/<time>/<pid>_p<page>.png

def argsParse(args):
    # xxx=yyy | xxx
    res = {}
    for i in args:
        i = i.split("=", 1)
        if len(i) == 1:
            res[i[0]] = True
        else:
            res[i[0]] = i[1]
    return res



def getImg(date, pid, page, ext):
    url = "https://i.pximg.net/img-original/img/{}/{}_p{}.{}"\
        .format(date, pid, page, ext)
    req = request.Request(url, headers={'referer': url})
    return request.urlopen(req).read()


def parse(pid):
    host = "http://www.pixiv.net"
    img_page = host + "/member_illust.php?mode=medium&illust_id=" + pid
    res = GET(img_page).read().decode("utf-8")
    m = re.sub(r'(?s).*(?:class="img-container"><a.*?><img src="(.*?)"|class="sensored"><img src="(.*?)").*', r'\1', res)
    return re.sub(r"(?s).*/img/(.*)/" + pid + ".*", r'\1', m)


def main(pid):
    date = parse(pid)
    ext = "png"
    page = 0
    while True:
        try:
            yield getImg(date, pid, page, ext)
            page += 1
        except HTTPError:
            if ext == "jpg":
                break
            else:
                ext = "jpg"
                continue

# py xxx dist=123 "pid=123456 123456"
args = argsParse(sys.argv)
assert "pid" in args
if "dist" in args:
    dist = args["dist"]
else:
    dist = None
for pid in args["pid"].split(" "):
    page = 0
    for p in main(pid):
        dist = f"{dist + '/' if dist else ''}{pid}_p{page}.png"
        with open(dist, 'wb') as f:
            f.write(p)
            print(f"saved to {dist}")
        page += 1
