import sys
sys.setrecursionlimit(1500)
res = (lambda pure:
  pure(lambda f:
      (lambda x: f(lambda *n: x(x)(*n)))
      (lambda x: f(lambda *n: x(x)(*n)))) >> (lambda Y:
  pure(lambda b, t, f: t() if b else f()) >> (lambda _if:
  pure(Y(lambda _while: lambda boolean, block: _if(
         boolean,
         lambda: block() >> (lambda b: _while(b, block)),
         lambda: pure(None)
      )))>> (lambda _while:
  pure(__import__("random")) >> (lambda random:
  pure(random.randint(1, 100)) >> (lambda answer:
  _while(True,
    lambda:
      pure(int(input("Guess a number: "))) >> (lambda guess:
        _if(guess > answer,
          lambda: pure(print("Wrong, it is too big!")) >> (lambda _: pure(True)),
          lambda: _if(guess < answer,
            lambda: pure(print("Wrong, it is too small!")) >> (lambda _: pure(True)),
            lambda: pure(print("Correct!")) >> (lambda _: pure(False))
          )
        )
    )
  )
)
))))
)(type("pure", (), {"__init__": (lambda self, v = None: setattr(self, "v", v)), "__rshift__": (lambda self, f: type(self)(f(self.v).v))}))

print(res)
print(res.v)
