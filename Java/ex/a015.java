import java.util.*;

public class a015 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String[] str = input.nextLine().split(" ");
        int x = Integer.valueOf(str[0]);
        int y = Integer.valueOf(str[1]);
        int count = 0;
        int[][] arr = new int[y][x];
        while(input.hasNext()) {
          str = input.nextLine().split(" ");
          for(int i = 0;i < str.length;i++) {
              arr[i][count] = Integer.valueOf(str[i]);
          }
          count += 1;
          if(count == x) {
            for(int[] i:arr) {
                for(int j:i) {
                    System.out.print(j + " ");
                }
                System.out.println();
            }
            if(input.hasNext()) {
                str = input.nextLine().split(" ");
                x = Integer.valueOf(str[0]);
                y = Integer.valueOf(str[1]);
                arr = new int[y][x];
                count = 0;
            }
          }
        }
    }

}