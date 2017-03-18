import os
from hashlib import md5 as hashlib


def md5(file):
    hash = hashlib()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hash.update(chunk)
    return hash.hexdigest()


def rename(old, new, state):
    new += '.' + old.split('.')[-1]
    if not (state or old == new):
        try:
            os.remove(new)
        except WindowsError:
            pass
    os.rename(old, new)

def main():
    file_name = os.path.split(__file__)[1]
    for state in [0, 1]:
        i = 1
        for file in os.listdir('.'):
            if file == file_name or os.path.isdir(file):
                continue
            rename(file, str(i) if state else md5(file), state)
            i += 1
    os.remove(file_name)
main()