n, char = input().split(" ")
total = int(n)
n = int((2 * (total + 1)) ** .5 / 2) - 1
i = n
c = 2 * n + 1
while i >= -n:
    tmp = 2 * abs(i) + 1
    print(" " * ((c - tmp) // 2) + char * tmp)
    i -= 1
print(char * (total - 2 * n * n - 4 * n - 1))
