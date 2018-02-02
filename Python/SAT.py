import random
def f(n):
    return [random.randint(0, 255) for i in range(n)]

i = [f(10) for _ in range(10)]

#   x ->
# y --------
# | [[ a b ]
# v  [ c d ]]
def build(i):
    l1 = len(i)
    l2 = len(i[0])
    I = [[0] * l2 for _ in range(l1)]
    assert l1 != 0 and l2 != 0
    for x in range(l2):
        for y in range(l1):
            for a in range(y):
                for b in range(x):
                    print(i[a][b])
                    I += i[a][b]
    return I