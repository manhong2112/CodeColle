class Cache():
    __CACHE = {}
    def __init__(self):
        self.__CACHE = Cache.__CACHE
    def __getattr__(self, name):
        return self.__CACHE[name]
    def __setattr__(self, name, val):
        self.__CACHE[name] = val
    def haskey(self, name):
        return name in self.__CACHE