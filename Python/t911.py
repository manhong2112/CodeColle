for i in range(1, 201):
    print("", end=str(i) + "\n" if str(i * i) == str(i * i)[::-1] else "")

for i in range(1, 201):
    a = list(str(i * i))
    b = list(str(i * i))
    a.reverse()
    if a == b:
        print(i)

print("\n".join(str(i) for i in range(1, 201) if str(i * i) == str(i * i)[::-1]))
