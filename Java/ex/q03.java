public class q03 {
    public static void main(String[] args) {
        int s = 100;
        int e = 999;
        for(int i = s;i<e;i++) {
            char[] x = ("" + i).toCharArray();
            int a = ((int) x[0]) -48, b = ((int) x[1]) - 48, c = ((int) x[2])-48;
            if(a*a*a+b*b*b+c*c*c==i) {
                System.out.println(i);
            }
        }
    }
}