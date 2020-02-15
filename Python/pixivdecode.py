import re
import sys
import pathlib
import json
import math
from collections import namedtuple

from urllib.error import HTTPError


from webutils import GET, GET_json, POST, POST_json

IllustInfo = namedtuple("IllustInfo", ["pid", "author", "title", "tag", "date", "pics"])
EachPicture = namedtuple("EachPicture", ["img", "ext", "url"])
MemberInfo = namedtuple(
    "MemberInfo", ["mid", "name", "pageNum", "illustNum", "illustList"]
)


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
    return table[a] if a in table else args


def getImg(url):
    return GET(url, headers={"referer": url}).read()


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
        m = re.sub(
            r'.*(?:class="img-container"><a.*?><img src="(.*?)"|class="sensored"><img src="(.*?)").*',
            r"\1",
            page,
        )
        return re.sub(r"(?s).*/img/(.*)/" + pid + ".*", r"\1", m)

    host = "https://www.pixiv.net"
    url = f"{host}/member_illust.php?mode=medium&illust_id={pid}"
    res = GET(url).read().decode("utf-8")
    date = parseDate(pid, res)
    title = parseTitle(res)
    tag = parseTag(res)
    author = parseAuthor(res)
    return IllustInfo(pid, author, title, tag, date, [])


def download_illust_id(illust_id):
    info = parse_illust_id(illust_id)
    ext = "png"
    page = 0
    while True:
        try:
            url = getImgUrl(info.date, illust_id, page, ext)
            info.pics.append(EachPicture(getImg(url), ext, url))
            page += 1
        except HTTPError as e:
            if ext == "jpg":
                break
            else:
                ext = "jpg"
                continue

    return info


def login(account, password):
    def get_post_key(page):
        return re.findall(r'"pixivAccount.postKey":"(.*?)"', page)[0]

    def get_PHPSESSID(res):
        return re.findall(r"PHPSESSID=(.*?);", res.getheader("Set-Cookie"))[0]

    def get_device_token(res):
        return re.findall(r"device_token=(.*?);", res.getheader("Set-Cookie"))[0]

    res = GET("https://accounts.pixiv.net/login")
    post_key = get_post_key(res.read().decode("utf-8"))
    PHPSESSID = get_PHPSESSID(res)
    url = "https://accounts.pixiv.net/api/login?lang=zh_tw"
    res = POST(
        url,
        headers={"Cookie": f"PHPSESSID={PHPSESSID}"},
        data={"password": password, "pixiv_id": account, "post_key": post_key,},
    )
    return {"device_token": get_device_token(res), "PHPSESSID": get_PHPSESSID(res)}


def parse_member_id(mid, cookie):
    def getMemberInfo(mid, content):
        picNum = int(re.findall(r'<span class="count-badge">(.*?)件</span>', content)[0])
        pageNum = math.ceil(picNum / 20)
        memberName = re.findall(r'class="user-name"title="(.*?)">', content)[0]
        return MemberInfo(mid, memberName, pageNum, picNum, [])

    def get_illust_id(content):
        illust_id_list = re.findall(r'data-type="illust"data-id="(\d+)"d', content)
        return illust_id_list

    host = "https://www.pixiv.net"
    url = f"{host}/member_illust.php?id={mid}&type=all&p=1"

    res = GET(url, headers={"Cookie": cookie})

    info = getMemberInfo(mid, res.read().decode("utf-8"))
    for i in range(1, info.pageNum + 1):
        url = f"{host}/member_illust.php?id={mid}&type=all&p={i}"
        info.illustList.extend(
            get_illust_id(GET(url, headers={"Cookie": cookie}).read().decode("utf-8"))
        )
    return info


def download_member_id(member_id, cookie):
    info = parse_member_id(member_id, cookie)
    pics = []
    for i, illust_id in enumerate(info.illustList):
        info.illustList[i] = download_illust_id(illust_id)
    return info


def args_illust_id(args):
    dist = args["dist"] if "dist" in args else ""
    pathlib.Path(dist).mkdir(parents=True, exist_ok=True)
    for illust_id in args["illust_id"].split(" "):
        info = download_illust_id(illust_id)
        pics = info.pics
        with open(f"{dist}/info.txt", "a+", encoding="utf-8") as f:
            f.write(
                repr((info.pid, info.author, info.title, info.tag, info.date)) + "\n"
            )

        for page, eachPicture in enumerate(pics, 0):
            img = eachPicture.img
            ext = eachPicture.ext
            url = eachPicture.url
            _dist = f"{dist}/{illust_id}_p{page}.{ext}"
            with open(_dist, "wb") as f:
                f.write(img)
                print(f"{url} -> {_dist}")


def args_member_id(args):
    dist = args["dist"] if "dist" in args else None
    cookie = args["cookie"]
    cookie = f"device_token={cookie['device_token']}; PHPSESSID={cookie['PHPSESSID']}"
    for mid in args["member_id"].split(" "):
        mem_info: MemberInfo = download_member_id(mid, cookie)
        mem_dist = (dist + "/" + mid) if dist else mid
        pathlib.Path(mem_dist).mkdir(parents=True, exist_ok=True)

        illustList: [IllustInfo] = mem_info.illustList

        with open(f"{mem_dist}/info.txt", "a+", encoding="utf-8") as f:
            f.write(repr((mem_info.mid, mem_info.name, mem_info.illustNum)) + "\n")

        for illustInfo in illustList:
            illustId = illustInfo.pid
            pics = illustInfo.pics
            with open(f"{mem_dist}/info.txt", "a+", encoding="utf-8") as f:
                f.write(
                    repr(
                        (
                            illustInfo.pid,
                            illustInfo.author,
                            illustInfo.title,
                            illustInfo.tag,
                            illustInfo.date,
                        )
                    )
                    + "\n"
                )

            for page, eachPicture in enumerate(pics):
                url = eachPicture.url
                ext = eachPicture.ext
                pic_dist = f"{mem_dist}/{illustId}_p{page}.{ext}"
                with open(pic_dist, "wb") as f:
                    f.write(eachPicture.img)
                    print(f"{url} -> {pic_dist}")


# python xxx [dist=123] ["illust_id=123 123"] ["member_id=123 123"] ["account=acc" "password=pw"]
if __name__ == "__main__":
    args = argsParse(sys.argv)
    if "help" in args and args["help"]:
        print("python xxx [dist=<path>] [illust_id=<illust_id>]")
        print(
            "python xxx [dist=<path>] [member_id=<member_id> account=<acc> password=<pw>]"
        )
    if "illust_id" in args:
        args_illust_id(args)
    if "member_id" in args:
        assert "account" in args
        assert "password" in args
        args["cookie"] = login(args["account"], args["password"])
        args_member_id(args)
