import sys
import env
import interp

def unittest():
    expr = "(do\
                (def (F x)\
                    (if (= x 0)\
                   
                        1\
                        (* x (F (- x 1)))\
                    ))\
                (F 5))"
    print(interp.interp(interp.parser(expr)))

if __name__ == '__main__':
    unittest()