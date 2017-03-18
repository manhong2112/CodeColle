Y = (lambda F: ((lambda u: u(u))(lambda f: F(lambda v: f(f)(v)))))
Y(lambda f: (lambda x: 1 if x <= 2 else f(x - 1) + f(x - 1)))(5)
Y(lambda f: (lambda x: 1 if x == 0 else x * f(x - 1)))(5)

TRUE = lambda t, f: t
FALSE = lambda t, f: f
IF = lambda b, t, f: b(t, f)
AND = lambda b1, b2: IF(b1, b2, FALSE)
OR = lambda b1, b2: IF(b1, TRUE, b2)
NOT = lambda b: IF(b, FALSE, TRUE)
