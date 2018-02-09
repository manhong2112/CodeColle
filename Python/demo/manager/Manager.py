from collections import namedtuple
from singleton import Singleton
import os
import os.path
import hashlib
import pathlib
import time
import json

from utils import delete_folder
# File :: (String, String, String, Set<Tag>)
class File(namedtuple("File", ["name", "path", "hash", "tags"])):
   def __init__(self, *args, **vargs):
      self.__hashcode = int(self.hash[:16], 16)
   
   def __hash__(self):
      return self.__hashcode
   
   def __eq__(self, obj):
      return type(obj) is File and self.hash == obj.hash and self.name == obj.name and self.path == obj.path
   
   def __repr__(self):
      tags = ", ".join(tag.name for tag in sorted(self.tags))
      return f"File(name='{self.name}', path='{self.path}', tags='{tags}')"

class Tag(namedtuple("Tag", ["name", "files"])):
   def __init__(self, *args, **vargs):
      super().__init__()
      self.__hashcode = hash(self.name)

   def __hash__(self):
      return self.__hashcode
   
   def __eq__(self, obj):
      return type(obj) is Tag and self.name == obj.name
   
   def __repr__(self):
      files = ", ".join(tag.name for tag in sorted(self.files))
      return f"Tag(name='{self.name}', files='{files}')"

def hashFile(file):
   bs = 1024*1024*4
   sha = hashlib.sha256()
   sha.update(file.read())
   buffer = file.read(bs)
   while len(buffer) > 0:
      sha.update(buffer)
      buffer = file.read(bs)
   return sha

def createFileObj(path):
   assert os.path.isfile(path)
   name = os.path.basename(path)
   with open(path, mode="rb") as f:
      sha = hashFile(f)
      path = tuple(os.path.normpath(path).split(os.sep))
      return File(name, path, sha.hexdigest(), set())
   pass

class DB(metaclass=Singleton):
   def __init__(self, path="./managerdb"):
      self.path = path
      pathlib.Path(path).mkdir(parents=True, exist_ok=True) 

   def save(self, op, args):
      opts = str(int(time.time()*1000))
      path = os.path.join(self.path, opts)
      if os.path.isfile(path):
         return self.save(op, args)
      with open(path, "w+") as f:
         json.dump({"op": op, "args": args}, f)

   def load(self, tm, start=0):
      for name in (i for i in sorted(int(x) for x in os.listdir(self.path)) if i >= start):
         p = os.path.join(self.path, str(name))
         with open(p, "r") as f:
            obj = json.load(f)
            op = obj["op"]
            args = obj["args"]
         print(op + ": " + repr(args))
         if op == "createTag":
            tm.createTag(args[0], db=False)
         elif op == "removeTag":
            tm.removeTag(name=args[0], db=False)
         elif op == "addFile":
            tm.addFile(tm.createTag(args[0]), createFileObj("/".join(args[1])), db=False)
         elif op == "removeFile":
            tm.removeFile(path="/".join(args[1]), db=False)

class Manager(metaclass=Singleton):
   def __init__(self, db=DB()):
      self.db = db
      self.tagmap = dict()
      # self.tagmap :: Dict<Name : String, Tag>
      self.filemap = dict()
      # self.tagmap :: Dict<Path : String, File>

   def createTag(self, name, db=True):
      assert type(name) is str
      if name in self.tagmap:
         return self.tagmap[name]
      if db: self.db.save("createTag", [name])
      t = Tag(name, set())
      self.tagmap[name] = t
      return t
   
   def removeTag(self, name=None, tag=None, db=True):
      assert name is not None or tag is not None
      if tag:
         name = tag.name
      if db: self.db.save("removeTag", [name])
      tag = self.tagmap.pop(name, None)
      for file in tag.files:
         file.tags.remove(tag)
      tag.files.clear

   def addFile(self, tag, file, db=True):
      assert type(file) is File
      assert type(tag) is Tag
      if db: self.db.save("addFile", [tag.name, file.path])
      if file.path not in self.filemap:
         self.filemap[file.path] = file
      file.tags.add(tag)
      tag.files.add(file)
   
   def removeFile(self, file=None, path=None, db=True):
      assert file is not None or path is not None
      if file:
         path = file.path
      if db: self.db.save("removeFile", path)
      file = self.filemap.pop(path, None)
      for tag in file.tags:
         tag.files.remove(file)
      tag.files.clear()
   

def listAll(tm):
   print("="*20)
   print("Tags: ")
   for i in tm.tagmap.values():
      print(repr(i))
   print("Files: ")
   for i in tm.filemap.values():
      print(repr(i))
   print("="*20)

def test1():
   f = createFileObj("65746707_p0.jpg")
   tm: Manager = Manager()
   tm.addFile(tm.createTag("Picture"), f)
   tm.addFile(tm.createTag("Anime"), f)
   listAll(tm)
   tm.removeTag(name="Anime")
   listAll(tm)

def test2():
   tm: Manager = Manager()
   DB().load(tm)
   listAll(tm)

if __name__ == "__main__":
   test1()
   test2()
   delete_folder("managerdb")