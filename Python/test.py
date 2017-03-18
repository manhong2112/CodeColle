import math


def radiationExposure(start, stop, step):
    r = 0
    while start < stop:
        x = 400 * math.e ** (math.log(0.5)/3.66 * start)
        if step < 1:
            start += start
            r += x * step
        elif step >= 1:
            start += step
            r += x 
    return r


def radiationExposure2(start, stop, step):
    if start == stop:
        return 0
    elif step < 1:
        return f(start) * step + radiationExposure(start + start, stop, step)
    elif step >= 1:
        return f(start) + radiationExposure(start + step, stop, step) 

def f(x):
    return 400*math.e**(math.log(0.5)/3.66 * x)

print(radiationExposure2(1, 100, -3))
print(radiationExposure(1, 100, -3))
