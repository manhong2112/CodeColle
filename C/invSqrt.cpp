#include <stdio.h>
#include <iostream>

double Q_rsqrt(double number);

int main(void) {
  std::cout << Q_rsqrt(100);
}

double Q_rsqrt(double number) {
  long i;
  double x2, y;
  const double threehalfs = 1.5;

  x2 = number * 0.5;
  y  = number;
  i  = *(long*) &y;
  i  = 0x5fe6ec85e7de30daL - (i >> 1);
  y  = *(double*) &i;
  y  = y * (threehalfs - (x2 * y * y));
  y  = y * (threehalfs - (x2 * y * y));
  y  = y * (threehalfs - (x2 * y * y));
  return y;
}
