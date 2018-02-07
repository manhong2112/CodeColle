import urllib.request as request
import re
import sys
import pathlib
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import math

from urllib.error import HTTPError

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
    req = request.Request(url, headers={'referer': url})
    return request.urlopen(req).read()

def getImgUrl(date, pid, page, ext):
    url = f"https://i.pximg.net/img-original/img/{date}/{pid}_p{page}.{ext}"
    return url

def parse_illust_id(pid):
    def parseTag(page):
        return re.findall(r'<meta name="keywords" content="(.*?)">', page)[0]
    def parseTitle(page):
        return re.findall(r'userdata"><h1 class="title">(.*)</h1>', page)[0]
    def parseAuthor(page):
        return re.findall(r'<a href="member.php.*>(.*?)</a></h2>', page)[0]
    def parseDate(pid, page):
        m = re.sub(r'.*(?:class="img-container"><a.*?><img src="(.*?)"|class="sensored"><img src="(.*?)").*', r'\1', page)
        return re.sub(r"(?s).*/img/(.*)/" + pid + ".*", r'\1', m)

    host = "https://www.pixiv.net"
    url = host + "/member_illust.php?mode=medium&illust_id=" + pid
    res = GET(url).read().decode("utf-8")
    date = parseDate(pid, res)
    title = parseTitle(res)
    tag = parseTag(res)
    author = parseAuthor(res)
    ret = {"pid": pid, "author": author, "title": title, "tag": tag, "date": date}
    return ret

def download_illust_id(illust_id):
    info = parse_illust_id(illust_id)
    ext = "png"
    page = 0
    pics = []
    urls = []
    while True:
        try:
            url = getImgUrl(info["date"], illust_id, page, ext)
            pics.append((getImg(url), ext))
            urls.append(url)
            page += 1
        except HTTPError as e:
            if ext == "jpg":
                break
            else:
                ext = "jpg"
                continue
    return {"info": info, "pics": pics, "urls": urls}

def login(account, password):
    def get_post_key(page):
        return re.findall(r'"pixivAccount.postKey":"(.*?)"', page)[0]
    def get_PHPSESSID(res):
        return re.findall(r'PHPSESSID=(.*?);', res.getheader("Set-Cookie"))[0]
    def get_device_token(res):
        return re.findall(r'device_token=(.*?);', res.getheader("Set-Cookie"))[0]
    res = GET("https://accounts.pixiv.net/login")
    post_key = get_post_key(res.read().decode("utf-8"))
    PHPSESSID = get_PHPSESSID(res)
    url = "https://accounts.pixiv.net/api/login?lang=zh_tw"
    res = POST(url, headers={
        "Cookie": f"PHPSESSID={PHPSESSID}"
    },\
    data={
        "password": password,
        "pixiv_id": account,
        "post_key": post_key,
    })
    return {"device_token": get_device_token(res), "PHPSESSID": get_PHPSESSID(res)}

def parse_member_id(member_id, cookie):
    def getMemberInfo(content):
        picNum = int(re.findall(r'<span class="count-badge">(.*?)件</span>', content)[0])
        pageNum = math.ceil(picNum / 20)
        memberName = re.findall(r'class="user-name"title="(.*?)">', content)[0]
        return {"pageNum": pageNum, "memberName": memberName, "picNum": picNum}
    def get_illust_id(content):
        illust_id_list = re.findall(r'data-type="illust"data-id="(\d+)"d', content)
        return illust_id_list
    host = "https://www.pixiv.net"
    url = f"{host}/member_illust.php?id={member_id}&type=all&p=1"
    res = GET(url, headers={"Cookie": cookie})
    info = getMemberInfo(res.read().decode("utf-8"))
    info["member_id"] = member_id
    info["picList"] = []
    for i in range(1, info["pageNum"]+1):
        url = f"{host}/member_illust.php?id={member_id}&type=all&p={i}"
        info["picList"].extend(get_illust_id(GET(url, headers={"Cookie": cookie}).read().decode("utf-8")))
    return info

def download_member_id(member_id, cookie):
    info = parse_member_id(member_id, cookie)
    pics = []
    for illust_id in info["picList"]:
        pics.append(download_illust_id(illust_id))
    return {"info": info, "pics": pics}

def args_illust_id(args):
    dist = args["dist"] if "dist" in args else ""
    pathlib.Path(dist).mkdir(parents=True, exist_ok=True) 
    for illust_id in args["illust_id"].split(" "):
        tmp = download_illust_id(illust_id)
        info = tmp["info"]
        pics = tmp["pics"]
        with open(f"{dist}/info.txt" , 'a+', encoding="utf-8") as f:
            f.write(repr(info) + "\n")

        page = 0
        for p, ext in pics:
            _dist = f"{dist}/{illust_id}_p{page}.{ext}"
            with open(_dist, 'wb') as f:
                f.write(p)
                print(f"Saved to {_dist}")
            page += 1

def args_member_id(args):
    dist = args["dist"] if "dist" in args else None
    cookie = args["cookie"]
    cookie = f"device_token={cookie['device_token']}; PHPSESSID={cookie['PHPSESSID']}"
    for mid in args["member_id"].split(" "):
        tmp = download_member_id(mid, cookie)
        mem_dist = (dist + "/" + mid) if dist else mid
        pathlib.Path(mem_dist).mkdir(parents=True, exist_ok=True) 

        mem_info = tmp["info"]
        mem_pics = tmp["pics"]
        
        with open(f"{mem_dist}/info.txt" , 'a+', encoding="utf-8") as f:
            f.write(repr(mem_info) + "\n")

        for pic in mem_pics:
            info = pic["info"]
            pics = pic["pics"]
            urls = pic["urls"]
            illust_id = info['pid']
            with open(f"{mem_dist}/info.txt" , 'a+', encoding="utf-8") as f:
                f.write(repr(info) + "\n")
            page = 0
            for i, (p, ext) in enumerate(pics):
                pic_dist = f"{mem_dist}/{illust_id}_p{page}.{ext}"
                with open(pic_dist, 'wb') as f:
                    f.write(p)
                    print(f"{urls[i]} -> {pic_dist}")
                page += 1
# python xxx [dist=123] ["illust_id=123 123"] ["member_id=123 123"] ["account=acc" "password=pw"]
if __name__ == "__main__":
    args = argsParse(sys.argv)
    if "illust_id" in args:
        args_illust_id(args)
    if "member_id" in args:
        assert "account" in args
        assert "password" in args
        args["cookie"] = login(args["account"], args["password"])
        args_member_id(args)
