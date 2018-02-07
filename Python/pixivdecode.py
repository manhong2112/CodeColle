import urllib.request as request
from urllib.error import HTTPError
import re
import sys

GET = lambda url: request.urlopen(url)
# http://www.pixiv.net/img-original/img/<time>/<pid>_p<page>.png

def argsParse(args):
    # xxx=yyy | xxx[=true]
    res = {}
    for i in args:
        i = i.split("=", 1)
        if len(i) == 1:
            res[i[0]] = True
        else:
            res[i[0]] = argsParse0(i[1])
    return res

def argsParse0(args):
    table = {
        "true": True,
        "false": False,
    }
    a = args.lower()
    if a in table:
        return table[a]
    else:
        return args

def getImg(url):
    print(f"GET: {url}")
    req = request.Request(url, headers={'referer': url})
    return request.urlopen(req).read()

def getImgUrl(date, pid, page, ext):
    url = "https://i.pximg.net/img-original/img/{}/{}_p{}.{}"\
        .format(date, pid, page, ext)
    return url

def parse(pid):
    host = "http://www.pixiv.net"
    page = host + "/member_illust.php?mode=medium&illust_id=" + pid
    res = GET(page).read().decode("utf-8")
    date = parseDate(pid, res)
    title = parseTitle(res)
    tag = parseTag(res)
    author = parseAuthor(res)
    ret = {"pid": pid, "author": author, "title": title, "tag": tag, "date": date}
    return ret

def parseTag(page):
    return re.findall(r'<meta name="keywords" content="(.*?)">', page)[0]

def parseTitle(page):
    return re.findall(r'userdata"><h1 class="title">(.*)</h1>', page)[0]

def parseAuthor(page):
    return re.findall(r'<a href="member.php.*>(.*?)</a></h2>', page)[0]

def parseDate(pid, page):
    m = re.sub(r'.*(?:class="img-container"><a.*?><img src="(.*?)"|class="sensored"><img src="(.*?)").*', r'\1', page)
    return re.sub(r"(?s).*/img/(.*)/" + pid + ".*", r'\1', m)

def _main(info):
    ext = "png"
    page = 0
    while True:
        try:
            yield getImg(getImgUrl(info["date"], pid, page, ext)), ext
            page += 1
        except HTTPError as e:
            print(e)
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
    info = parse(pid)
    with open(f"{dist + '/' if dist else ''}/info.txt" , 'a+', encoding="utf-8") as f:
        f.write(repr(info) + "\n")
    for p, ext in _main(info):
        _dist = f"{dist + '/' if dist else ''}{pid}_p{page}.{ext}"
        with open(_dist, 'wb') as f:
            f.write(p)
            print(f"saved to {_dist}")
        page += 1
