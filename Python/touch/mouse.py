import win32api, win32con
import math
import time

def setPos(x, y):
    win32api.SetCursorPos((x,y))

def getPos():
    return win32api.GetCursorPos()

def click():
    x, y = getPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def move(x, y, sec=1):
    # range [0, 100]
    fun = lambda x: - (10 * (x - 100)) / ( x + 20) / 1125
    i = 0
    origx, origy = getPos()
    nowx, nowy = origx, origy
    while i < 100:
        i += 1
        nowx += (x-origx) * abs(fun(i))
        nowy += (y-origy) * abs(fun(i))
        setPos(int(nowx), int(nowy))
        time.sleep(sec/100)
    setPos(x, y)