

#ifdef _MSC_VER
   #define msvc 1
#else
   #define msvc 0
#endif

#ifdef __clang__
   #define clang 1
#else
   #define clang 0
#endif
int main(void) {
  if(msvc) {
     puts("msvc");
  }
  if(clang) {
     puts("clang");
  }
}
