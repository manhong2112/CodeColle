import java.lang.*;
import java.lang.Integer;
import java.lang.Override;
import java.lang.String;
import java.lang.System;
import java.util.Random;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.ConcurrentHashMap;

public class Test_random {
	public static void main(String[] args) {

		long time1, time2;
		time1 = System.currentTimeMillis();
		Random random = new Random();
		Map<Integer,Integer> map = new ConcurrentHashMap<Integer,Integer>();
		
		    for (int i = 0; i < 10000; i++) {
      int tmp = (int) (random.nextInt(10000) + 0.5);
      if (map.containsValue(tmp)) {
        i--;
        continue;
      }
      map.put(i, tmp);
    }

		time2 = System.currentTimeMillis();
		System.out.println((time2 - time1) + "ms");
	}
}