import socket
import json
import base64


def send(url, data):
   # assume data is bytearray
   content = f"""POST /{url} HTTP/1.1
user-agent: LBR/ASMR
Host: 119.29.97.152:19100
Content-Length: {len(data)}\n\n""".encode() + data
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.connect(("119.29.97.152", 19100))
   sock.send(content)
   buff = sock.recv(1024)
   response = buff
   while buff:
      buff = sock.recv(1024)
      response += buff
   sock.close()
   return response.split(b"\r\n\r\n", 1)


def GetMediaList(num=19, offset=0, order=0, asmrtype=0):
   data = {
       "RequestCode": "GetMediaList",
       "num": num,
       "offset": offset,
       "order": order,
       "asmrtype": str(asmrtype)
   }
   res = send("GetMediaList", base64.b64encode(json.dumps(data).encode()))
   return json.loads(base64.b64decode(res[1][7:-7]))
