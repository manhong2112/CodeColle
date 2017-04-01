def f(items, C):
    lst = []
    for i in items:
        it = items[:]
        it.remove(i)
        if C-i[0] < 0: continue
        lst.append(f(it, C-i[0]) + i[1])
    if len(lst) == 0:
        return 0
    return max(lst)
