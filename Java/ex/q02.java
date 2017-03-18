public class q02 {
    public static void main(String[] args) {
        int s = 101;
        int e = 200;
        int c = 0;
        for(int i = s;i<=e;i += 2) {
            boolean isPrime = true;
            for(int j = 3;j < Math.sqrt(i);j += 2) {
                if(i % j == 0) {
                    isPrime = false;
                    break;
                }
            }
            if(isPrime) {
                System.out.println(i);
                c++;
            }
        }
        System.out.println(c);

    }
}