j = int(input())
x, y = 1, 0

for i in range(1, j + 1):
    x, y = y, x + y
    print(y)


def f1(n):
    if n <= 2:
        return 1
    return f1(n - 1) + f1(n - 2)

for i in range(1, j + 1):
    print(f1(i))

f = (lambda n: 1 if n <= 2 else f(n-1) + f(n-2))
for i in range(1, j + 1):
    print(f(i))
