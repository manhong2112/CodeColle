import re
import os


def check(dir):
    for i in os.listdir(dir):
        if os.path.isdir(i):
            check(dir + "/" + i)
        print(str(i) + "\n" if re.search(r'.*\.txt', i) else "", end="")


check(os.getcwd())
