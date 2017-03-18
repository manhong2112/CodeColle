from copy import copy

def pick(k, e):
    try:
        return e[k]
    except Exception:
        return k

def put(k, v, e):
    e[k] = v
    return e

def put_rec(pair, e):
    for k, v in pair:
        e[k] = interp(v, e)
    return e


class Closure:
    def __str__(self):
        return "<Closure exp({}), env({})>".format(self.exp, self.env)
        pass

    def __init__(self, exp, env):
        self.exp = exp
        self.env = env


class quote:
    def __str__(self):
        return "<quote %s>".format(self.lst)

    def __init__(self, lst):
        self.lst = lst
        pass

    def cons(x, _quote):
        l = copy(_quote.lst[::-1])
        l.append(str(x))
        return quote(l[::-1])

    def car(_quote):
        return _quote.lst[0]

    def cdr(_quote):
        return quote(_quote.lst[1:])

    def pick(i, _quote):
        return _quote.lst[i + 1]

    def put(i, v, _quote):
        l = copy(_quote.lst[:])
        l[i] = v
        return quote(l)


def interp(scheme, env={}):
    if isinstance(scheme, str):
        if (scheme[0] == "-" and scheme[1:].isdigit()) or scheme.isdigit():
            return eval(scheme)
        if scheme == "True" or scheme == "False":
            return eval(scheme)
        return pick(scheme, env)

    if isinstance(scheme, list):
        v0 = interp(scheme[0], env)
        if isinstance(v0, Closure):
            return interp(v0.exp[2], put(v0.exp[1][0], interp(scheme[1], env), v0.env))

        if v0 in ("if", "lambda", "let"):
            return {
                "if": lambda: interp(scheme[2 if interp(scheme[1], env) else 3], env),
                "lambda": lambda: Closure(scheme, copy(env)),
                "let": lambda: interp(scheme[2], put_rec(scheme[1], env))
            }[v0]()

        v1 = interp(scheme[1], env)
        if v0 in ("car", "cdr"):
            return {
                "car": lambda: quote.car(v1),
                "cdr": lambda: quote.cdr(v1)
            }[v0]()

        v2 = interp(scheme[2], env)
        if v0 in ("pick", "cons", "+", "-", "*", "/", "^", "=", ">", "<", "<=", ">="):
            return {
                "pick": lambda: quote.pick(v1, v2),
                "cons": lambda: quote.cons(v1, v2),
                "+": lambda: v1 + v2,
                "-": lambda: v1 - v2,
                "*": lambda: v1 * v2,
                "/": lambda: v1 / v2,
                "^": lambda: v1 ** v2,
                "=": lambda: v1 == v2,
                ">": lambda: v1 > v2,
                "<": lambda: v1 < v2,
                "<=": lambda: v1 <= v2,
                ">=": lambda: v1 >= v2
            }[v0]()


# (lambda arg exp) => Closure((lambda arg exp) env)
# (Closure(lambda env) arg)
# (quote (lst))
# (if b t f)
# (op e1 e2)
# (let ((k1 exp1) .. (kn expn)) exp)

# parser str to list
def parser(s):
    def _f(index):
        result = []
        t = ""
        while True:
            if s[index] == "(":
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


print(interp(parser("(let ((abs (lambda (n) (if (< n 0) (- 0 n) n)))) (abs -5))")))

