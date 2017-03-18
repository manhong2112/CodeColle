print(end="\t")
for i in range(1, 10):
    print(i, end="\t")
print()
for i in range(1, 10):
    print(i, end="\t")
    for j in range(1, 10):
        print(i * j, end="\t")
    print()

for i in range(1, 10):
    for j in range(1, 10):
        print(i, "*", j, '=', i * j)
