public class q06 {
    public static void main(String[] args) {
        int a = 30, b = 90;
        int x = a, y = b;
        int tmp = 0;
        while(b != 0) {
            tmp = b;
            b = a % b;
            a = tmp;
        }
        System.out.println(a);
        System.out.print(x*y/a);
    }
}