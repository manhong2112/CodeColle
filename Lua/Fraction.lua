require("Class")
require("Math")

Fraction = class()
Fraction.constructor
("num", "num")
(function(self, x, y)
  local s = 0
  if x < 0 then
    s = 1
  end
  if y < 0 then
    s = s - 1
  end
  x = Math.abs(x)
  y = Math.abs(y)
  xy_gcd = Math.gcd(x, y)
  self[1] = ((s == 0) and 1) or -1
  self[2] = x / xy_gcd
  self[3] = y / xy_gcd
end)

Fraction.func("toString")() (
  function()
    return self[1] * self[2] .. "/" .. self[3]
  end
)
function Fraction.__add(f1, f2)
  l = Math.lcm(f1[3], f2[3])
  return new(Fraction)(f1[1] * f1[2] * l / f1[3] + f2[1] * f2[2] * l / f2[3], l)
end
function Fraction.__sub(f1, f2)
  l = Math.lcm(f1[3], f2[3])
  return new(Fraction)(f1[1] * f1[2] * l / f1[3] - f2[1] * f2[2] * l / f2[3], l)
end
function Fraction.__mul(f1, f2)
  return new(Fraction)(f1[1] * f2[1] * f1[2] * f2[2], f1[3] * f2[3])
end
function Fraction.__div(f1, f2)
  return new(Fraction)(f1[1] * f2[1] * f1[2] * f2[3], f2[2] * f1[3])
end
function Fraction.__eq(f1, f2)
  return f1[1] == f2[1] and f1[2] == f2[2] and f1[3] == f2[3]
end