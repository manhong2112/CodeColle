fun :: Int -> [Int]
fun 0 = 1
fun n = n * fun (n - 1)
main :: IO ()
main = do
    print (fun 5)