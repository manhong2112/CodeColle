def f(string, fmt):
    res = []
    buffer = ""
    for i in string:
        buffer += i
        if buffer in fmt:
            res.append(buffer)
            buffer = ""
        else:
            for j in range(len(buffer)):
                k = buffer[-j:]
                if k in fmt:
                    res.append(buffer[:len(buffer)-j])
                    res.append(k)
                    buffer = ""
    if buffer:
        res.append(buffer)
    res.append(-1)
    return res

f("var x := 1\n////var y := x", ["var", ":=", " ", "\n", "//"])
