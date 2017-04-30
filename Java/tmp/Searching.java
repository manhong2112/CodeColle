public class Searching

{

public static int brSearch(int[] data,int target,int first,int last)

    {

        if(first<=last)

        {

            int mid=(first+last)/2;

            if(target==data[mid])

                return mid;

            else if(data[mid]>target)

                return brSearch(data,target,first,mid-1);

            else

                return brSearch(data,target,mid+1,last);

        }
        return -1;

    }

}