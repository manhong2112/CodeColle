import os
import math
import pickle
sum = lambda x: 0 if len(x) == 0 else x[0] + sum(x[1:])


class Reader(object):

    def __init__(self, path=None):
        self.Note = NoteManager.get_note(path)
        self.Note.load()
        pass

    def read(self):
        return self.Note.Context

    def write(self, context):
        self.Note.Context = context
        pass

    def write_line(self, context):
        self.Note.Context += context
        self.Note.Context += "\n"
        pass

    def append(self, context):
        self.Note.Context += context
        pass

    def save(self):
        with open(self.Note.nPath, "wb+") as f:
            pickle.dump((self.Note.Context, self.Note.Type), f)


class Note(object):
    storageLoc = "./note"

    def __init__(self, path, name, file_type="Text"):
        assert type(name) is str
        assert type(path) is str
        assert type(file_type) is str
        self.Name = name
        self.Type = file_type
        self.id = path
        self.nPath = os.path.join(self.storageLoc, path)
        self.Context = ""

    def load(self):
        os.makedirs(os.path.dirname(self.nPath), exist_ok=True)
        if not os.path.isfile(self.nPath):
            with open(self.nPath, "wb+") as f:
                pickle.dump(("", self.Type), f)
        with open(self.nPath, "rb+") as f:
            self.Context, self.Type = pickle.load(f)


class NoteManager(object):
    note_pool_loc = "./NoteList.db"
    __note_pool = {}

    @staticmethod
    def get_note(path):
        pool, name = NoteManager.parse_path(path)
        return pool[name]["Note"]
        pass

    @staticmethod
    def new_note(path, name, file_type="Text"):
        n = Note(path, name, file_type)
        NoteManager.add_note(path, n)
        pass

    @staticmethod
    def filter(dir, f):
        assert type(dir) is str
        result = []
        pool, name = NoteManager.parse_path(dir)
        for i in pool:
            if i[-1] == "/":
                result.extend(NoteManager.filter(dir + i, f))
            elif (pool[i]["Tag"] & f) == f:
                result.append(dir + i)
        return sorted(result)
        pass

    @staticmethod
    def save():
        tmp = {}

        def _f(path, pool):
            for p in pool:
                if p[-1] == "/":
                    _f(path + p, pool[p])
                else:
                    x = pool[p]
                    tmp[p] = {"Tag": x["Tag"], "Name": x["Note"].Name}
        _f("", NoteManager.__note_pool)
        with open(NoteManager.note_pool_loc, "wb+") as f:
            pickle.dump(tmp, f)
        pass

    @staticmethod
    def add_note(path, note):
        pool, name = NoteManager.parse_path(path)
        pool[name] = {"Tag": 0, "Note": note}
        pass

    @staticmethod
    def del_note(path):
        os.remove(os.path.join(Note.storageLoc, path))
        pool, name = NoteManager.parse_path(path)
        pool.remove(name)
        pass

    @staticmethod
    def add_tag(path, *tag):
        pool, name = NoteManager.parse_path(path)
        t = sum(tag)
        if (pool[name]["Tag"] & t) != t:
            pool[name]["Tag"] += t

    @staticmethod
    def del_tag(path, *tag):
        pool, name = NoteManager.parse_path(path)
        t = sum(tag)
        if (pool[name]["Tag"] & t) == t:
            pool[name]["Tag"] -= t

    @staticmethod
    def get_tag(path):
        pool, name = NoteManager.parse_path(path)
        t = pool[name]["Tag"]
        tag = set({})
        while t != 0:
            x = int(math.log(t, 2))
            t -= x
            tag.add(TagManager.tag(x))
            pass
        return tag

    @staticmethod
    def parse_path(path):
        x = path.split("/")
        pool = NoteManager.__note_pool
        for i in x[:-1]:
            if i + "/" not in pool:
                pool[i + "/"] = {}
            pool = pool[i + "/"]
        return pool, x[-1]

    if not os.path.isfile(note_pool_loc):
        with open(note_pool_loc, "wb+") as f:
            pickle.dump(__note_pool, f)
    else:
        with open(os.path.join(note_pool_loc), "rb+") as f:
            tmp = pickle.load(f)
        for i in tmp:
            x = i.split("/")
            pool = __note_pool
            for i in x[:-1]:
                if i + "/" not in pool:
                    pool[i + "/"] = {}
                pool = pool[i + "/"]
            name = x[-1]
            pool[name] = {"Tag": tmp[i]["Tag"],
                          "Note": Note(i, tmp[i]["Name"])}


class TagManager(object):
    tag_pool_loc = "TagList.db"
    __tag_pool = []

    @staticmethod
    def mk_filter(*tag):
        return sum(tag)

    @staticmethod
    def new_tag(tag_name):
        if tag_name not in TagManager.__tag_pool:
            TagManager.__tag_pool.append(tag_name)
        pass

    @staticmethod
    def tag(x):
        if type(x) is str:
            return 2**TagManager.__tag_pool.index(x)
        elif type(x) is int:
            return TagManager.__tag_pool[math.log(x, 2)]

    @staticmethod
    def save():
        with open(os.path.join(TagManager.tag_pool_loc), "wb+") as f:
            pickle.dump(TagManager.__tag_pool, f)
        pass

    if os.path.isfile(tag_pool_loc):
        with open(os.path.join(tag_pool_loc), "rb+") as f:
            __tag_pool = pickle.load(f)
    else:
        with open(os.path.join(tag_pool_loc), "wb+") as f:
            pickle.dump(__tag_pool, f)

