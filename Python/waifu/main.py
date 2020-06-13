from mirai import Mirai, Plain, MessageChain, Friend, Group, Member, At, Plain, Source, Image
from mirai.utilles.dependencies import AssertAt
import asyncio

qq = 1471609662
authKey = 'ngkjsdntiosengoiwejetk3w90jtg'
mirai_api_http_locate = 'localhost:3103/ws'

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")


def main():
   app.run()


@app.receiver("FriendMessage")
async def event_fm(app: Mirai, friend: Friend, message: MessageChain):
   print(message.toString())
   if message.toString() == "/followed":
      await app.sendFriendMessage(friend, [Image.fromFileSystem("D:\\palette\\Sync\\Devices\\81519056_p0.jpg")])
      # import pixiv
      # pixiv.main(dest="./pixiv/")
      # await app.sendFriendMessage(friend, [Plain(text=message.toString())])

if __name__ == "__main__":
   main()
