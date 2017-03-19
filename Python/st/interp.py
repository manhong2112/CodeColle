"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
# parser str to list
def parser(expr):
    def _f(index):
        result = []
        buffer = []
        while True:
            if expr[index] == "(":
                if buffer:
                    result.append(''.join(buffer))
                buffer = []
                sub_res, index = _f(index + 1)
                result.append(sub_res)
            char = expr[index]
            if char == ")":
                if buffer:
                    result.append(''.join(buffer))
                return result, index + 1
            elif char == " ":
                if buffer:
                    result.append(''.join(buffer))
                    buffer = []
            else:
                buffer.append(char)
            index += 1
    return _f(1)[0]

class Func():
    def __init__(self, func, scope):
        self.args_namelist = []
        self.args_len = len(args_namelist)
        self.func = func
        self.scope = scope
        self.runtime = 0

    def invoke(self, args):
        pass

class PreDefFunc(Func):
    def __init__(self, func):
        self.func = func
        self.scope = None
        self.runtime = 0

    def invoke(self, args):
        return (self.func(args), None)

class Env():
    def __init__(self):
        self.env = dict()

    def get(self, scope, name):
        while True:
            try:
                return self.env[(name, scope)]
            except KeyError:
                if scope is None:
                    return None
                else:
                    scope = scope[1]

    def set(self, scope, name, val):
        self.env[(name, scope)] = val

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def interp0(expr, env, scope):
    if isinstance(expr, list):
        lst = []
        for i in range(0, len(expr)):
            lst.append(interp0(expr[i], env, scope)[0])
        return lst[0].invoke(lst[1:])
    elif is_int(expr):
        return (int(expr), None)
    elif is_float(expr):
        return (float(expr), None)
    else:
        return (env.get(scope, expr), None)

def interp(expr):
    env = Env()
    env.set(None, "+", PreDefFunc(lambda x: x[0] + x[1]))
    env.set(None, "-", PreDefFunc(lambda x: x[0] - x[1]))
    env.set(None, "*", PreDefFunc(lambda x: x[0] * x[1]))
    env.set(None, "/", PreDefFunc(lambda x: x[0] / x[1]))
    return interp0(expr, env, None)[0]
# [+ [+ 1 1] 1]

def unittest():
    """Simple Unit Test"""
    data = ["(+ 1 1)", "(+(+ 1 1) 1)", "(* (+ (+ 2 2) (+ 2 2)) (+ (+ 2 2) (+ 2 2)))"]
    result = [2, 3, 64]
    assert len(data) == len(result)
    for i in range(0, len(data)):
        res = interp(parser(data[i]))
        if res == result[i]:
            print(f"Test{i} Passed")
        else:
            print(f"Test{i} Failed, Expected '{result[i]}' but got '{res}'")

unittest()