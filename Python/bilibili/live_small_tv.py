import live_chat
import live_tool
import utils as ut
import json
import numpy as np
import time

def get_small_tv_list(roomid):
   url = f"https://api.live.bilibili.com/gift/v3/smalltv/check?roomid={roomid}"
   return ut.GET_json(url)["data"]["list"]

def join(roomid, tv_id, cookie):
   return ut.POST(
       "https://api.live.bilibili.com/gift/v3/smalltv/join",
       data={
          "roomid": roomid,
          "raffleId": tv_id,
          "type": "Gift",
          "csrf_token": "e85b0f4d99828f1498d5d03a379582af",
          "visit_id": ""
       },
       headers={
           "Cookie":
           cookie,
           "Origin":
           "https://live.bilibili.com",
           "Referer":
           f"https://live.bilibili.com/{roomid}",
           "User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36 Vivaldi/1.96.1147.36",
       })

def process(msg, cookie):
   roomid = msg["real_roomid"]
   tv_list = get_small_tv_list(roomid)
   return [join(roomid, i["raffleId"], cookie).read().decode() for i in tv_list]


def main(args):
   print(args["cookie"])
   room = live_tool.Live(184298).get_chat_room()
   while True:
      msg = room.next()["content"]
      try:
         msg = json.loads(msg)
         if msg["cmd"] == "SYS_MSG" and msg["rep"] == 1 and msg["styleType"] == 2:
            print("small tv?")
            print(msg)
            if np.random.rand(1)[0] > 0.1:
               t = np.random.rand() * 5 + abs(np.random.normal(loc=10, scale=5))
               print(f"sleep for {t}")
               time.sleep(t)
               print("\n".join(process(msg, args["cookie"])))
      except Exception as e:
         print(e)

def argsParse(argv, defValue=None):
   args = defValue
   if not args:
      args = {}
   for i in argv:
      x = i.split("=", 1)
      if len(x) == 1:
         args[x[0]] = True
      else:
         args[x[0]] = x[1]
   return args

if __name__ == "__main__":
   import sys
   main(argsParse(sys.argv[1:]))
