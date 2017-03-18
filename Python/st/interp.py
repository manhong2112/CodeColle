# parser str to list
def parser(s):
    def _f(index):
        result = []
        t = ""
        while True:
            if s[index] == "(":
                x, index = _f(index + 1)
                result.append(x)
            c = s[index]
            if c == ")":
                if t != "":
                    result.append(t)
                return result, index + 1
            elif c == " ":
                if t != "":
                    result.append(t)
                    t = ""
            else:
                t += c
            index += 1
    return _f(1)[0]

print("(+ 1 2 3 4 (- 1 2 3 4 5) (+(+(+))))")