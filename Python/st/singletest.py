import sys
import env
import interp

def unittest():
    expr =  "x"
    print(interp.interp(interp.parser(expr)))

if __name__ == '__main__':
    unittest()