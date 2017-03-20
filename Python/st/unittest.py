import traceback
import sys
import env
import interp

data = ["(print 1)", None,
        "(print x)", KeyError,
        "(print 'x')", None,
        "(print \"x\")", None,
        "(do (+ 1 3) (+ 1 1))", 2,
        "(do (+ 1 2 3 4 5 6 7 8 9 10))", 55,
        "(+(+ 1                1)1)", 3,
        "(do (def x 1) x)", 1,
        "(do (def x (do (def x 2) (print x) 1)) x)", 1,
        "((fn (x) x) 1)", 1,
        "((fn (x) ((fn (x) x) x)) ((fn (x) x) 1))", 1,
        "(do (def x (fn () 1)) (x))", 1,
        "((fn () 1))", 1,
        "(((fn (x) (fn (y) (+ x y))) 1) 2)", 3,
        "(= 1 1)", True,
        "(= 1 2)", False,
        "(if #t 1 2)", 1,
        "(do (def (f x) x) (f 1))", 1,
        "(do\
            (def x 1)\
            (def f (fn () x))\
            (def f2 (fn (x) (f)))\
            (f2 2))", 1, # 雖然 pass 了...但何苦為難自己呢.._(:3」∠)_
        "(do\
            (def x 1)\
            (def f (fn () x))\
            (def f2 (fn (x) (f)))\
            (def x 3)\
            (f2 2))", AssertionError, # 和預想的一樣, 重新綁定會改變閉包 ## 禁止重新綁定好還是當成feature好呢...
        "(do\
            (def F (fn (x)\
                (if (= x 0)\
                    1\
                    (* x (F (- x 1)))\
                )\
            )) (F 5))", 120, # 遞歸成功, 耶比~
        "(do\
            (def Y (fn (f) \
                        ((fn (u) (u u))\
                            (fn (g)\
                            (f (fn (x) ((g g) x)))))))\
            ((Y (fn (f)\
                    (fn (x)\
                        (if (= x 0)\
                            1\
                            (* x (f (- x 1)))))))\
                5))", 120, # Y算子遞歸 ## 試着在interp print了一下作用域, 只能說遞歸爆炸~
        "(let ([x 1] [y 1]) (+ x y))", 2,
        "(let ([x 2] [y x]) (+ x y))", 4,
        "(let ([x (let ([x (let ([x 1] [y 1]) (+ x y))]\
                        [y 1])\
                        (+ x y))]\
                [y x])\
                (+ x y))", 6, # 它說是6, 那就6吧, 誰會去手算這玩意... 反正隔壁Scheme也說是6
        "(do\
            (def (gcd a b)\
                (if (= b 0)\
                    a\
                (gcd b (% a b))))\
            (gcd 4 8)\
        )", 4,
        "_", KeyError]

test_list = []
def Test(fun):
    test_list.append((fun.__name__, fun))

@Test
def unittest1():
    """
    Simple Unit Test
    same env
    """
    env0 = env.Env()
    def _fun(e, y):
        return interp.interp0(interp.parser(y), e, None)[0]
    unittest(env.Env, _fun, data)

@Test
def unittest2():
    """
    Unit Test
    Individual Env
    """
    unittest(lambda: None, lambda _, y: interp.interp(interp.parser(y)), data)

@Test
def unittest_parser():
    """Parser Unit Test""" # 一改parser就出一堆bug了, 不加不行啊orz
    data = ["(+ 1 2)", ["+", "1", "2"], "_", "_"]
    unittest(lambda: None, lambda _, y: interp.parser(y), data)

def unittest(setup, fun, data):
    """UnitTest"""
    s = setup()
    for i in range(0, len(data), 2):
        try:
            res = fun(s, data[i])
        except Exception as e0:
            if isinstance(data[i + 1], type) and isinstance(e0, data[i + 1]):
                print(f"Test{int(i/2)} Passed")
            else:
                print(f"Exception at Test{int(i/2)}")
                traceback.print_exception(*sys.exc_info())
            continue
        if res == data[i + 1]:
            print(f"Test{int(i/2)} Passed")
        else:
            print(f"Test{int(i/2)} Failed, Expected '{data[i + 1]}' but got '{res}'")

def starttest():
    for i in range(0, len(test_list)):
        print("=" * 16)
        print(f"{test_list[i][0]}...")
        test_list[i][1]()
        print("=" * 16)


if __name__ == '__main__':
    starttest()
    