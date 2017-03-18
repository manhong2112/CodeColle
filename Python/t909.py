j = 0
a = int(input())
if a > j:
    j = a
a = int(input())
if a > j:
    j = a
a = int(input())
if a > j:
    j = a
print(j)

j = 0

for i in range(0, 3):
    k = int(input())
    j = k if k > j else j
print(j)

j = 0
f = (lambda x, y: x if x > y else y)
for i in range(0, 3):
    j = f(j, int(input()))
print(j)


def f1(x):
    f = (lambda x, y: x if x > y else y)
    y = 0
    for i in x:
        y = f(i, y)
    return y


a = []
for i in range(0, 3):
    a.append(int(input()))

print(f1(a))


def f2(*x):
    for i in x: y = y if (y if 'y' in locals() else 0) > i else i
    return y


print(f2(int(input()), int(input()), int(input())))
