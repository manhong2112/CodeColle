"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
# parser str to list
def parser(s):
    def _f(index):
        result = []
        t = ""
        while True:
            if s[index] == "(":
                if t != "":
                    result.append(t)
                t = ""
                x, index = _f(index + 1)
                result.append(x)
            c = s[index]
            if c == ")":
                if t != "":
                    result.append(t)
                return result, index + 1
            elif c == " ":
                if t != "":
                    result.append(t)
                    t = ""
            else:
                t += c
            index += 1
    return _f(1)[0]

class Closure():
    def __init__(self, func, scope):
        # TODO
        self.argsList = []
        self.argsLen = len(argsList)
        self.func = func
        self.scope = scope
        self.runtime = 0
    
    def invoke(self, args, env):
        for i in range(0, self.argsLen):
            

class PreDefFunc():
    def invoke(args, env):
        for i in range(0, self.argsLen):

class Env():
    def __init__(self):
        self.env = dict()
    def get(self, scope, name):
        while True:
            try:
                return self.env[(name, scope)]
            except KeyError:
                scope = scope[1]
                if scope is None:
                    return None
    def set(self, scope, name, val):
        self.env[(name, scope)] = val

def interp0(expr, env, scope):
    if expr is list
        if expr[0] is list:
            e0 = interp(expr, env, scope)
        fun = expr[interp(expr, env, scope)]
        for i in expr:
    else:
        return (env.get(scope, expr), None)

def interp(expr):
    interp0(expr, Env(), None)[0]
# [+ [+ 1 1] 1]
print(interp(parser("(+(+ 1 1) 1)"), Env(), None))