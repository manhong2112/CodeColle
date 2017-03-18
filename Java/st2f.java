public class st2f {
  public static void main(String[] args) {
    System.out.println(st2f("1.100"));
  }
  static double st2f(String str) {
    String str_split[] = str.split("\\.");
    return Integer.valueOf(str_split[0]) + (Integer.valueOf(str_split[1])/Math.pow(10,str_split[1].length()));
  }
  static int val(String str) {
    char str_chararray = str.toChar();
  }
}