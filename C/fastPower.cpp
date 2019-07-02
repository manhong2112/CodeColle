#include <iostream>
#define ll long long
using namespace std;

ll fastPwr(int a, int k);

int main(void) {
  cout << fastPwr(9, 999) << endl;
  return 0;
}

ll fastPwr(int a, int k) {
  ll ans = 1;
  while (k) {
    if ((k & 0b1) == 0b1) {
      ans = ans * a;
    }
    a *= a;
    k >>= 1;
  }
  return ans;
}
