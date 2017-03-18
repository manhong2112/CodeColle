import java.util.*;
public class a520 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int num;
        while(input.hasNext()) {
            num = Integer.valueOf(input.nextLine());
            for(int i :fn(num)) {
                System.out.println(i);
            }
        }
  }

    private static Integer[] fn(int num) {
        if(num <= 0) return new Integer[]{};
        if(num == 1) return new Integer[]{1};
        int[] intArray = new int[num];
        int n = fn2(num);
        int j = 0;
        int temp;
        Integer[] result = new Integer[n];
        for(int i = 0;i < num;i++) {
            intArray[num - 1 - i] = i + 1;
        }
        for(int i = 0;i < n;i++) {
            if(j == num) {
                j = 0;
            }
            result[i] = arr2int(intArray);
            temp = intArray[(j + 1) >= num?0:j + 1];
            intArray[(j + 1) >= num?0:j + 1] = intArray[j];
            intArray[j] = temp;
            j++;
        }
        Arrays.sort(result, Collections.reverseOrder());
        return result;
    }

    private static int fn2(int num) {
        int a = 1;
        for (int y = 1; y <= num; y++) {
            a *= y;
        }
        return a;
    }

    private static int arr2int(int[] arr) {
        int l = arr.length;
        int result = 0;
        for(int i = 0;i < l;i++) {
            result += arr[i] * Math.pow(10, l - i - 1);
        }
        return result;
    }
}