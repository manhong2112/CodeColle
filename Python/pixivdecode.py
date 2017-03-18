import urllib.request as request
from urllib.error import HTTPError
import re

GET = lambda url: request.urlopen(url)
# http://www.pixiv.net/img-original/img/<time>/<pid>_p<page>.png


def getImg(date, pid, page, ext):
    url = "http://i1.pixiv.net/img-original/img/{}/{}_p{}.{}"\
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

while True:
    pid = input("pid > ")
    page = 0
    for p in main(pid):
        dist = "{}_p{}.png".format(pid, page)
        with open(dist, 'wb') as f:
            f.write(p)
            print("saved to {}".format(dist))
        page += 1
