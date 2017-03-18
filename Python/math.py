from decimal import Decimal, getcontext

getcontext().prec = 8


class F(object):
    def __init__(self, a, b, c):
        self.a = Decimal(a)
        self.b = Decimal(b)
        self.c = Decimal(c)


def q(F1, F2):
    assert type(F1) is F and type(F2) is F
    assert F1.a * F2.b - F1.b * F2.a is not 0
    x = (F1.c * F2.b - F2.c * F1.b) / (F1.a * F2.b - F2.a * F1.b)
    y = (F1.c - F1.a * x) / F1.b
    return {"x": x, "y": y}

while True:
    print((lambda x: "x={}, y={}".format(x["x"], x["y"]))(q(F(input("a="), input("b="), input("c=")), F(input("d="), input("e="), input("f=")))))
