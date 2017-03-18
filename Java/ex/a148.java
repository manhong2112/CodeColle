import java.util.*;
public class a148 {
  public static void main(String[] args) {
  	Scanner input = new Scanner(System.in);
    String[] str;
    double m;
    double n;
    double c;
    while(input.hasNext()) {
      str = input.nextLine().split(" ");
      n = Integer.valueOf(str[0]); // 100
      c = Integer.valueOf(str[1]); // 1000
      m = (Math.sqrt(Math.abs(8 * c + 4 * n * n - 4 * n + 1)) - 1) / 2 + 0.5;
      System.out.println(((int) m) - ((int) n) + 1);
    }
  }
}