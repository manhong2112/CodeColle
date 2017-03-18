import java.util.*;

public class a013 {
    public static String[][] conventMap = {
            {"M", "1000"},
            {"CM", "900"},
            {"D", "500"},
            {"CD", "400"},
            {"C", "100"},
            {"XC", "90"},
            {"L", "50"},
            {"XL", "40"},
            {"X", "10"},
            {"IX", "9"},
            {"V", "5"},
            {"IV", "4"},
            {"I", "1"}
        };

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String[] str;
        int x;
        while(input.hasNext()) {
          str = input.nextLine().split(" ");
          if(str[0].equals("#")) {
              break;
          }
          if(str[0].equals(str[1])) {
              System.out.println("ZERO");
              continue;
          }
          x = Math.abs(toInt(str[0]) - toInt(str[1]));
          System.out.println(toRoman(x));
        }
    }

    public static int toInt(String str) {
        int keyId = 0, result = 0;
        String key = conventMap[keyId][0];
        while(true) {
            if(str.matches("^" + key + ".*")) {
                str = str.substring(key.length());
                result += Integer.valueOf(conventMap[keyId][1]);
            } else {
                keyId += 1;
                if(keyId >= conventMap.length) {
                    return result;
                }
                key = conventMap[keyId][0];
            }
        }
    }

    public static String toRoman(int value) {
        int keyId = 0;
        int key = Integer.valueOf(conventMap[keyId][1]);
        StringBuilder result = new StringBuilder();
        while(true) {
            if(value >= key) {
                value -= key;
                result.append(conventMap[keyId][0]);
            } else {
                keyId += 1;
                if(keyId >= conventMap.length) {
                    return result.toString();
                }
                key = Integer.valueOf(conventMap[keyId][1]);
            }
        }
    }

}