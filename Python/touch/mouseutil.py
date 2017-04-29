import mouse
import random
import time
import win32gui
import re

def rclick(range):
    x, y = mouse.getPos()
    mouse.move(x * random.random() * range, y * random.random() * range, 0.01)
    mouse.click()

def rdelay(sec, randrange=10):
    time.sleep(sec + (-1 if random.randint(1, 2) else 1) * random.randint(0, randrange))


