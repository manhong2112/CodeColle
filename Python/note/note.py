class TagNode(object):
    def __init__(self, tagname, tagmap):
        self.tagname = tagname
        self.content = set()
        self.next = {} # TagName: Tag
        self.path = None
        tagmap.setpath(tagname, self)

    def insert(self, tagtree):
        tagtree.path = self.path + "." + tagtree.tagname
        self.next[tagtree.tagname] = tagtree

class TagMap(object):
    def __init__(self):
        self.map = {} # TagName: Tag

    def setpath(self, tagname, tag):
        self.map[tagname] = tag
    
    def search(self, tagname):
        r = set()
        for i in self.map:
            if tagname in i:
                r.add(i)
        return r
    
    def get(self, tagname):
        return self.map[tagname]

class Content(object):
    def __init__(self, Name, Text = ""):
        self.text = Text
        self.name = Name
        self.tag = set()

    def addtag(self, tag):
        tag.content.add(self)
        self.tag.add(tag)
    
    def gettag(self):
        return self.tag

tagMap = TagMap()
root = TagNode("root", tagMap)
root.path = "root"
# ====
rt = tagMap.get(tagMap.search("root").pop())

secondNode = TagNode("secondNode", tagMap)
rt.insert(secondNode)
ct = Content("Hello World")
ct.addtag(secondNode)

for i in tagMap.map:
    print(i + ": " +  tagMap.map[i].path)
    for j in tagMap.map[i].content:
        print("  - " + j.name + " #" + "".join(map(lambda x: x.path, j.gettag())))