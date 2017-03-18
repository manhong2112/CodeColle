public class q04 {
    public static void main(String[] args) {
        int c = 90;
        StringBuilder result = new StringBuilder();
        for(int i = 2;i<=c;i++) {
            if(c % i == 0) {
                c /= i;
                result.append(i);
                result.append("*");
            }
        }
        if(c != 1) {
            result.append(c);
        } else {
            result.append("\b");
        }
        System.out.println(result.toString());
    }
}