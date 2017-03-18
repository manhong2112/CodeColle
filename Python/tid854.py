import random
import sys

o = []
m, n = int(input("m = ")), int(input("n = "))
if 1 <= m <= n:
    sys.exit(1)
while len(o) < n:
    a = random.choice(range(1, m + 1))
    if a in o:
        continue
    o.append(a)

o.sort()
print(o)
