import random
import timeit


def printf(string, *obj):
    return print(string.format(*obj))


def bubble_sort(arr):
    arr = arr[:]
    for i in range(len(arr) - 1, 0, -1):
        for j in range(i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    a = arr[0]
    b = []
    c = []
    for i in arr[1:]:
        (b if i < a else c).append(i)
    return quick_sort(b) + [a] + quick_sort(c)


def quicksort_inplace_iter(arr):
    stack = [(0, len(arr))]
    while stack:
        s, e = stack.pop()
        s1, e1 = s, e
        if s >= e:
            continue
        i = s
        x = arr[e-1]
        while s+1 < e1:
            if arr[s] > x:
                swap(arr, s, e1 - 1)
                e1 -= 1
            else:
                swap(arr, s, s1)
                s1 += 1
            s += 1
        stack.append((i, s))
        stack.append((s+1, e))


def random_arr(length):
    arr = []
    for i in range(length):
        arr.append(random.randint(0, length ** 2))
    return arr


def merge_sort(arr):
    def merge(arr1, arr2):
        result = []
        i = 0
        j = 0
        while True:
            if i == len(arr1):
                result.extend(arr2[j:])
                break
            if j == len(arr2):
                result.extend(arr1[i:])
                break
            if arr1[i] < arr2[j]:
                result.append(arr1[i])
                i += 1
            else:
                result.append(arr2[j])
                j += 1
        return result

    length = len(arr)
    if length <= 1:
        return arr
    return arr if length <= 1 else merge(
        merge_sort(arr[:int(length / 2)]),
        merge_sort(arr[int(length / 2):]))


def select_sort(arr):
    for i in range(len(arr)):
        for j in range(i, len(arr)):
            if arr[j] < arr[i]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr


def time(fun, *arr):
    s = timeit.default_timer()
    fun(*arr)
    e = timeit.default_timer()
    return((e - s) * 1000)