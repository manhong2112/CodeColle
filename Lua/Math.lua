Math = {
  gcd = function(x, y)
          while y ~= 0 do
            if x > y then
              x = x - y
            else
              y = y - x
            end
          end
          return x
        end,
  lcm = function(x, y)
          return x * y / Math.gcd(x, y)
        end,
  abs = function(x)
          if x < 0 then
            return -x
          else
            return x
          end
        end
}
Math.__index = Math
