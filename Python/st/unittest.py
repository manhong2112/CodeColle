import traceback
import sys
import env
import interp

def unittest():
    """Simple Unit Test"""
    data = ["(print 1)", None,
            "(do (+ 1 3) (+ 1 1))", 2,
            "(do (+ 1 2 3 4 5 6 7 8 9 10))", 55,
            "(+(+ 1                1)1)", 3,
            "(do (def x 1) x)", 1,
            "(do (def x (do (def x 2) (print x) 1)) x)", 1,
            "((lambda (x) x) 1)", 1,
            "((lambda (x) ((lambda (x) x) x)) ((lambda (x) x) 1))", 1,
            "(do (def x (lambda () 1)) (x))", 1,
            "((lambda () 1))", 1,
            "(((lambda (x) (lambda (y) (+ x y))) 1) 2)", 3,
            "(= 1 1)", True,
            "(= 1 2)", False,
            "(if #t 1 2)", 1,
            "(do (def (f x) x) (f 1))", 1,
            "(do\
                (def x 1)\
                (def f (lambda () x))\
                (def f2 (lambda (x) (f)))\
                (f2 2))", 1, # 雖然 pass 了...但何苦為難自己呢.._(:3」∠)_
            "(do\
                (def x 1)\
                (def f (lambda () x))\
                (def f2 (lambda (x) (f)))\
                (def x 3)\
                (f2 2))", 3, # 和預想的一樣, 重新綁定會改變閉包
            "(do\
                (def F (lambda (x)\
                    (if (= x 0)\
                        1\
                        (* x (F (- x 1)))\
                    )\
                )) (F 5))", 120, # 遞歸成功, 耶比~
            "(do\
                (def Y (lambda (f) \
                            ((lambda (u) (u u))\
                                (lambda (g)\
                                (f (lambda (x) ((g g) x)))))))\
                ((Y (lambda (f)\
                        (lambda (x)\
                            (if (= x 0)\
                                1\
                                (* x (f (- x 1)))))))\
                    5))", 120] # Y算子遞歸
    env0 = env.Env()
    env.init_env(env0)
    for i in range(0, len(data), 2):
        try:
            res = interp.interp0(interp.parser(data[i]), env0, None)[0]
        except Exception:
            print(f"Exception at Test{int(i/2)}")
            traceback.print_exception(*sys.exc_info())
            continue
        if res == data[i + 1]:
            print(f"Test{int(i/2)} Passed")
        else:
            print(f"Test{int(i/2)} Failed, Expected '{data[i + 1]}' but got '{res}'")
    print(len(env0.env)) # 64 orz

if __name__ == '__main__':
    unittest()