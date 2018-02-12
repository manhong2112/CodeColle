from collections import namedtuple
from singleton import Singleton
import os.path
import hashlib
import time
import utils
import fileaccessor

import json

# File :: (String, String, String, Dict<TagName: String, Tag>)
class File(namedtuple("File", ["name", "path", "tags", "dao"])):
   def __init__(self, *args, **vargs):
      self.__hashcode = hash((self.name,) + self.path)

   def __hash__(self):
      return self.__hashcode

   def __eq__(self, obj):
      return type(obj) is File and self.name == obj.name and self.path == obj.path

   def __repr__(self):
      tags = ", ".join(tag.name for tag in sorted(self.tags.values()))
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



def createFileObj(dao, path):
   path = utils.path2tuple(path)
   return File(path[-1], path, dict(), dao)

class DB():
   def __init__(self, dao, path):
      self.dao: fileaccessor.FileAccessor = dao
      self.path = path
      self.last = 0
      self.dao.mkdir(path)

   def save(self, op, args):
      opts = self.last = str(int(time.time()*1000))
      path = os.path.join(self.path, opts)
      print(path)
      print(self.dao.isfile(path))
      if self.dao.isfile(path):
         return self.save(op, args)
      with self.dao.open(path, "w+") as f:
         f.write(json.dumps({"op": op, "args": args}))

   def load(self, tm, start=None):
      start = start if start is not None else self.last
      fileList = [os.path.join(self.path, str(i)) \
                    for i in sorted(int(x) for x in self.dao.listdir(self.path))\
                    if i >= start]
      for obj in utils.readAllJson(self.dao, fileList):
         op, args = obj["op"], obj["args"]
         print(op + ": " + repr(args))
         if op == "createTag":
            tm.createTag(args[0], db=False)
         elif op == "removeTag":
            tm.removeTag(name=args[0], db=False)
         elif op == "addFile":
            p = "/".join(args[1])
            tm.addFile(tm.createTag(args[0]), createFileObj(tm.dao, p), db=False)
         elif op == "removeFile":
            tm.removeFile(path="/".join(args[1]), db=False)
      if fileList: self.last = fileList[-1]

class TagManager(metaclass=Singleton):
   def __init__(self, dao, dbpath=".tagdb"):
      self.dao: fileaccessor.FileAccessor = dao
      self.db = DB(dao, dbpath)
      self.tagmap = dict()
      # self.tagmap :: Dict<Name : String, Tag>
      self.filemap = dict()
      # self.tagmap :: Dict<Path : String, File>

   def load(self, start=0):
      self.db.load(self, start)

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
         file.tags.pop(name, None)
      tag.files.clear()

   def addFile(self, tag, file, db=True):
      assert type(file) is File
      assert type(tag) is Tag
      if tag in file.tags:
         return
      if db: self.db.save("addFile", [tag.name, file.path])
      if file.path not in self.filemap:
         self.filemap[file.path] = file
      self.filemap[file.path].tags[tag.name] = tag
      tag.files.add(self.filemap[file.path])

   def removeFile(self, file=None, path=None, db=True):
      assert file is not None or path is not None
      if file:
         path = file.path
      if db: self.db.save("removeFile", path)
      file = self.filemap.pop(path, None)
      for tag in file.tags:
         tag.files.remove(file)
      tag.files.clear()

   def reset(self):
      self.tagmap = dict()
      # self.tagmap :: Dict<Name : String, Tag>
      self.filemap = dict()
      # self.tagmap :: Dict<Path : String, File>

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
   dao = fileaccessor.Local("./")
   f = createFileObj(dao, "65746707_p0.jpg")
   tm: TagManager = TagManager()
   tm.addFile(tm.createTag("Picture"), f)
   tm.addFile(tm.createTag("Anime"), f)
   tm.removeTag(name="Anime")
   listAll(tm)

def test2():
   tm: TagManager = TagManager()
   DB().load(tm)
   listAll(tm)

if __name__ == "__main__":
   test1()
   TagManager().reset()
   test2()
   utils.deleteFolder(".tagdb")