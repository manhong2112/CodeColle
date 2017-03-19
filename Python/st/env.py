import interp
import functools

funcId = 0
class Func():
    def __init__(self, args, body, scope):
        # (lambda (<args>) <body>)
        self.args_namelist = args
        self.args_len = len(args)
        self.body = body
        global funcId
        funcId += 1
        self.closure = (funcId, scope)
        self.runtime = 0

    def invoke(self, args, env, scope):
        self.runtime += 1
        assert len(args) == self.args_len
        for i in range(0, self.args_len):
            env.set(
                (self.runtime, self.closure), # scope
                self.args_namelist[i], # var name
                interp.interp0(args[i], env, scope)[0]) # value
        return interp.interp0(self.body, env, (self.runtime, self.closure))

class PreDefFunc(Func):
    def __init__(self, func, scope=None):
        self.func = func
        global funcId
        funcId += 1
        self.closure = (funcId, scope)
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
                tmp = self.env[(name, scope)]
                # print("get:", (name, scope))
                return tmp
            except KeyError:
                if scope is None:
                    return None
                else:
                    scope = scope[1]

    def set(self, scope, name, val):
        # print("set:", (name, scope))
        assert (name, scope) not in self.env
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

def _add(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return functools.reduce(lambda x, y: x + interp.interp0(y, env, scope)[0], args)

def _sub(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return functools.reduce(lambda x, y: x - interp.interp0(y, env, scope)[0], args)

def _mul(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return functools.reduce(lambda x, y: x * interp.interp0(y, env, scope)[0], args)

def _div(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return functools.reduce(lambda x, y: x / interp.interp0(y, env, scope)[0], args)

def _do(args, env, scope):
    # (do ...)
    res = None
    for i in args:
        res = interp.interp0(i, env, scope)
    return res[0]

def _def(args, env, scope):
    # (def <name> <val>)
    # (def (<name> <args>) <body>) => (def <name> (lambda (<args>) <body>))
    if isinstance(args[0], list):
        env.set(scope[1], args[0][0], _lambda((args[0][1:], args[1]), env, scope[1]))
    else:
        env.set(scope[1], str(args[0]), interp.interp0(args[1], env, scope[1])[0])

def _lambda(args, env, scope):
    # (lambda (<fun args>) <fun body>)
    return Func(args[0], args[1], scope)

def _print(args, env, scope):
    # (print ...)
    res = map(lambda y: str(interp.interp0(y, env, scope)[0]), args)
    print(" ".join(res))

def _eq(args, env, scope):
    return interp.interp0(args[0], env, scope)[0] == interp.interp0(args[1], env, scope)[0]

def _if(args, env, scope):
    # (if <b> <t> <f>)
    if interp.interp0(args[0], env, scope)[0]:
        return interp.interp0(args[1], env, scope)[0]
    else:
        return interp.interp0(args[2], env, scope)[0]

def _let(args, env, scope):
    # (let ((<name> <value>) ... ) <body>)
    for i in args[0]:
        env.set(
            scope, # scope
            i[0], # var name
            interp.interp0(i[1], env, scope)[0]) # value
    return interp.interp0(args[1], env, scope)[0]


def init_env(env):
    env.set(None, "do", PreDefFunc(_do))
    env.set(None, "print", PreDefFunc(_print))
    env.set(None, "def", PreDefFunc(_def))
    env.set(None, "let", PreDefFunc(_let))
    env.set(None, "lambda", PreDefFunc(_lambda))
    env.set(None, "if", PreDefFunc(_if))
    env.set(None, "+", PreDefFunc(_add))
    env.set(None, "-", PreDefFunc(_sub))
    env.set(None, "*", PreDefFunc(_mul))
    env.set(None, "/", PreDefFunc(_div))
    env.set(None, "=", PreDefFunc(_eq))
    env.set(None, "#t", True)
    env.set(None, "#f", False)
