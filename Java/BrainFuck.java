import java.util.Scanner;
import java.util.Stack;
public class BrainFuck {
  public static void main(String... args) {
    String hello = "--->->->>+>+>>+[++++[>+++[>++++>-->+++<<<-]<-]<+++]>>>.>-->-.>..+>++++>+++.+>-->[>-.<<]";
    Interp.exec(hello);
  }
}
class Interp {
  public static void exec(String str) {
    byte[] ram = new byte[65536];
    short ptr = 0;
    Stack<Integer> loopStack = new Stack<Integer>();
    int excapingLoopCount = 0;
    for(int i = 0;i < str.length();i++) {
      switch(str.charAt(i)) {
        case '[':
          if(excapingLoopCount > 0) {
            excapingLoopCount += 1;
          }
          else if(ram[ptr] != 0) {
            loopStack.push(i);
          }
          else{
            excapingLoopCount = 1;
          }
          break;
        case ']':
          if(excapingLoopCount > 0) {
            excapingLoopCount -= 1;
          }
          else if(ram[ptr] != 0) {
            i = loopStack.peek();
          }
          else {
            loopStack.pop();
          }
          break;
        case '+':
          ram[ptr] += 1;
          break;
        case '-':
          ram[ptr] -= 1;
          break;
        case '>':
          ptr += 1;
          break;
        case '<':
          ptr -= 1;
          break;
        case ',':
          Scanner reader = new Scanner(System.in);
          ram[ptr] += (char) reader.next().charAt(0);
          break;
        case '.':
          System.out.print((char) ram[ptr]);
          break;
      }
    }
  }
}