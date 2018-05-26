import live_chat
import live_tool
import utils as ut
import json
import numpy as np
import time


def join(msg, cookie):
   shortid = msg["roomid"]
   roomid = msg["real_roomid"]
   tv_id = msg["tv_id"]
   url = f"https://api.live.bilibili.com/gift/v2/smalltv/join?roomid={roomid}&raffleId={tv_id}"
   return ut.GET(
       url,
       headers={
           "Cookie":
           cookie,
           "Origin":
           "https://live.bilibili.com",
           "Referer":
           f"https://live.bilibili.com/{shortid}",
           "User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36 Vivaldi/1.96.1147.36",
       })


def main(args):
   room = live_tool.Live(184298).get_chat_room()
   while True:
      msg = room.next()["content"]
      try:
         msg = json.loads(msg)
         if msg["cmd"] == "SYS_MSG" and msg["rep"] == 1 and msg["styleType"] == 2:
            print("small tv?")
            print(msg)
            if np.random.rand(1)[0] > 0.1:
               t = np.random.rand() * 5 + abs(np.random.normal(loc=20, scale=5))
               print(f"sleep for {t}")
               time.sleep(t)
               print(join(msg, args["cookie"]).read())
      except Exception as e:
         print(e)

def argsParse(argv, defValue=None)
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
