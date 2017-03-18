import random

pwd = ""

for i in range(0, 4): pwd += str(random.randint(0, 9))

print("Guess a number: ")
print("(", pwd, ")")
while True:
    guess = input()
    if len(guess) != 4:
        continue
    A, B = 0, 0
    for i in range(0, 4):
        B += guess[i] in pwd[i:4]
        A += guess[i] == pwd[i]

    print(A, "A", (B - A), "B", sep="")
    if A == 4:
        break

print("You Win!")
