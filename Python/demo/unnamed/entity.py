from cache import Cache
from item import *

class Player():
    def __init__(self, name, attribute=None):
        self.name = name
        self.backpack = []
        self.attribute = attribute or Attribute()
        self.buff = []

    def addItem(self, item):
        cache = Cache()
        if not cache.haskey("item"):
            cache.item = {}
        cache.item[item.id] = item
        self.backpack.append(item.id)
        if type(item) is Item:
            for k, v in item.attribute.items():
                self.attribute[k] += v

    def delItem(self, itemid):
        item = Cache().cache.item[itemid]
        if type(item) is Item:
            for k, v in item.attribute.items():
                self.attribute[k] -= v
        del self.backpack[itemid]

class Mob():
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute
