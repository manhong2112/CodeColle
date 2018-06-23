main :: IO ()
main = putStrLn $ show (T `and'` T)
data Boolean = T | F

instance Show Boolean where
   show T = "T"
   show F = "F"


and' :: Boolean -> Boolean -> Boolean
T `and'` T = T
_ `and'` _ = F
