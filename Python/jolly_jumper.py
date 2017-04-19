def f(arr):
    l = len(arr) - 1
    for a, b in zip(arr, arr[1:]):
        # print(l, i, n)
        if abs(b - a) != l:
            return False
        l -= 1
    return True
# Why f([2 -1 0 2]) should be True ???