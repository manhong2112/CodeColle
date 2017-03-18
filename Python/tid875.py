import re
import os


def check(dir, text):
    for i in os.listdir(dir):
        if os.path.isdir(i):
            check(dir + "/" + i, text)
        if re.search(r'.*\.txt', i):
            file = open(dir + "/" + i, encoding="utf8").read()
            print(str(i) + "\n" if re.search(text, file) else "", end="")


check(os.getcwd(), "hello world")
