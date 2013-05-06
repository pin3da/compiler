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
            error(0,'Function main was not found',filename=sys.argv[1])
            

    #podria llamarse visit_Function y llamar el metodo visit para que vaya a los hijos
    def generate_table_function(self,function): 
        function_t = Data(function.id,'function',function.type, function.arglist)
        is_repeated = self.actual_t.find_function_repeated(function_t)
        if is_repeated == 2:
            error(function.lineno,"The function was previously declared but the argument's type doesn't match ", filename=sys.argv[1] )
        elif is_repeated == 1:
            error(function.lineno,"The funcion was previously declared, neither return type nor argument's size matches",filename=sys.argv[1] )
        elif is_repeated == 3:
            error(function.lineno, "The function was previously declared", filename=sys.argv[1])

        temporal_table = Table('fun_'+function.id , self.actual_t , 'function')

        
        self.actual_t.add_child(temporal_table)        
        self.actual_t = temporal_table
        self.actual_fun = function_t 
        
        ids = []
        for field in function.arglist.variables:
            if field.id in ids:
                error(function.lineno, 'Argument '+ field.id+' was declared more than once', filename=sys.argv[1])
            ids.append(field.id)
            self.actual_t.add(Data(field.id , 'variable',field.typename),' , Agument redefined in function : ' + function_t.name)
        
        if function.id == 'main':
            if self.main:
                error(function.lineno, 'The program must have a only one main function', filename=sys.argv[1])
            else:
                self.main = True

        for local in function.locals.local_var:
            self.visit(local)
            

        #llama para que de aqui en adelante los datos necesarios esten calculados
        self.visit_Block(function.block)

        
        p_return_type = None
        for statement in function.block:
        
            if(statement.return_type[1]): #means is a return istruction or wrap someone
                if p_return_type == None:
                    p_return_type = statement.return_type[0]
                elif p_return_type != statement.return_type[0]:
                    error(statement.lineno , 'Function has different return types', filename = sys.argv[1])

        if function.type == None:
            function.type = p_return_type
        else:
            if p_return_type == None:
                error(function.lineno,'Function must have at least one return', filename = sys.argv[1])
            if p_return_type != function.type:
                error(function.lineno, 'Function return does not matches with definition',filename = sys.argv[1] )
        

        # return -The control- to program table
        self.actual_t = self.actual_t.parent


    def visit_Var_dec(self, var_dec): #no se si es necesario
        if self.actual_t.find_repeated(var_dec.id):
            raise Semantic_error('Identifier was declared multiple times in this scope: '+ var_dec.id + 'line: '+ var_dec.lineno)
        self.actual_t.add(Data(var_dec.id,'variable',var_dec.typename ))


    def visit_Block(self,block):
        p_type = None
        for statement in block.declarations_list:
            self.visit(statement)
            if p_type == None:
                p_type = statement.return_type
            elif p_type != statement.return_type and statement.return_type != None:
                raise Semantic_error('The function can not have different return types: '+ self.actual_fun)

    
   
        
    def visit_While(self, _while):
        self.visit(_while.conditional)
        if not(_while.conditional.type == 'integer'): ## se puede comparar con._class por si hay problemas
            raise Semantic_error('Conditional in while is not correct, function: '+ self.actual_fun.name)
        self.visit(_while.then)
        _while.return_type = _while.then.return_type
        
    def visit_Assignation(self, node): #necesario
        if(node):
            var=self.actual_t.find(node.ubication.value)
            if not(var):
                raise Semantic_error('Identifier in assignation not found' + self.actual_fun.name)
            else:
                self.visit(node.value)                  
                if var._type!=node.value.return_type:
                    #print 'Incompatible types in function: ' + self.actual_fun.name + ' line: ',.lineno
                    raise Semantic_error('Incompatible types in function: ' + self.actual_fun.name)
        
        
    def visit_Print(self, node): #necesario
        if(node):
            if(node.value.return_type!=String_type):#???
                raise Semantic_error('Argument for Print must be a String in function' + self.actual_fun.name)                
        
        
    def visit_Write(self, node): #necesario
        if(node):
            if not(self.actual_t.find(node.value)):
                raise Semantic_error('Identifier not found in function' + self.actual_fun.name)
        
    
    def visit_Read(self, node): #necesario
        if(node):
            if not(self.actual_t.find(node.value)):
                raise Semantic_error('Identifier not found in function' + self.actual_fun.name)
                 
        
    def visit_Return(self, ret):
        if(node):
            self.visit(ret.value)
            if(self.actual_fun._type==None):
                self.actual_fun._type=ret.value.return_type
            else:
                if(ret.value.return_type!=self.actual_fun._type):
                    raise Semantic_error('Conflicting Return Types in Function' + self.actual_fun.name)
                    
            
        
        
    def visit_Call_func(self, node):
        pass
        
   
        
    def visit_Ifthen(self, ifthen):
        self.visit(ifthen.conditional)
        if not(ifthen.conditional.type == 'integer'):
            raise Semantic_error('Conditional in if is not correct, function: ' + self.actual_fun.name)
        self.visit(ithen.then)
        ifthen.return_type = ifthen.then.return_type

    
    def visit_Ifthenelse(self, _if):
        self.visit(_if.conditional)
        if not (_if.conditional.type == 'integer'):
            raise Semantic_error('Conditional in if is not correct, function: ' + self.actual_fun.name)
        self.visit(_if.then)
        #TODO: cambiar else por _else en el AST
        self.visit(_if._else)
        if _if.then.return_type != _if._else.return_type:
            raise Semantic_error('Return type does not matches between then and else blocks, function: '+self.actual_fun.name)
     
    ##   
    #def visit_Dec_list(self, node):# no se si es necesario
    #   pass
    ###
    # No es necesario, porque es la lista de statements y se llama en el for de block
    ##
        
        
    
    def visit_Then(self, _then):
        if type(_then.declaration) == list:
            p_return_type = None
            for statement in _then.declaration:
                self.visit(statement)
                if p_return_type == None:
                    p_return_type = statement.return_type
                elif p_return_type != statement.return_type and statement.return_type != None:
                    raise Semantic_error('Statments of then in function: '+ self.actual_fun.name + ' has no same return type')
        else:
            self.visit(_then.declaration)
            _then.return_type = _then.declaration.return_type
            
        
        
    def visit_Ubication_vector(self, node): #necesario
        pass  
        
    def visit_Binary_op(self, node):
        if(node):
            self.visit(node.left)
            self.visit(node.right)
            if(node.left.return_type != node.right.return_type):
                raise Semantic_error('Incompatible types in operation, in function' + self.actual_fun.name) 
            else:
               node.return_type=node.left.return_type               
       
        
    def Unary_op(self, node):
        pass
        
    def visit_Cast_int(self, node):
        if (node):
            visit(node.value)
            if(node.value.return_type != Float_type):#deberiamos tener todo esto en una rchivo que angle mando (Float_type, String_type)
                raise Semantic_error('Must be a float to convert to integer, in function' + self.actual_fun.name)
            node.return_type = Int_type    
       
        
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
        
    def visit_Position(self, node): # no se si es necesario
        pass
        
    def visit_Condition(self, node):
             
        pass




def check_program(root):
	checker = SemanticVisitor()
	checker.visit(root)

def main():
    import mpasparse
    import sys
    from errors import subscribe_errors
    lexer = mpaslex.make_lexer()
    parser = mpasparse.make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())
        check_program(program)

if __name__ == '__main__':
    main()