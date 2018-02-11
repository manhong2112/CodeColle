import os
import os.path
import pathlib

class FileAccessor():
   def isexist(self, path): raise NotImplementedError
   def isfile(self, path): raise NotImplementedError
   def isdir(self, path): raise NotImplementedError
   def open(self, path, mode="r", encoding="utf8"): raise NotImplementedError
   def listdir(self, path): raise NotImplementedError
   def mkdir(self, path, parent=True): raise NotImplementedError

class Local(FileAccessor):
   def __init__(self, path):
      self.path = os.path.normpath(path)

   def isexist(self, path):
      return os.path.isexist(os.path.join(self.path, path))
      pass

   def isfile(self, path):
      return os.path.isfile(os.path.join(self.path, path))

   def isdir(self, path):
      return ps.path.isdir(os.path.join(self.path, path))

   def open(self, path, mode="r", encoding="utf8"):
      return open(os.path.join(self.path, path), mode=mode, encoding=encoding)

   def mkdir(self, path, parent=True):
      return pathlib.Path(path).mkdir(parents=parent, exist_ok=True)

   def listdir(self, path):
      return os.listdir(os.path.join(self.path, path))

import webdav.client as wc
class WebDavFileObject():
   def __init__(self, client, path, mode="r", encoding="utf8"):
      self.client = client
      self.path = path
      self.buffer = Buffer()

   def read(self):
      self.client.download_to(self.buffer, self.path)
      return self.buffer.read()

   def write(self, content):
      print(self.path)
      self.buffer.write(content)
      self.client.upload_from(self.buffer, "test")

   def __enter__(self):
      return self

   def __exit__(self, type, value, traceback):
      self.buffer = None

class WebDav(FileAccessor):
   def __init__(self, host, root, account, password, otherOptions={}):
      options = {
         "webdav_hostname": host,
         "webdav_login": account,
         "webdav_password": password,
         "webdav_root": root,
         **otherOptions
      }
      self.client = wc.Client(options)

   def isexist(self, path):
      return self.client.check(path)

   def isfile(self, path):
      return self.isexist(path) and not self.isdir(path)
   def isdir(self, path):
      return self.client.is_dir(path)
   def open(self, path, mode="r", encoding="utf8"):
      return WebDavFileObject(self.client, path, mode=mode, encoding=encoding)
   def listdir(self, path):
      return self.client.list(path)
   def mkdir(self, path, parent=True):
      if parent:
         par, child = os.path.split(path)
         if self.isdir(par):
            self.client.mkdir(path)
         else:
            self.mkdir(par)
            self.client.mkdir(path)
      else:
         self.client.mkdir(path)

class Buffer():
   def __init__(self, init=None):
      self.buff = init or b''

   def read(self, *args, **vargs):
      return self.buff

   def write(self, content, *args, **vargs):
      self.buff += content.encode()

   def clean(self):
      self.buff = b''

if __name__ == "__main__":
   dao = WebDav("http://127.0.0.1", "/nextcloud/remote.php/dav/files/manhong2112/manhong", "manhong2112", "f60af455")
   client = dao.client
   f = WebDavFileObject(client, "abc")
   f.write("hello world")