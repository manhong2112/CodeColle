import pathlib

def delete_folder(path) :
   pth = pathlib.Path(path)
   for sub in pth.iterdir() :
      if sub.is_dir() :
         delete_folder(sub)
      else :
         sub.unlink()
   pth.rmdir()
