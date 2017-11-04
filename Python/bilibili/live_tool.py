import urllib.request as request
import json
import re

from bs4 import BeautifulSoup

LIVE_HOST = "http://live.bilibili.com"
APT_HOST = "https://api.live.bilibili.com"
PLAYURL_API = f"{LIVE_HOST}/api/playurl"
GETINFO_API = f"{LIVE_HOST}/live/getInfo"
ROOMINIT_API = f"{APT_HOST}/room/v1/Room/room_init"
LIVE_STATUS = {
    "PREPARING": 0,
    "ROUND": 1,
    "LIVE": 2
}

def get_roomid(shortid):
    url = f"{ROOMINIT_API}?id={shortid}"
    data = get_json(url)
    return data["data"]["room_id"]

class Live():
    def __init__(self, live_id):
        self.LIVE_ID = live_id
        self.ROOM_ID = get_roomid(self.LIVE_ID)

        self.GETINFO_URL = f"{GETINFO_API}?roomid={self.ROOM_ID}"
        self.PLAYURL_URL = f"{PLAYURL_API}?cid={self.ROOM_ID}&quality=4"

        self.raw = get_json(self.GETINFO_URL)
        self.NICK_NAME = self.raw["data"]["ANCHOR_NICK_NAME"]

    def get_live_status(self):
        self.raw = get_json(self.GETINFO_URL)
        tmp = self.raw["data"]["LIVE_STATUS"]
        return LIVE_STATUS[tmp], tmp

    def get_url(self):
        self.raw = get_html(self.PLAYURL_URL)
        tmp = str(BeautifulSoup(self.raw, "html.parser").findAll("durl")[0])
        return re.findall(r"\[CDATA\[(.*)\]\]", tmp)

    def get_name(self):
        return self.NICK_NAME

    def get_title(self):
        self.raw = get_json(self.GETINFO_URL)
        return self.raw["data"]["ROOMTITLE"]
    
    def get_recently_rawdata(self):
        return self.raw

def get_html(url):
    return request.urlopen(url).read().decode("utf-8")

def get_json(url):
    return json.loads(request.urlopen(url).read().decode("unicode-escape").replace('\r\n', ''))

def get_url(live_id):
    return Live(live_id).get_url()

def get_live_status(live_id):
    return Live(live_id).get_live_status()
