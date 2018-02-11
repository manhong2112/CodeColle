import manager
import utils
import traceback
import sys
import fileaccessor
def main():
   func = {
      "tag": tag,
      "listtag": listtag,
      "filter": filter,
   }
   dao = fileaccessor.WebDav("http://127.0.0.1", "/nextcloud/remote.php/dav/files/manhong2112/manhong", "manhong2112", "f60af455")
   tm = manager.TagManager(dao)
   tm.load(0)
   while True:
      cmd = utils.parseArgs(input("> "))
      if cmd[0] == "exit":
         break
      if cmd[0] not in func:
         print("command not found")
         continue
      try:
         func[cmd[0]](tm, cmd)
      except Exception as e:
         traceback.print_exception(*sys.exc_info())

def tag(tm: manager.TagManager, args):
   # tag <tag> <path>
   tag, path = args[1], args[2]
   tm.addFile(tm.createTag(tag), manager.createFileObj(tm, path))

def listtag(tm: manager.TagManager, args):
   for v in tm.tagmap.values():
      print(v)

def filter(tm: manager.TagManager, args):
   # filter <tag|path|name> <content> [<tag> <content> ...]
   # TODO filterType <regextag|regexpath|regexname>
   result = set()
   filterType, arg = args[1], args[2]
   if filterType ==  "tag":
      result = tm.tagmap[arg].files
   elif filterType == "path":
      arg = utils.path2tuple(arg)
      for path, file in tm.filemap.items():
         if len(path) >= len(arg) and path[:len(arg)] == arg:
            result.add(file)
   elif filterType == "name":
      for file in tm.filemap.values():
         if file.name == arg:
            result.add(file)

   for filterType, tagname in utils.chunks(args[3:], 2):
      if filterType == "tag":
         for file in (f for f in result if tagname not in file.tags):
            result.remove(file)

   for file in result:
      print(file)
if __name__ == "__main__":
   main()