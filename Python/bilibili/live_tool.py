import urllib.request as request
from urllib.parse import urlencode
import json
import re

from bs4 import BeautifulSoup

LIVE_HOST = "http://live.bilibili.com"
API_HOST = "https://api.live.bilibili.com"
USERINFO_API = "http://space.bilibili.com/ajax/member/GetInfo"
PLAYURL_API = f"{LIVE_HOST}/api/playurl"
GETINFO_API = f"{API_HOST}/room/v1/Room/get_info"
ROOMINIT_API = f"{API_HOST}/room/v1/Room/room_init"
LIVE_STATUS = {
    "PREPARING": 0,
    "ROUND": 1,
    "LIVE": 2
}

def get_roomid(shortid):
    url = f"{ROOMINIT_API}?id={shortid}"
    data = get_json(url)
    return data["data"]["room_id"]

def get_userinfo(uid):
    return json.loads(post(USERINFO_API, {"mid": uid}, {"referer":USERINFO_API}))

def get_roominfo(roomid):
    return get_json(f"{GETINFO_API}?room_id={roomid}")

def post(url, data={}, headers={}):
    return request.urlopen(request.Request(url, urlencode(data).encode(), headers=headers)).read().decode()

class Live():
    def __init__(self, live_id):
        self.LIVE_ID = live_id
        self.ROOM_ID = get_roomid(self.LIVE_ID)

        self.raw = get_roominfo(self.ROOM_ID)
        self.userinfo = get_userinfo(self.raw["data"]["uid"])

    def get_live_status(self):
        self.raw = get_roominfo(self.ROOM_ID)
        tmp = self.raw["data"]["live_status"]
        return LIVE_STATUS[tmp], tmp

    def get_url(self):
        self.PLAYURL_URL = f"{PLAYURL_API}?cid={self.ROOM_ID}&quality=4"
        raw = get_html(self.PLAYURL_URL)
        tmp = str(BeautifulSoup(self.raw, "html.parser").findAll("durl")[0])
        return re.findall(r"\[CDATA\[(.*)\]\]", tmp)

    def get_name(self):
        return self.userinfo["data"]["name"]

    def get_title(self):
        self.raw = get_json(self.GETINFO_URL)
        return self.raw["data"]["ROOMTITLE"]

    def get_recently_rawdata(self):
        return self.raw

def get_html(url):
    return request.urlopen(url).read().decode("utf-8")

def get_json(url):
    return json.loads(request.urlopen(url).read())

def get_url(live_id):
    return Live(live_id).get_url()

def get_live_status(live_id):
    return Live(live_id).get_live_status()
