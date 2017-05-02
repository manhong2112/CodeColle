class Equip():
    def __init__(self, name, attribute, action):
        self.name = name
        self.attribute = attribute
        self.action = action

class Item():
    def __init__(self, name, attribute, buff):
        self.name = name
        self.attribute = attribute
        self.buff = buff

class Attribute(dict): pass
