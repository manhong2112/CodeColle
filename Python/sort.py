import random
import timeit
import multiprocessing

def printf(string, *obj):
    return print(string.format(*obj))


def bubble_sort(arr):
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

def middle(a, b, c):
    return min(max(a, b), c)

def quick_sort_v2(arr):
    # [1 ,2 , 3]
    length = len(arr)
    if length <= 1:
        return arr
    elif length < 16:
        return select_sort(arr)
    else:
        # [1,2,3,4,5,6,7,8]
        k = length//2
        pivot1 = middle(arr[k//3+1], arr[k*2//3+1], arr[k])
        pivot2 = middle(arr[k+1], arr[k+k*2//3+1], arr[-1])
        chunk1 = []
        chunk2 = []
        chunk3 = []
        chunk4 = []
        chunk5 = []
        for i in arr:
            if i < pivot1:
                chunk1.append(i)
            elif i == pivot1:
                chunk2.append(i)
            elif i > pivot2:
                chunk5.append(i)
            elif i == pivot2:
                chunk4.append(i)
            else:
                chunk3.append(i)
        return quick_sort_v2(chunk1) + chunk2 + quick_sort_v2(chunk3) + chunk4 + quick_sort_v2(chunk5)

def swap(arr, x, y):
    arr[x], arr[y] = arr[y], arr[x]

def quicksort_inplace_iter(arr):
    stack = [(0, len(arr))]
    while stack:
        s, e = stack.pop()
        if s >= e:
            continue
        s1, e1 = s, e
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
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j-1] > arr[j]:
            swap(arr, j, j-1)
            j -= 1
    return arr

def bit_quick_sort(arr, n=32):
    if not arr or n <= 0:
        return arr
    bit0 = []
    bit1 = []
    for i in arr:
        if i & (1 << n):
            bit1.append(i)
        else:
            bit0.append(i)
    return bit_quick_sort(bit0, n-1) + bit_quick_sort(bit1, n-1)

def time(fun, *arr):
    s = timeit.default_timer()
    fun(*arr)
    e = timeit.default_timer()
    return((e - s) * 1000)