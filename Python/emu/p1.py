F = 0
M = 0
TOTAL = 1 << 20

while TOTAL > 0:
    k = TOTAL >> 1
    F += k
    M += TOTAL - k
    TOTAL = k

print(F, M)