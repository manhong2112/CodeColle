import manager
import fileaccessor
if __name__ == "__main__":
   import cProfile
   dao = fileaccessor.WebDav("http://127.0.0.1", "/nextcloud/remote.php/dav/files/manhong2112/manhong", "manhong2112", "f60af455")
   tm = manager.TagManager(dao)
   tm.load()
   # cProfile.run("tm.load()")