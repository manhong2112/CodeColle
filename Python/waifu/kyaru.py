from pixiv import dict2cookie, download_list, get_image_ext, img_url, get_info
from pipe_fn import e
import re
import requests
import html
import json
import os.path


def take(n, lst):
    res = []
    for i in lst:
        res.append(i)
        if len(res) == n:
            return res
    return res


def get_tag_images(cookie, tag, page_id, ordering="date", mode="all", s_mode="s_tag_full"):
    def extract_date(url):
        date = re.compile(
            r"(?:custom-thumb|img-master)/img/(\d{4}/\d{2}/\d{2}/\d{2}/\d{2}/\d{2})/"
        ).findall(url)[0]
        return date

    url = f"https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order={ordering}&p={page_id}&s_mode={s_mode}&mode={mode}&type=all"

    response = requests.get(url, headers={"cookie": dict2cookie(cookie)})
    return (
        response.json()["body"]["illustManga"]["data"]
        | e / map @ (lambda x: (x["illustId"], extract_date(x["url"]), x["pageCount"]))
        | e / map @ (lambda x: (x[0], x[1], x[2], get_image_ext(x[1], x[0])))
        | e / list
    )


def main(
    cookie={
        "device_token": "",
        "PHPSESSID": "",
    },
    dest="D:\\palette\\Sync\\Devices\\chino",
):

    i = 1
    images = get_tag_images(cookie, "チノ", i, ordering="date")
    print(images)
    while images:
        download_list(
            images,
            dest,
            filtering=lambda x: (
                lambda y: y["bookmarkCount"] >= 300
                and (y["bookmarkCount"] >= 1000 if y["xRestrict"] == 1 else True)
            )(get_info(x[0])),
        )
        i += 1
        images = get_tag_images(cookie, "チノ", i, ordering="date")


if __name__ == "__main__":
    main()
