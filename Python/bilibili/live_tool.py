import json
import re
import urllib.request as request
from threading import Thread, Timer
from urllib.parse import urlencode

import websocket
from bs4 import BeautifulSoup
import queue
LIVE_HOST = "http://live.bilibili.com"
API_HOST = "http://api.live.bilibili.com"
USERINFO_API = "http://space.bilibili.com/ajax/member/GetInfo"
PLAYURL_API = f"{API_HOST}/api/playurl"
GETINFO_API = f"{API_HOST}/room/v1/Room/get_info"
ROOMINIT_API = f"{API_HOST}/room/v1/Room/room_init"
LIVE_STATUS = {"PREPARING": 0, "LIVE": 1, "ROUND": 2}


def get_roomid(shortid):
   url = f"{ROOMINIT_API}?id={shortid}"
   data = get_json(url)
   return data["data"]["room_id"]


def get_userinfo(uid):
   return json.loads(post(USERINFO_API, {"mid": uid}, {"referer": USERINFO_API}))


def get_roominfo(roomid):
   return get_json(f"{GETINFO_API}?room_id={roomid}")


def post(url, data={}, headers={}):
   return request.urlopen(\
            request.Request(url, urlencode(data).encode(), headers=headers)\
          ).read().decode() # yapf: disable


class Live():
   def __init__(self, live_id):
      self.LIVE_ID = live_id
      self.ROOM_ID = get_roomid(self.LIVE_ID)

      self.raw = get_roominfo(self.ROOM_ID)
      self.userinfo = get_userinfo(self.raw["data"]["uid"])

      self.PLAYURL_URL = f"{PLAYURL_API}?cid={self.ROOM_ID}&quality=4&otype=json&platform=web"

   def get_live_status(self):
      self.raw = get_roominfo(self.ROOM_ID)
      return self.raw["data"]["live_status"]

   def get_url(self):
      tmp = get_json(self.PLAYURL_URL)
      return [i["url"] for i in tmp["durl"]]

   def get_name(self):
      return self.userinfo["data"]["name"]

   def get_title(self):
      self.raw = self.raw = get_roominfo(self.ROOM_ID)
      return self.raw["data"]["title"]

   def get_recently_rawdata(self):
      return self.raw

   class ChatRoom(object):
      def __init__(self, roomid):
         import live_chat as lchat
         self.roomid = roomid
         self.danmakuList = []
         self.newDanmakuQueue = queue.Queue()
         self.conn = websocket.create_connection("ws://broadcastlv.chat.bilibili.com:2244/sub")
         data = lchat.chatEncode(7, (f'{{"uid":0,"roomid":{roomid},"protover":1,"platform":"web","clientver":"1.2.8"}}').encode())
         self.conn.send(data)

         def func():
            while True:
               data = lchat.chatDecode(self.conn.recv_frame().data)
               self.newDanmakuQueue.put(data)

         def keepSocketLife():
            self.conn.send(lchat.chatEncode(2, b'[object Object]'))

         self.danmakuThread = Thread(target=func)
         self.keepSocketLifeThread = Timer(30, keepSocketLife)
         self.danmakuThread.start()
         self.keepSocketLifeThread.start()

      def hasNext(self):
         return not self.newDanmakuQueue.empty()

      def next(self, block=True):
         danmaku = self.newDanmakuQueue.get(block)
         self.danmakuList.append(danmaku)
         return danmaku

      def cleanQueue(self):
         while not self.newDanmakuQueue.empty():
            self.danmakuList.append(self.newDanmakuQueue.get())
         return self.danmakuList

      def __get__(self, index):
         return self.danmakuList[index]

   def get_chat_room(self):
      return Live.ChatRoom(self.ROOM_ID)


def get_html(url):
   return request.urlopen(url).read().decode("utf-8")


def get_json(url):
   return json.loads(request.urlopen(url).read())


def get_url(live_id):
   return Live(live_id).get_url()


def get_live_status(live_id):
   return Live(live_id).get_live_status()
