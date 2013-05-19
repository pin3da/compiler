from mpasparse import *
from mpaslex import *
from mpasast import *
from errors import *

class Data:

    def __init__ (self,name, _class, _type, info = None):
        self.name = name
        self._class = _class
        self._type = _type
        self.info = info

class Semantic_error:        
    def __init__(self, message):
        print message 
        self.message = message

class Table:
    
    def __init__ (self, name, parent, _type):
        self.name =  name;
        self.table = {}
        self.children = []
        self.parent = parent
        self._type = _type



    def add(self, n_data, message = ""):
        if n_data.name in self.table:
            return False
        self.table[n_data.name] = n_data
        return True

    def find(self,name):
        if name in self.table:
            return self.table[name]
        else:
            if self.parent != None:
                return self.parent.find(name)

        return None


    #Busca si un campo se ha definido varias veces
    def find_repeated(self, name):
        if name in self.table:
            return True
        else:
            if self.parent != None:
                self.parent.find_repeated(name)
        return False


    def add_child(self, child):
        self.children.append(child)

    def find_child(self, name):
        #Toca buscar -a mano- porque compara por nombre
        for child in self.children:
            if child.name == name:
                return children
        return None

    #funciones redefinidas
    

    ######
    #   Return 1 if the function was previously declared but the return or the len of arguments doesn't matches
    #   Return 2 if the len of the arguments matches but each not
    #   Return 3 if the function was previously declared, arguments doesn't matters
    #   Return 0 if is not found (not repeated)
    ######
    def find_function_repeated(self, function):
        if function.name in self.table:
            possible = self.table[function.name]
            if possible._class != 'function' or possible._type != function._type or len(function.info) != len(possible.info): 
                return 1
                
            for args1,args2 in zip (function.info, possible.info):
                if args1._type != args2._type:
                     return 2


            return 3

        elif self.parent != None:
            self.parent.find_function_repeated(function)

        return 0


class SemanticVisitor(NodeVisitor):
   
    def __init__(self):
        self.main_t = Table('Main_t',None,'program')
        self.actual_t = self.main_t
        self.actual_fun = None
        self.in_while = False
        self.main = False

    # Cambio la palabra node en todos para recordar que atributos tengo
    def visit_Program(self,program):
        for function in program.func_list.functions:
            self.generate_table_function(function)

        if not (self.main) :
            error(0,'Warning: Function main was not found',filename=sys.argv[1])
            #exit()            

    def visit_Function(self,fun):
        self.generate_table_function(fun)

    #podria llamarse visit_Function y llamar el metodo visit para que vaya a los hijos
    def generate_table_function(self,function):
        temporal_table = Table('fun_'+function.id , self.actual_t , 'function')
        self.actual_t.add_child(temporal_table)        
        self.actual_t = temporal_table
        self.visit(function.arglist)
        function_parent = self.actual_fun 
        _arguments = []
        if function.arglist.__class__.__name__ != 'Empty_arguments':
            for ar in function.arglist.variables:
                _arguments.append(ar)
                
        function_t = Data(function.id,'function',function.type, _arguments)
        is_repeated = self.actual_t.find_function_repeated(function_t)
        if is_repeated == 2:
            error(function.lineno,"The function was previously declared but the argument's type doesn't match ", filename=sys.argv[1] )
            exit()
        elif is_repeated == 1:
            error(function.lineno,"The funcion was previously declared, neither return type nor argument's size matches",filename=sys.argv[1] )
            exit()
        elif is_repeated == 3:
            error(function.lineno, "The function was previously declared", filename=sys.argv[1])
            exit()
        
        self.actual_fun = function_t 

        if function.id == 'main':
            if self.main:
                error(function.lineno, 'The program must have a only one main function', filename=sys.argv[1])
                exit()
            else:
                self.main = True
        
        if not isinstance(function.locals , Empty_locals):
            if hasattr(function.locals,"local_var"):
                for local in function.locals.local_var:
                    self.visit(local)
            if hasattr(function.locals,"local_fun"):
                for local in function.locals.local_fun:
                    self.visit(local)

            

        #llama para que de aqui en adelante los datos necesarios esten calculados
        self.visit_Block(function.block)
       
        if(self.actual_fun._type != None):
            if not(function.block.hasReturn):
                error(function.lineno, 'The program must have at least one return on function: ' + function.id, filename=sys.argv[1])
                #exit()
        
        # return -The control- to program table

        if isinstance(function_t._type,Type):
            function_t._type = function_t._type.value
                
        self.actual_fun = function_parent
        self.actual_t = self.actual_t.parent
        self.actual_t.add(function_t)
       


    def visit_Var_dec(self, var_dec): 
        if self.actual_t.find(var_dec.id):
            error(var_dec.lineno, 'Warning: Redeclared Variable: '+ var_dec.id, filename=sys.argv[1])
            #exit()
            #pass
        else:
            self.visit(var_dec.typename)
            self.actual_t.add(Data(var_dec.id,'variable', var_dec.typename.return_type ))
            var_dec.return_type = var_dec.typename.return_type
            
    def visit_Assignation(self, assignation):
        self.visit(assignation.ubication)
        self.visit(assignation.value)
        
        p_var = self.actual_t.find(assignation.value.return_type)
        
        if not (p_var == None):
            assignation.value.return_type = p_var._type


        if assignation.ubication.return_type != assignation.value.return_type:
            #print 'Incompatible types in function: ' + self.actual_fun.name + ' line: ',.lineno
            error(assignation.lineno, 'Incompatible Types in assignation', filename=sys.argv[1])
            exit()

    def visit_Block(self,block):
        for statement in block.declarations_list:
            self.visit(statement)
            if(statement.hasReturn):
                block.hasReturn=True

    def visit_While(self, _while):
        self.visit(_while.conditional)
        if _while.conditional.return_type != 'integer' :
            error(_while.lineno , 'Conditional in while is not correct, function: '+ self.actual_fun.name ,filename=sys.argv[1] )
            exit()
        self.visit(_while.then)
        _while.hasReturn=_while.then.hasReturn
        _while.return_type = _while.then.return_type
        
    def visit_Print(self, _print):
        if(isinstance(_print.value, AST)):
            self.visit(_print.value)
            if _print.value.return_type != 'string':
                error(_print.lineno, 'Error, print must have a string type', filename=sys.argv[1])
                exit()
            _print.return_type = _print.value.return_type
        elif not(isinstance(_print.value, str)):
            error(_print.lineno, 'Error, print must have a string type', filename=sys.argv[1])    
    
    def visit_Write(self, write): 
        self.visit(write.value)
        write.return_type = write.value.return_type

    
    def visit_Read(self, read):
        self.visit(read.var_id)
        read.return_type = read.var_id.return_type
             
        
    def visit_Return(self, ret):
        self.visit(ret.value)
        
        ret.hasReturn=True
        if(self.actual_fun._type == None):
            self.actual_fun._type = ret.value.return_type
        else:
            if not (isinstance(self.actual_fun._type,str)):
                self.actual_fun._type = self.actual_fun._type.value 
            elif(ret.value.return_type != self.actual_fun._type): 
                error(ret.lineno, 'Error, return types do not match, in function: '+ self.actual_fun.name, filename=sys.argv[1])   
                exit()
        ret.return_type  = ret.value.return_type
        
        

    def visit_Ubication(self,ubication):
         foo = self.actual_t.find(ubication.value)
         if foo == None:
            error(ubication.lineno, 'Identifier not declared : '+ ubication.value, filename=sys.argv[1] )
            exit()
         ubication.return_type = foo._type


    def visit_Call_func(self, fun):
        act_fun = self.actual_t.find(fun.func_id)
        if (act_fun == None or act_fun._class != 'function') and fun.func_id != self.actual_fun.name:
            error(fun.lineno, 'Function not declared: '+ fun.func_id , filename=sys.argv[1] )
            exit()
        else:
            if(fun.func_id == self.actual_fun.name): #Porque a penas se esta visitando
                return     
            fun.return_type = act_fun._type    
        
        _arguments = []
        if fun.varlist.__class__.__name__ == 'Expression_list':
            for ar in fun.varlist.expr:
                _arguments.append(ar)
        
        if fun.varlist.__class__.__name__ != 'Empty_expr_list':
            if (act_fun.info.__class__.__name__ == 'Empty_expr_list' or len(_arguments) != len(act_fun.info) ):
                error(fun.lineno, "Arguments' length don't match 1: "+ fun.func_id , filename=sys.argv[1] )
                exit()
        else:
            
            if (act_fun.info.__class__.__name__ != 'Empty_expr_list'):
                error(fun.lineno, "Arguments' length don't match 2: "+ fun.func_id , filename=sys.argv[1] )
                exit()
        
        for (arg1, arg2) in zip (_arguments , act_fun.info):
            self.visit(arg1)
            #self.visit(arg2)
            if arg1.return_type != arg2.return_type:
                error(fun.lineno, "Arguments' types don't match: "+ fun.func_id , filename=sys.argv[1] )
                exit()
          
          
    def visit_Empty_arguments(self,node):
        pass
    
    def visit_Arguments(self,args):
        ids = []
        for field in args.variables:
            if field.id in ids:
                error(function.lineno, 'Argument '+ field.id+' was declared more than once', filename=sys.argv[1])
            ids.append(field.id)
            #self.actual_t.add(Data(field.id , 'variable',field.typename.value))
            self.visit(field)
            if( hasattr(field.typename,'value') ):
                field.return_type =  field.typename.value
            else:
                self.visit(field.typename)
                field.return_type  = field.typename.return_type
    
    def visit_Ifthen(self, ifthen):
        self.visit(ifthen.conditional)
        if not(ifthen.conditional.return_type == 'integer'):
            error(ifthen.lineno, 'Conditional in if is not correct, function: ' + self.actual_fun.name, filename=sys.argv[1] )
        self.visit(ifthen.then)
        ifthen.hasReturn=ifthen.then.hasReturn
        ifthen.return_type = ifthen.then.return_type

    
    def visit_Ifthenelse(self, _if):
        self.visit(_if.conditional)
        if (_if.conditional.return_type != 'integer'):
            error(_if.lineno, 'Conditional in if is not correct, function: ' + self.actual_fun.name, filename=sys.argv[1] )
        self.visit(_if.then)
        self.visit(_if._else)
        _if.hasReturn = _if.then.hasReturn or _if._else.hasReturn
        _if.return_type = _if.then.return_type

            
    def visit_Then(self, _then):
        if type(_then.declaration) == list:
            for statement in _then.declaration:
                self.visit(statement)
                if(statement.hasReturn):
                    _then.hasReturn = statement.hasReturn
        else:
            self.visit(_then.declaration)
            if(_then.declaration.hasReturn):
                _then.hasReturn = True
            _then.return_type = _then.declaration.return_type
            
        
    
    def visit_Binary_op(self, node):
        self.visit(node.left)
        self.visit(node.right)
        if(node.left.return_type != node.right.return_type):
            error(node.lineno,'Incompatible types in operation, in function: ' + self.actual_fun.name, filename=sys.argv[1] ) 
            exit()
        else:
            node.return_type = node.left.return_type
    
    def visit_Cast_int(self, node):
        self.visit(node.value)
        possible = ['float']
        if not (node.value.return_type in possible):#deberiamos tener todo esto en una rchivo que angle mando (Float_type, String_type)
            error(node.lineno, 'Must be a float to convert to integer, in function' + self.actual_fun.name, filename=sys.argv[1] )
        node.return_type = 'integer'
    
    #######
    
    def visit_Id(self,_id):
        p_id = self.actual_t.find(_id.value)
        if( p_id == None):
            error(_id.lineno, 'Variable not declared: '+ _id.value, filename=sys.argv[1] )
        else:
            _id.return_type =  p_id._type
        
    def visit_Ubication_vector(self, ubi_vector): 
        p_id =  self.actual_t.find(ubi_vector.id)
        if(p_id == None):
            error(ubi_vector.lineno, 'Vector not declared: '+ ubi_vector.id, filename=sys.argv[1] )
            exit()
        else:
            self.visit(ubi_vector.Position)
            if ubi_vector.Position.return_type != 'integer':
                error(ubi_vector.lineno, 'Index invalid, must be an integer: '+ ubi_vector.id, filename=sys.argv[1] )
                exit()

        ubi_vector.return_type = p_id._type


        
    def visit_Unary_op(self, node):
        self.visit(node.value)
        node.return_type = node.value.return_type
       
    def visit_Integer(self, node):
        node.return_type = 'integer'
     
    def visit_Float(self,node):
        node.return_type = 'float'
        
        
    def visit_Type(self,_type):
        _type.return_type =  _type.value
    
    ####
    # Preguntar acerca de indices negativos.Deberia ser en tiempo de ejecucion.
    # si es algo como X[a*b] ?
    ####
    def visit_Ubication_vector(self,ubication):
        var = self.actual_t.find(ubication.id)
        if(var == None):
            error(ubication.lineno,'Vector not declared', filename=sys.argv[1])
            exit()
        ubication.return_type = var._type[:-6]
        


    def visit_Vector(self,vector):
        vector.return_type = vector.type+"vector"
        self.visit(vector.length)
        if( vector.length.return_type != 'integer'):
            error(vector.lineno, 'Length of vector must be an integer',filename=sys.argv[1] )
            exit()
    
    def visit_Cast_float(self, node):
        if (node):
            visit(node.value)
            if(node.value.return_type != Int_type):#deberiamos tener todo esto en una rchivo que angle mando (Float_type, String_type)
                raise Semantic_error('Must be a an Integer to convert to float, in function' + self.actual_fun.name)
            node.return_type= Float_type    
        
        
    def visit_Expr_list(self, node): # no se si es necesario
        pass
        
    def visit_Else(self, node):
        pass
        
    def visit_Position(self, pos):
        self.visit(pos.expr)
        pos.return_type = pos.expr.return_type
        
    def visit_Condition(self, _condition):
        self.visit(_condition.relation)
        _condition.return_type =  _condition.relation.return_type
   
    def visit_Local_fun(self,_fun):
        self.visit(_fun.local_fun)
        _fun.return_type = _fun.local_fun.return_type


def check_program(root):
	checker = SemanticVisitor()
	checker.visit(root)

def main():
    import mpasparse
    import sys
    from errors import subscribe_errors
    lexer = mpaslex.make_lexer()
    parser = mpasparse.make_parser()
    with subscribe_errors(lambda msg: sys.stderr.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())
        check_program(program)

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print "usage: python semantic.py <path_to_file>"
        exit()
    main()
