def binarySearch(n, arr):
    return binarySearch0(n, arr, 0, len(arr) - 1)

def binarySearch0(n, arr, start, end):
    if len(arr) == 0 or start > end:
        return -1
    k = (end + start) >> 1
    v = arr[k]
    if v == n:
        return k
    elif n < v:
        return binarySearch0(n, arr, start, k - 1)
    else:
        return binarySearch0(n, arr, k + 1, end)

binarySearch(0, [1, 2])