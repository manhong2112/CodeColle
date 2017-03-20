"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
import env
import functools


# parser str to list
def parser(expr):
    length = len(expr)
    def _f(index):
        result = []
        buffer = []
        while index < length:
            if expr[index] == "(" or expr[index] == "[":
                if buffer:
                    if is_quote_by(buffer, '"') or is_quote_by(buffer, "'"):
                        result.append(env.String(''.join(buffer[1:-1])))
                    else:
                        result.append(''.join(buffer))
                    buffer = []
                sub_res, index = _f(index + 1)
                result.append(sub_res)
                if index >= length:
                    return result
            char = expr[index]
            if char == ")" or char == "]":
                if buffer:
                    if is_quote_by(buffer, '"') or is_quote_by(buffer, "'"):
                        result.append(env.String(''.join(buffer[1:-1])))
                    else:
                        result.append(''.join(buffer))
                return result, index + 1
            elif char == " ":
                if buffer:
                    if is_quote_by(buffer, '"') or is_quote_by(buffer, "'"):
                        result.append(env.String(''.join(buffer[1:-1])))
                    else:
                        result.append(''.join(buffer))
                    buffer = []
            else:
                buffer.append(char)
            index += 1
        return ''.join(buffer), index
    return _f(0)[0]

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

def is_none(s):
    return s is None

def is_string(s):
    return isinstance(s, env.String)

def is_quote_by(s, q):
    return s[0] == s[-1] == q

scopeID = 0
def interp0(expr, env, scope):
    if isinstance(expr, list):
        fun = interp0(expr[0], env, scope)[0]
        global scopeID
        scopeID += 1
        # print((str(fun), scope))
        return fun(expr[1:], env, (str(fun), scope))
    elif is_none(expr):
        return (None, None)
    elif is_string(expr):
        return (expr, None)
    elif is_int(expr):
        return (int(expr), None)
    elif is_float(expr):
        return (float(expr), None)
    else:
        return (env.get(scope, expr), None)

def interp(expr):
    return interp0(expr, env.Env(), None)[0]
