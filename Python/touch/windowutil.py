import mouse
import random
import time
import win32gui
import re

def findwindow(name):
    _handle = None
    def fun(hwnd, wildcard):
        nonlocal _handle
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            _handle = hwnd
    win32gui.EnumWindows(fun, f".*{name}.*")
    return _handle

def getwindowsrect(name):
    """ (name) -> (startx, starty, endx, endy)"""
    hd = findwindow(name)
    if hd != 0:
        return win32gui.GetWindowRect(hd)