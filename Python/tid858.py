o = [1, 1, 2, 2, 3, 4, 5, 5, 6, 7]
o2 = []
for i in o:
    if i in o2:
        continue
    o2.append(i)

o2.sort()
print(o2)
