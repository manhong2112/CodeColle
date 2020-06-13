import requests
import re
import html
from pipe_fn import e
import json
import os.path
import bs4

img_url = "https://i.pximg.net/img-original/img/{date}/{pid}_p{page}.{ext}"
artworks_url = "https://www.pixiv.net/artworks/{pid}"


def get_info(illust_id):
    url = artworks_url.format(pid=illust_id)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content)
    content = json.loads(soup.find("meta", id="meta-preload-data")["content"])
    return {
        "id": content["illust"][illust_id]["id"],
        "title": content["illust"][illust_id]["title"],
        "description": content["illust"][illust_id]["description"],
        "illustType": content["illust"][illust_id]["illustType"],
        "xRestrict": content["illust"][illust_id]["xRestrict"],
        "tags": content["illust"][illust_id]["tags"]["tags"]
        | e / map @ (lambda t: t["tag"])
        | e / list,
        "pageCount": content["illust"][illust_id]["pageCount"],
        "bookmarkCount": content["illust"][illust_id]["bookmarkCount"],
        "likeCount": content["illust"][illust_id]["likeCount"],
        "viewCount": content["illust"][illust_id]["viewCount"],
    }


def dict2cookie(cookie):
    return (
        list(cookie.items())
        | e / map @ (lambda x: str(x[0]) + "=" + str(x[1]))
        | e / ";".join
    )


def get_image_ext(date, pid):
    url = img_url.format(date=date, pid=pid, page=0, ext="jpg")
    x = requests.head(url, headers={"referer": url})
    if x.status_code == 200:
        return "jpg"
    else:
        # normally there are only two formats
        return "png"


def get_newest_followed_illusts(cookie, page_id):
    def extract_date(illust):
        url = illust["url"]
        date = re.compile(
            r"img-master/img/(\d{4}/\d{2}/\d{2}/\d{2}/\d{2}/\d{2})/"
        ).findall(url)[0]
        return date

    patt = re.compile(
        '<div id="js-mount-point-latest-following"data-items="(.*)"style="min-height: 1460px;"></div>'
    )
    url = f"https://www.pixiv.net/bookmark_new_illust.php?p={page_id}"
    response = requests.get(
        url, params={"p": page_id}, headers={"cookie": dict2cookie(cookie)}
    )
    result = patt.findall(response.content.decode())
    return (
        result[0]
        | e / html.unescape
        | e / json.loads
        | e / filter @ (lambda x: x["illustType"] != "2")  # ignore animate
        | e / map @ (lambda x: (x["illustId"], extract_date(x), x["pageCount"]))
        | e / map @ (lambda x: (x[0], x[1], x[2], get_image_ext(x[1], x[0])))
        | e / list
    )


def download_newest_followed_illusts(cookie, latest_pid, dest):
    lst = []
    k = 1
    p = get_newest_followed_illusts(cookie, k)
    ret = p | e / map @ (lambda x: int(x[0])) | e / max
    p = p | e / filter @ (lambda x: int(x[0]) > latest_pid) | e / list
    while p:
        download_list(p, dest)
        k += 1
        p = (
            get_newest_followed_illusts(cookie, k)
            | e / filter @ (lambda x: int(x[0]) > latest_pid)
            | e / list
        )
    return (ret, lst)


def download_list(lst, dest, filtering=lambda x: True):
    for illust in lst:
        if not filtering(illust):
            continue
        # illust :: (pid, date, page count, ext)
        for page in range(0, int(illust[2])):
            name = "{}_p{}.{}".format(illust[0], page, illust[3])
            with open(os.path.join(dest, name), "wb") as f:
                url = img_url.format(
                    pid=illust[0], date=illust[1], ext=illust[3], page=page
                )
                print("Downloading {}".format(url))
                response = requests.get(url, headers={"referer": url})
                print("Response: {}".format(response.status_code))
                if response.status_code != 200:
                    continue
                f.write(response.content)
    return True


def main(
    cookie={
        "device_token": "",
        "PHPSESSID": "",
    },
    latest_pid="81515705",
    dest="D:\\palette\\Sync\\Devices",
):
    if os.path.isfile("prop/latest_pid"):
        with open("prop/latest_pid", "r") as f:
            latest_pid = f.readline()
    latest_pid, _ = download_newest_followed_illusts(
        cookie, int(latest_pid), "D:\\palette\\Sync\\Devices"
    )
    with open("prop/latest_pid", "w") as f:
        f.write(str(latest_pid))


if __name__ == "__main__":
    main()
