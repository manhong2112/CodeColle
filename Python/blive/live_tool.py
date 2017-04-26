import urllib.request as request
import json
import re

from bs4 import BeautifulSoup

LIVE_HOST = "http://live.bilibili.com"
PLAYURL_API = f"{LIVE_HOST}/api/playurl"
GETINFO_API = f"{LIVE_HOST}/live/getInfo"
LIVE_STATUS = {
    "PREPARING": 0,
    "ROUND": 1,
    "LIVE": 2
}




class Live():
    def __init__(self, live_id):
        self.ROOM_URL = live_id
        tmp = get_html(f"{LIVE_HOST}/{live_id}")
        tmp = str(BeautifulSoup(tmp, "html.parser").findAll("script")[2])
        tmp = re.search(r"var ROOMID = (\d+)", tmp)

        self.ROOM_ID = tmp.group(1)

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

def get_roomid(live_id):
    return Live(live_id).ROOM_ID

def get_live_status(live_id):
    return Live(live_id).get_live_status()
