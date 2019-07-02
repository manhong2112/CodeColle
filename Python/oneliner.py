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
  pure(type("MutVar", (), {"__init__": (lambda self, v = None: setattr(self, "v", v))})) >> (lambda newVar:
  pure(lambda var: var.v) >> (lambda getVar:
  pure(lambda var, v: setattr(var, v)) >> (lambda putVar:
  pure()
))))))
)(type("pure", (), {"__init__": (lambda self, v = None: setattr(self, "v", v)), "__rshift__": (lambda self, f: type(self)(f(self.v).v))}))

assert res.v is None
