#include <stdio.h>
int main() {
    printf("%d\n", queen(4));
    return 0;
}
int queen(int n) {
    return queen(0, 0, 0, 0)
}
int _queen(int l, int r, int m, int k) {
    int ans = 0;

    for(int i = (~(l | r | m)) & 0xff; i; i -= i & -i) {
        ans += queen((l | (i & -i)) << 1, (r | (i & -i)) >> 1 , m | (i & -i), k + 1);
    }

    return k == 8 ? 1 : ans;
}
