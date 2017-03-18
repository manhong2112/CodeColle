import msvcrt


def interp(expr):
    ptr = 0
    ram = dict()
    loopStack = []
    excapingLoop = 0
    i = 0
    while(i < len(expr)):
        # print(ram, loopStack, excapingLoop)
        x = expr[i]
        if not (ptr in ram) or ram[ptr] > 127 or ram[ptr] < -128:
            ram[ptr] = 0
        if x == "[":
            if excapingLoop > 0:
                excapingLoop += 1
            elif ram[ptr] != 0:
                loopStack.append(i)
            else:
                excapingLoop = 1
        elif x == "]":
            if excapingLoop > 0:
                excapingLoop -= 1
            elif ram[ptr] != 0:
                i = loopStack[-1]
            else:
                loopStack.pop()
        elif excapingLoop > 0:
            pass
        elif x == "+":
            ram[ptr] += 1
        elif x == "-":
            ram[ptr] -= 1
        elif x == ">":
            ptr += 1
        elif x == "<":
            ptr -= 1
        elif x == ".":
            print(chr(ram[ptr]), end="")
            pass
        elif x == ",":
            ram[ptr] = ord(msvcrt.getch())
        i += 1

version = 0x01
header = [0x00, 0x10, 0x26, 0xBF, version, 0x00]
# null, id, id, ver, id, mem_len


class ID():
    START_LOOP = 0
    END_LOOP = 1
    INC = 2
    DEC = 3
    NEXT = 4
    BACK = 5
    GETC = 6
    PUTC = 7

    ADD = 8
    MOVE = 9


def compile(expr):
    result = header.copy()
    state = 0
    tmp = 0
    memloc = 0
    mmemloc = 0
    loopStack = []
    i = 0
    while i <= len(expr):
        # print(ram, loopStack, excapingLoop)
        if memloc > mmemloc:
            mmemloc = memloc
        x = expr[i] if i != len(expr) else 0xFF
        if state == 0:
            if x == "[":
                loopStack.append(len(result))
                result.append(ID.START_LOOP)
                result.append(0)
                if memloc == 0:
                    memloc = 1
            elif x == "]":
                a = loopStack.pop()
                result[a + 1] = len(result) - a - 1
                result.append(ID.END_LOOP)
                result.append(len(result) - a + 1)
            elif x == "+":
                state = ID.ADD
                tmp += 1
            elif x == "-":
                state = ID.ADD
                tmp -= 1
            elif x == ">":
                state = ID.MOVE
                tmp += 1
            elif x == "<":
                state = ID.MOVE
                tmp -= 1
            elif x == ".":
                result.append(ID.PUTC)
            elif x == ",":
                result.append(ID.GETC)
        elif state == ID.ADD:
            if x in "+-":
                if x == "+":
                    tmp += 1
                elif x == "-":
                    tmp -= 1
            else:
                if tmp == 0:
                    pass
                elif tmp == 1:
                    result.append(ID.INC)
                elif tmp == -1:
                    result.append(ID.DEC)
                else:
                    result.append(ID.ADD)
                    result.append(tmp)
                state = 0
                i -= 1
                tmp = 0
        elif state == ID.MOVE:
            if x in "><":
                if x == ">":
                    tmp += 1
                elif x == "<":
                    tmp -= 1
            else:
                if tmp == 0:
                    pass
                elif tmp == 1:
                    result.append(ID.NEXT)
                    memloc += 1
                elif tmp == -1:
                    result.append(ID.BACK)
                    memloc -= 1
                else:
                    result.append(ID.MOVE)
                    result.append(tmp)
                    memloc += tmp
                i -= 1
                state = 0
                tmp = 0
        i += 1
    result[5] = mmemloc
    result.append(0xFF)
    return result


class Env(object):
    def __init__(self, mem_len):
        self.data = [0] * (mem_len + 1)
        self.ptr = 0

    def move(self, val):
        self.ptr += val

    def read(self):
        return self.data[self.ptr]

    def write(self, val):
        self.data[self.ptr] = val if -128 <= val <= 127 else 0


def execute(compiledExpr):
    expr = compiledExpr
    i = len(header)
    env = Env(expr[5])
    while i < len(expr) - 1:
        x = expr[i]
        if x == ID.INC:
            env.write(env.read() + 1)
        elif x == ID.DEC:
            env.write(env.read() - 1)
        elif x == ID.NEXT:
            env.move(1)
        elif x == ID.BACK:
            env.move(-1)
        elif x == ID.PUTC:
            print(chr(env.read()), end="")
        elif x == ID.GETC:
            env.write(ord(msvcrt.getch()))
        else:
            if x == ID.START_LOOP and env.read() == 0:
                i += expr[i + 1]
            elif x == ID.END_LOOP and env.read() != 0:
                i -= expr[i + 1]
            elif x == ID.ADD:
                env.write(env.read() + expr[i + 1])
            elif x == ID.MOVE:
                env.move(expr[i + 1])
            i += 1
        i += 1

import timeit


def time(fun, *arr):
    s = timeit.default_timer()
    fun(*arr)
    e = timeit.default_timer()
    return((e - s) * 1000)

expr = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
cexpr = compile(expr)

x1, x2 = 0, 0
for i in range(0, 1000):
    x1 += time(execute, cexpr)
for i in range(0, 1000):
    x2 += time(interp, expr)

print(x1 / 1000)
print(x2 / 1000)
