class a(object):
    a = {"b": 1}

    def b(self, c):
        self.a["b"] = c

    def reset(self):
        self.a = {}


class b(a):
    def b(self):
        super().b(10)


ia = a()
ib = b()

ia.b(12)
ib.b()
print(ia.a, hex(id(ia.a)))
print(ib.a, hex(id(ib.a)))

ia.reset()
ib.reset()

ia.b(12)
ib.b()
print(ia.a, hex(id(ia.a)))
print(ib.a, hex(id(ib.a)))
