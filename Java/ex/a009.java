import java.util.Scanner;
public class main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        char[] str;
        while(input.hasNext()) {
            str = input.nextLine().toCharArray();
            for(char i:str) {
                System.out.print((char) (((int) i) - 7));
            }
            System.out.println();
        }
    }
}