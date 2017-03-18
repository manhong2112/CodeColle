import os
import os.path
import threading
import time

threadCount = 0


def getDir(dir):
    cmd = f'adb shell "find \'{dir}\' -maxdepth 1 -type d | cut -c {len(dir.encode("utf8"))+1}-"'
    return os.popen(cmd).read().split("\n")[1:-1]


def getFile(dir):
    cmd = f'adb shell "find \'{dir}\' -maxdepth 1 -type f | cut -c {len(dir.encode("utf8"))+1}-"'
    return os.popen(cmd).read().split("\n")[:-1]


def pullFile(file, dist):
    while threadCount > 50:
        time.sleep(1)
    threading.Thread(target=pullFile0, args=(file, dist)).start()


def pullFile0(file, dist):
    global threadCount
    threadCount += 1
    cmd = f'adb pull "{file}" "{dist}"'
    os.popen(cmd).read()
    print(file, "->", dist)
    threadCount -= 1


def backup(dir, dist, overwrite=True):
    for f in getFile(dir):
        i = f"{dir}{f}"
        o = f"{dist}{f}"
        if overwrite or not os.path.isfile(o):
            os.makedirs(os.path.split(o)[0], exist_ok=True)
            pullFile(i, o)
    for d in getDir(dir):
        backup(f"{dir}{d}", f"{dist}{d}", overwrite)

backup("/sdcard/", "sdcard/", False)
#             exist 
# overwrite |   0   |   1   |
#     0     |   1   |   0   |
#     1     |   1   |   1   |