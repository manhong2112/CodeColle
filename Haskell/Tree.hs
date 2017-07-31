data Tree a = Node a (Tree a) (Tree a)
            | Empty
              deriving (Show)

height :: Tree a -> Int
height Empty = 0
height (Node _ Empty x) = 1 + height x
height (Node _ x Empty) = 1 + height x
height (Node _ x y) = 1 + max (height x) (height y)
  