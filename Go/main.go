package main

import (
	"fmt"
	"math/rand"
  "time"
)

func main() {
  quiz := "あかさたなはまやらわいきしちにひみりうくすつぬふむゆるんえけせてねへめれおこそとのほもよろを"
  ans := "a kasatanahamayarawai kisitinihimiriu kusutunufumuyurun e kesetenehemereo kosotonohomoyorowo"
  rand.Seed(time.Now().UnixNano())
	for {
    i := rand.Intn(46) + 1
    fmt.Println(string([]rune(quiz)[i-1]))
    input_ans := ""
    fmt.Scanln(&input_ans)
    if input_ans == string(ans[2 * (i-1)]) + string(ans[2 * i-1]) || (len(input_ans) == 1 && input_ans == string(ans[2 * (i-1)])) {
      fmt.Println("Correct!")
    } else {
      fmt.Printf("Wrong, the answer is %s%s\n",string(ans[2 * (i-1)]),string(ans[2 * i-1]))
    }
  }
}
