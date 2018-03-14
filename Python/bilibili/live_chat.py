import base64
import random
import time
from threading import Thread


class Int16(object):
   SIZE = 2

   @staticmethod
   def toUInt8arr(num):
      s = Int16.SIZE
      n = Int16.toUInt16(num)
      assert 0 <= n < (1 << (8 * s))
      limit = 255
      parts = [0] * s
      for i in range(0, s)[::-1]:
         parts[i] = n & limit
         n >>= 8
      return parts

   @staticmethod
   def fromUInt8arr(arr):
      return Int16.fromUint16(sum(v << (8 * (1 - i)) for i, v in enumerate(arr[:Int16.SIZE], 0)))

   @staticmethod
   def toUInt16(num):
      import struct
      return struct.unpack_from("H", struct.pack("h", num))[0]

   @staticmethod
   def fromUint16(num):
      import struct
      return struct.unpack_from("h", struct.pack("H", num))[0]


class Int32(object):
   SIZE = 4

   @staticmethod
   def toUInt8arr(num):
      s = Int32.SIZE
      n = Int32.toUInt32(num)
      assert 0 <= n < (1 << (8 * s))
      limit = 255
      parts = [0] * s
      for i in range(0, s)[::-1]:
         parts[i] = n & limit
         n >>= 8
      return parts

   @staticmethod
   def fromUInt8arr(arr):
      s = Int32.SIZE
      return Int32.fromUint32(sum(v << (s * (3 - i)) for i, v in enumerate(arr[:s], 0)))

   @staticmethod
   def toUInt32(num):
      import struct
      return struct.unpack_from("I", struct.pack("i", num))[0]

   @staticmethod
   def fromUint32(num):
      import struct
      return struct.unpack_from("i", struct.pack("I", num))[0]


HeaderLen = 16


def chatEncode(op, content, ver=1, seq=1):
   # Assure content is bytearray or list
   # [0, 0, 0, 0] + [0, 0]    + [0, 0] + [0, 0, 0, 0] + [0, 0, 0, 0]
   # contentLen   + headerLen + ver    + op           + seq
   headerLen = 16
   ver = 1
   seq = 1
   return arrayPadTo(4, Int32.toUInt8arr(len(content) + headerLen)) + \
          arrayPadTo(2, Int16.toUInt8arr(HeaderLen)) + \
          arrayPadTo(2, Int16.toUInt8arr(ver)) + \
          arrayPadTo(4, Int32.toUInt8arr(op)) + \
          arrayPadTo(4, Int32.toUInt8arr(seq)) + \
          list(content)


def chatDecode(bytearr):
   # [0, 0, 0, 0] + [0, 0]    + [0, 0] + [0, 0, 0, 0] + [0, 0, 0, 0]
   # contentLen   + headerLen + ver    + op           + seq
   return {
       "contentLen": Int32.fromUInt8arr(bytearr[:4]),
       "headerLen": Int16.fromUInt8arr(bytearr[4:6]),
       "ver": Int16.fromUInt8arr(bytearr[6:8]),
       "op": Int32.fromUInt8arr(bytearr[8:12]),
       "seq": Int32.fromUInt8arr(bytearr[12:16]),
       "content": bytearr[16:],
   }


def arrayPadTo(length, arr):
   assert length >= len(arr)
   return ([0] * (length - len(arr))) + arr


def keepSocketLife(socket):
   while True:
      time.sleep(30)
      socket.send(chatEncode(2, b'[object Object]'))  # ??? i don't know why, maybe it just a bug?


def main(roomid):
   import websocket
   conn = websocket.create_connection("ws://broadcastlv.chat.bilibili.com:2244/sub")
   data = chatEncode(7, (f'{{"uid":0,"roomid":{roomid},"protover":1,"platform":"web","clientver":"1.2.8"}}').encode())  # yapf: disable
   conn.send(data)
   thread = Thread(target=keepSocketLife, args=(conn, ))
   thread.start()
   while True:
      data = chatDecode(conn.recv_frame().data)
      print(data)
      print(data["content"].decode("unicode-escape"))


if __name__ == "__main__":
   main(49728)
