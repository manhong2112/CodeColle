for i in range(1, 1001): print("", end=str(i) + "\n" if i % 3 == 2 and i % 5 == 2 and i % 7 == 2 else "")

for i in range(1, 1001):
    if i % 3 == 2:
        if i % 5 == 2:
            if i % 7 == 2:
                print(i)

print('\n'.join(str(i) for i in range(1, 1001) if i % 3 == 2 and i % 5 == 2 and i % 7 == 2))

