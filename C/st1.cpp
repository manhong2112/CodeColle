#include <iostream>
#include <cmath>
int main() {
  int n = 0, i = 0;
  while(i < 1964) {
    n++;
    if(pow((int) sqrt(n), 2) != n) {
      i++;
    }
  }
  std::cout << n;
  return 0;
}
