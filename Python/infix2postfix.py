precedence = {
    "+": 0,
    "-": 0,
    "*": 1,
    "/": 1
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
        if(expr[i] == "("):
            x = infix2postfix(expr, i + 1)
            result += x[0]
            i = x[1]
        elif(expr[i] == ")"):
            result += "".join(stack[::-1])
            return result, i
        else:
            if len(stack) != 0 and precedence[expr[i]] < precedence[stack[-1]]:
                result += stack.pop()
            stack.append(expr[i])
        i += 1
    result.extend(stack[::-1])
    return result, i
