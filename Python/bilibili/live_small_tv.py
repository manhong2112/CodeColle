"""Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Content-Length: 93
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36 Vivaldi/1.96.1147.36

{"cmd":"SYS_MSG","msg":"","msg_text":"","rep":1,"styleType":2,"url":"http://live.bilibili.com/8498920","roomid":8498920,"real_roomid":8498920,"rnd":176055739,"tv_id":"49044"}
"""
import live_chat
import live_tool
import utils as ut
import json


def join(msg, cookie):
   shortid = msg["roomid"]
   roomid = msg["real_roomid"]
   tv_id = msg["tv_id"]
   url = f"https://api.live.bilibili.com/gift/v2/smalltv/join?roomid={roomid}&raffleId={tv_id}"
   return ut.GET(
       url,
       headers={
           "Cookie": cookie,
           "Origin": "https://live.bilibili.com",
           "Referer": f"https://live.bilibili.com/{shortid}",
       })


def main():
   room = live_tool.Live(184298).get_chat_room()
   while True:
      msg = room.next()["content"]
      try:
         msg = json.loads(msg)
         if msg["cmd"] == "SYS_MSG" and msg["rep"] == 1 and msg["styleType"] == 2:
            print("small tv?")
            print(
                join(
                    msg,
                    ""
                ).read())
      except Exception as e:
         print(e)


if __name__ == "__main__":
   main()
