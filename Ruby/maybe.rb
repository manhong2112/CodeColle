require_relative "record"

data("Maybe", record("Just", :a), record("Nothing"))

Maybe.impl(Eq) do
   def ==(x, y)
      p "my =="
      x.is_a?(Just) && y.is_a?(Just) && (x.a == y.a) ||
         x.is_a?(Nothing) && y.is_a?(Nothing)
   end
end

x = Just(1)
y = Just(2)
z = Just(1)

p x == y
p x == z
p x != y
p x != z
