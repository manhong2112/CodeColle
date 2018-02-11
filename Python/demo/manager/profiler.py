import manager
import fileaccessor
if __name__ == "__main__":
   import cProfile
   dao = fileaccessor.Local("")
   tm = manager.TagManager(dao)
   cProfile.run("tm.load(0)")