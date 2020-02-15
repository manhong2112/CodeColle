import socket
import select
import sys

host = "127.0.0.1"
port = 8080

def send(*data):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((host,port))
   s.send(("\n".join(data) + "\n\n\n").encode())
   ready = select.select([s], [], [], 10)
   response = b""
   while True:
      if ready[0]:
         response = s.recv(1024)
      if not response:
         break
      print(response.decode(), end="")
   s.close ()

# scala
# send("#cp", "C:\\scala\\lib\\scala-compiler.jar")
# send("#cp", "C:\\scala\\lib\\scala-library.jar")
# send("#run",
#    "#name", "scala.tools.nsc.MainGenericRunner",
#    "#args", "-Jclient", "-cp", "C:\\scala\\lib\\scala-library.jar;"+sys.argv[1],
#    *sys.argv[2:]
#    )

# dotty
send("#run",
   "#cp", sys.argv[1],
   "C:\\DOTTY-~1.0-R\\lib\\scala-library-2.13.1.jar",
   "C:\\DOTTY-~1.0-R\\lib\\dotty-library_0.22-0.22.0-RC1.jar",
   "#name", sys.argv[2],
   "#args", *sys.argv[3:]
)
