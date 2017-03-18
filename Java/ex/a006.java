import java.util.Scanner;
public class a006 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String[] str;
        int a, b, c, delta, x1, x2;
        while(input.hasNext()) {
            str = input.nextLine().split(" ");
            a = Integer.valueOf(str[0]);
            b = Integer.valueOf(str[1]);
            c = Integer.valueOf(str[2]);
            delta = (int) Math.pow(b,2) - 4 * a *c;
            if(delta < 0) {
                System.out.println("No real root");
            }
            x1 = (int) (-b + Math.sqrt(delta)) / (2 * a);
            if(delta == 0) {
                System.out.println("Two same roots x=" + x1);
            } else if(delta > 0){
                x2 = (int) (-b - Math.sqrt(delta)) / (2 * a);
                System.out.println("Two different roots x1=" + x1 + " , x2=" + x2);
            }
        }
    }
}