import sys
import env
import interp

def unittest():
    expr = """(do
                (def (gcd a b)
                    (if (= b 0)
                        a
                    (gcd b (% a b))))
                (gcd 4 8))"""
    print(interp.interp(interp.parser(expr)))

if __name__ == '__main__':
    unittest()