from array import array
import hashlib
import base64

def gen(*args, n=1, m=1):
    r = f1(*args)
    for i in range(0, n):
        r = f2(r)
    for i in range(0, m):
        r = f1(*(r.encode()))
    return f2(r)

def f1(*args):
    k = []
    for i in args:
        r = []
        s = str(i).encode()
        for j in range(1, len(s) + 1):
            r.append((s[j - 1] * j) % 26)
        k.append(sum(r))
    x = sum(k)
    for i in k:
        x *= i
    return str(x)

def f2(data):
    m = hashlib.md5(data.encode()).hexdigest()
    s = hashlib.sha256(str(m).encode()).hexdigest()
    b = base64.b64encode(str(int(s, 16) ^ int(m, 22)).encode()).decode("utf-8")
    t = str(int(s, 28) % int(m, 34))
    return str(hashlib.md5((t + b).encode()).hexdigest())
