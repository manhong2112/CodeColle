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
        # TODO
        self.args_namelist = []
        self.args_len = len(self.args_namelist)
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
        fun = interp0(expr[0], env, scope, scopeLevel)[0]
        return fun.invoke(expr[1:], env, scope)
    elif is_int(expr):
        return (int(expr), None)
    elif is_float(expr):
        return (float(expr), None)
    else:
        return (env.get(scope, expr), None)

def interp(expr):
    env = Env()
    init_env(env)
    return interp0(expr, env, None)[0]

def init_env(env):
    def _add(args, env, scope):
        args[0] = interp0(args[0], env, scope)[0]
        return functools.reduce(lambda x, y: x + interp0(y, env, scope)[0], args)
    def _sub(args, env, scope):
        args[0] = interp0(args[0], env, scope)[0]
        return functools.reduce(lambda x, y: x - interp0(y, env, scope)[0], args)
    def _mul(args, env, scope):
        args[0] = interp0(args[0], env, scope)[0]
        return functools.reduce(lambda x, y: x * interp0(y, env, scope)[0], args)
    def _div(args, env, scope):
        args[0] = interp0(args[0], env, scope)[0]
        return functools.reduce(lambda x, y: x / interp0(y, env, scope)[0], args)
    def _do(args, env, scope):
        res = None
        for i in args:
            res = interp0(i, env, scope)
        return res[0]
    def _def(args, env, scope):
        env.set(scope[1], str(args[0]), interp0(args[1], env, scope[1])[0])
    def _defn(args, env, scope):
        env.set(scope[1], str(args[0]), interp0(args[1], env, scope[1])[0])
    def _print(args, env, scope):
        res = map(lambda y: str(interp0(y, env, scope)[0]), args)
        print(" ".join(res))

    env.set(None, "defn", PreDefFunc(_defn))
    env.set(None, "do", PreDefFunc(_do))
    env.set(None, "print", PreDefFunc(_print))
    env.set(None, "def", PreDefFunc(_def))

    env.set(None, "+", PreDefFunc(_add))
    env.set(None, "-", PreDefFunc(_sub))
    env.set(None, "*", PreDefFunc(_mul))
    env.set(None, "/", PreDefFunc(_div))


def unittest():
    """Simple Unit Test"""
    data = ["(do (print 1 1) (+ 1 1))", 2,
            "(+(+ 1             1)    1)", 3,
            "(* (+ (+ 2 2) (+ 2 2)) (+ (+ 2 2) (+ 2 2)))", 64,
            "(do (def x 1) x)", 1,
            "(do (def x (do (def x 2) (print x) 1)) x)", 1,
            ]

    for i in range(0, len(data), 2):
        try:
            res = interp(parser(data[i]))
        except Exception as e:
            print(f"Exception at Test{int(i/2)}")
            print("--", e)
            continue
        if res == data[i + 1]:
            print(f"Test{int(i/2)} Passed")
        else:
            print(f"Test{int(i/2)} Failed, Expected '{data[i + 1]}' but got '{res}'")

unittest()