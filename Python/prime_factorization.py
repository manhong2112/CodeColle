from functools import *
def f(x):
    k = int(x ** 0.5)
    def _f(x, n):
        if n > k:
            return [x]
        elif x % n == 0:
            return [n] + _f(x//n, n)
        else:
            return _f(x, n+2)
    if x % 2 == 0:
        return [2] + f(x//2, 3)
    else:
        return _f(x, 3)