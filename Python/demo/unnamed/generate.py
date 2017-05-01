cache = {}
def newName(seed):
    if "name" not in cache:
        cache["name"] = open("dict.txt").read().split("\n")
    pass

def newItem(seed):
    pass

def newEquip(seed):
    pass

def newMob(seed):
    pass


class Mob():
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute

class Equip():
    def __init__(self, name, attribute, skill):
        self.name = name
        self.attribute = attribute

class Item():
    def __init__(self, name, attribute, skill):
        self.name = name
        self.attribute = attribute

class Attribute(dict): pass
