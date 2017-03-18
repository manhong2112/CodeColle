import os
import os.path
import multiprocessing
import time

def getDir(dir):
    cmd = f'adb shell "find \'{dir}\' -maxdepth 1 -type d | cut -c {len(dir.encode("utf8"))+1}-"'
    return os.popen(cmd).read().split("\n")[1:-1]


def getFile(dir):
    cmd = f'adb shell "find \'{dir}\' -maxdepth 1 -type f | cut -c {len(dir.encode("utf8"))+1}-"'
    return os.popen(cmd).read().split("\n")[:-1]


def pullFile(file, dist):
    cmd = f'adb pull "{file}" "{dist}"'
    os.popen(cmd).read()
    print(file, "->", dist)
    threadCount -= 1

def backup(pool, dir, dist, overwrite=True):
    for f in getFile(dir):
        i = f"{dir}{f}"
        o = f"{dist}{f}"
        if overwrite or not os.path.isfile(o):
            os.makedirs(os.path.split(o)[0], exist_ok=True)
            pool.apply_async(pullFile, (i, o))
    for d in getDir(dir):
        backup(pool, f"{dir}{d}", f"{dist}{d}", overwrite)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(16)
    backup(pool, "/sdcard/", "sdcard/", True)
#             exist 
# overwrite |   0   |   1   |
#     0     |   1   |   0   |
#     1     |   1   |   1   |