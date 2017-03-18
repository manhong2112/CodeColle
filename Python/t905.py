from math import pow

def main():
    a = int(input())
    b = 1
    for i in range(1, 11):
        print(b)
        b *= a

    for i in range(0, 10):
        print(pow(a, i))

main()