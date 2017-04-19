priority = {
    "+": 0,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2
}


def to_postfix(expr, start=0):
    stack = []
    result = []
    buffer = ""
    i = start
    while i < len(expr):
        if expr[i].isalpha() or expr[i].isdigit():
            if expr[i].isdigit():
                buffer += expr[i]
            else:
                result.append(expr[i])
            i += 1
            continue
        if buffer != "":
            result.append(buffer)
            buffer = ""
        if expr[i] == "(":
            x = to_postfix(expr, i + 1)
            result += x[0]
            i = x[1]
        elif expr[i] == ")":
            result += "".join(stack[::-1])
            return result, i
        else:
            if stack and priority[expr[i]] <= priority[stack[-1]]:
                result += stack.pop()
            stack.append(expr[i])
        i += 1
    if buffer:
        stack.append(buffer)
    result.extend(stack[::-1])
    return result, i

def calc(lst):
    stack = []
    for i in lst:
        if i == "+":
            stack.append(stack.pop() + stack.pop())
        elif i == "-":
            stack.append(stack.pop() - stack.pop())
        elif i == "*":
            stack.append(stack.pop() * stack.pop())
        elif i == "/":
            x = stack.pop()
            y = stack.pop()
            stack.append(x // y)
        elif i == "%":
            stack.append(stack.pop() % stack.pop())
        else:
            stack.append(int(i))
    return stack.pop()

import sys
for s in sys.stdin:
    print(calc(to_postfix(s.strip().replace(" ", ""))[0]))

