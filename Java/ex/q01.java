public class q01 {
    public static void main(String[] args) {
        int m = 12;
        for(int i = 0, j = 1, c = 0;c <= m;c++) {
            int tmp = i;
            i = j;
            j = tmp + i;
            System.out.printf("%d: %d\n", c, i*2);
        }
    }
}