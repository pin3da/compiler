/**
* Comentario Inicial
*/
func mf( a : int, b:int , c:float)
    begin
        a=10;
        b=10+5 
    end
/**
* Comentario final
*/

func otherfunc(a:int)
    begin
        if(a == 1) then
            return 1
        else
            return a + otherfunc(a-1)
    end
