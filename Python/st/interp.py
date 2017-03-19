"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
import functools

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
        self.closure = scope
        self.runtime = 0

    def invoke(self, args):
        pass

class PreDefFunc(Func):
    def __init__(self, func, scope=None):
        self.func = func
        self.closure = scope
        self.runtime = 0

    def invoke(self, args, env, scope):
        self.runtime += 1
        return (self.func(args, env, (self.runtime, scope)), None)

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
    except TypeError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def interp0(expr, env, scope, scopeLevel=0):
    if isinstance(expr, list):
        lst = []
        for i in range(0, len(expr)):
            if expr[i][0] == "'":
                lst.append(expr[i])
            else:
                lst.append(interp0(expr[i], env, scope, scopeLevel)[0])
        return lst[0].invoke(lst[1:], env, scope)
    elif is_int(expr):
        return (int(expr), None)
    elif is_float(expr):
        return (float(expr), None)
    else:
        return (env.get(scope, expr), None)

def interp(expr):
    env = Env()
    env.set(None, "+", PreDefFunc(lambda x, env, scope: x[0] + x[1]))
    env.set(None, "-", PreDefFunc(lambda x, env, scope: x[0] - x[1]))
    env.set(None, "*", PreDefFunc(lambda x, env, scope: x[0] * x[1]))
    env.set(None, "/", PreDefFunc(lambda x, env, scope: x[0] / x[1]))
    def _do(args, env, scope):
        return functools.reduce(lambda x, y: interp0(y, env, scope), args)[0]
    env.set(None, "do", PreDefFunc(_do))
    def _def(args, env, scope):
        env.set(scope, str(args[0]), interp0(args[1], env, scope[1])[0])
    env.set(None, "def", PreDefFunc(_def))
    def _print(args, env, scope):
        res = map(lambda y: str(interp0(y, env, scope)[0]), args)
        print(" ".join(res))
        return None
    env.set(None, "print", PreDefFunc(_print))
    return interp0(expr, env, None)[0]

def unittest():
    """Simple Unit Test"""
    data = ["(do (print 1 1) (+ 1 1))", 2,
            "(+(+ 1             1)    1)", 3,
            "(* (+ (+ 2 2) (+ 2 2)) (+ (+ 2 2) (+ 2 2)))", 64,
            "(do (def 'x (do (def 'x 2) (print 'x) 1)) 'x)", 1]

    for i in range(0, len(data), 2):
        res = interp(parser(data[i]))
        if res == data[i + 1]:
            print(f"Test{int(i/2)} Passed")
        else:
            print(f"Test{int(i/2)} Failed, Expected '{data[i + 1]}' but got '{res}'")

unittest()