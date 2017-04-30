import Searching;
public class SearchingTest

{

    public static void main(String[] args)

    {

        int[] numbers={12,16,23,36,45,59,61,78,82,96};

        System.out.print("the numbers are:");

        for(int i=0;i<numbers.length;i++)

        {

            System.out.print(numbers[i]+"  ");

        }

        int a=Searching.brSearch(numbers,78,0,numbers.length);

        System.out.println();

        System.out.println("78 is No."+a);

    }   

}
