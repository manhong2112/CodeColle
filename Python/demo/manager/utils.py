
def deleteFolder(path) :
   import pathlib
   pth = pathlib.Path(path)
   for sub in pth.iterdir() :
      if sub.is_dir() :
         deleteFolder(sub)
      else :
         sub.unlink()
   pth.rmdir()

def hashFile(file):
   bs = 1024*1024*4
   sha = hashlib.sha256()
   sha.update(file.read())
   buffer = file.read(bs)
   while len(buffer) > 0:
      sha.update(buffer)
      buffer = file.read(bs)
   return sha

def parseArgs(args):
   cmd = [""]
   quote = False
   escapeChar = False
   for i in args:
      if escapeChar:
         escapeChar = False
         cmd[-1] += i
      elif i == "\"":
         quote = not quote
      elif quote:
         if i == "\\":
            escapeChar = True
         else:
            cmd[-1] += i
      elif i == " ":
         if cmd[-1] != "":
            cmd.append("")
      else:
         cmd[-1] += i
   return cmd

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def path2tuple(path):
   import os
   import os.path
   return tuple(os.path.normpath(path).split(os.sep))

def readFile(dao, path):
   with dao.open(path) as f:
      return f.read()

import yajl as json
def readJson(dao, path):
   with dao.open(path) as f:
      # print(path)
      return json.loads(f.read())

def readAllFile(dao, pathList):
   import multiprocessing
   pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
   return pool.starmap(readFile, [(dao, i) for i in pathList])

def readAllJson(dao, pathList):
   import multiprocessing
   pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
   return pool.starmap(readJson, [(dao, i) for i in pathList])

