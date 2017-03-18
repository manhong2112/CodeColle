def queen(n):
    ans = [0]
    upperlim = (1 << n) - 1
    def test(row, ld, rd):
        p = 0
        pos = 0
        if row != upperlim:
            pos = upperlim & (~(row | ld | rd ))
            while pos != 0:
                p = pos & (~pos + 1)
                pos = pos - p
                test(row | p, (ld | p) << 1, (rd | p) >> 1);  
        else:
            ans[0] += 1
    test(0, 0, 0)
    return ans[0]

print(queen(8))

