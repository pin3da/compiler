func binary_search(arr:int[100],val:int)
    lo:int;
    hi:int;
    mid:int;
    begin
        lo := 0;
        hi := 100;
        while(lo<hi) do
            begin
                mid := (lo+hi)/2;
                if(arr[mid] > val) then
                    hi := mid;
                if(arr[mid] < val) then
                    lo := mid +1;
                if(arr[mid]==val) then
                    return 1
            end;
         return 0
    end

func main()
    arr:int[100];
    lll:float;
    ans:int;
    begin
        ans := binary_search(arr,int(val))
    end
