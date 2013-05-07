/*****
*   Range Minimum Query using segment trees
*   This code must be correct
******/


func min(a:int , b:int)
    begin
        if a < b then 
            return a
        else 
            return b
    end

func ST_init(data:int[100],tree:int[404],node:int, a:int, b:int)
    left:int;
    c:int;
    begin
        if (a == b) then
            begin
                tree[node] := data[a]
            end
        else
            begin
                ST_init(data, tree, node*2 , a, (a+b)/2);
                ST_init(data, tree, (node*2)+1, ((a+b)/2)+1, b);
                tree[node] := min(tree[node*2],tree[(node*2)+1])
            end
    end


func ST_query(tree:int[404], node:int, a:int, b:int, i:int, j:int):int
    left:int;
    right:int;
    mid:int;
    begin
        left := (a+b)/2;
        right := left + 1;
        return right
    end

func main()
    a:int;
    i:int;
    q:int;
    from:int;
    to:int;
    data:int[100];
    tree:int[404];
    begin
        read(a);
        i := 0;
        while( a > 0) do
            begin
               read(data[i]);
               i := i - 1;
               a := a - 1
            end;
        
        ST_init(data, tree, 1, 0 ,i - 1);

        read(q);

        while(q != 0) do
            begin
                read(from);
                read(to);
                write( ST_query(tree,1,0,i - 1,from,to) );
                read(q)
            end

    end


