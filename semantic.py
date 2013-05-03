import mpasparse
import mpaslex
import mpasast
import errors


class Data:

    def __init__ (self,name, _class, _type, info = None):
        self.name = name
        self._class = _class
        self._type = _type
        self.info = info

class Table:
    
    def __init__ (self, name, parent, _type):
        self.name =  name;
        self.table = {}
        self.children = []
        self.parent = parent
        self._type = _type

    class Semantic_error:        
        def __init(self, message):
            print(message)
            self.message = message

    def add(self, n_data, message = ""):
        if self.table.has_key[n_data.name]:
            raise Semantic_error('Identifier redefined: '+ n_data.name + message)
        self.table[n_data.name] = n_data

    def find(self,name):
        if self.table.has_key[name]:
            return self.table[name]
        else:
            if self.parent != None:
                return self.parent.find(name)
            raise Semantic_error('Identifier was not declared: '+ name)


    #Busca si un campo se ha definido varias veces
    def find_repeated(self, name):
        if self.table.has_key[name]:
            raise Semantic_error('Identifier was declared multiple times')
        else:
            if self.parent != None:
                self.parent.find_repeated(name)


    def add_child(self, child):
        self.children.append(child)

    def find_child(self, name):
        #Toca buscar -a mano- porque compara por nombre
        for child in self.children:
            if child.name == name
                return children
        raise Semantic_error('Indentifier was not declared: '+ name)

    #funciones redefinidas

    def find_function_repeated(self, function):
        if self.table.has_key[function.name]:
            possible = self.table[function.name]
                if possible._class != 'function' or possible._type != function._type or len(function.info) != len(possible.info):
                    raise Semantic_error('Function '+function.name+' was previously declared, return type or args does not match')
                
                for args1,args2 in zip (function.info, possible.info):
                    if args1._type != args2._type:
                        raise Semantic_error('Function previously decladred. Args declared erroneously for function: '+ function.name)

        elif self.parent != None:
            self.parent.find_function_repeated(function)


class SemanticVisitor(NodeVisitor):
   
    def __init_(self,node):
        self.main_t = Table('Main_t',None,'program')
        self.actual_t = self.main_t
        self.acutal_fun = None
        self.in_while = False
        self.main = False

    # Cambio la palabra node en todos para recordar que atributos tengo
    def visit_Program(self,program):
        for function in program.func_list.functions:
            self.generate_talbe_function(function)

        if not(self.main):
            raise Semantic_error('Function main was not found')
            

    #podria llamarse visit_Function y llamar el metodo visit para que vaya a los hijos
    def generate_table_function(self,function): 
        function_t = Data(function.id,'function',function.type, function.arglist)
        self.actual_t.find_function_repeated(function_t)
        temporal_table = self.actual_t
 
        for field in function.arglist:
            temporal_table.add(Data(field.id , 'variable',field.typename),' , Agument redefined in function : ' + function_t.name)
        
        if function.id == 'main'
            if self.main:
                raise Semantic_error('The program must have a only one main function')

        #add locals
        #
        # Acá se debe crear otra tabla que contiene el scope de las variables para la funcion
        #
        for local in function.locals:
            local.visit(self)

        #llama para que de aqui en adelante los datos necesarios esten calculados
        visit_Block(function.block)

        p_return_type = None
        for statement in function.block:
            if p_return_type == None:
                p_return_type = statement.return_type
            else:
                if p_return_type != statement.return_type:
                    raise Semantic_error('Function has different return types')

        if function.type == None:
            function.type = p_return_type
        else:
            if p_return_type == None:
                raise Semantic_error('Function must have at least one return')
            if p_return_type != function.type:
                raise Semantic_error('Function return does not matches with definition')

        #si pasa todas las verificaciones, añado la nueva tabla
        self.actual_t = temporal_table

         
    def visit_Var_dec(self, var_dec): #no se si es necesario
        self.actual_t.find_repeated(var_dec.id)
        self.actual_t.add(Data(var_dec.id,'variable',var_dec.type ))


    def visit_Block(self,block):
        for statement in block:
            statement.visit(self)
        # en este punto, todos los statements deberían tener un valor asociado al return_typei
        # falta verificar y agregar un return_type al bloque


    
    def visit_Vector(self, node): #no se si es necesario, se puede sacar de Var_dec, pero en todo caso 
        pass 
        
    def visit_While(self, _while):
        _while.conditional.visit(self)
        if not(_while.conditional.type == 'integer'): ## se puede comparar con._class por si hay problemas
            raise Semantic_error('Conditional in while is not correct, function: '+ self.actual_fun.name)
        _while.then.visit(self)
        _while.return_type = _while.then.return_type
        
    def visit_Assignation(self, node): #necesario
        pass 
        
    def visit_Print(self, node): #necesario 
        pass 
        
    def visit_Write(self, node): #necesario
        pass  
    
    def visit_Read(self, node): #necesario
        pass            
        
    def visit_Return(self, ret):
        if self.actual_fun.return_type != ret.return_type:
            raise Semantic_error('Invalid return type in method : '+ self.actual_fun.name)
        
    def visit_Call_func(self, node): #necesario
        pass
        
    def visit_Break(self, node): #necesario
        pass
        
    def visit_Ifthen(self, ifthen):
        ifthen.conditional.visit(self)
        if not(ifthen.conditional.type == 'integer'):
            raise Semantic_error('Conditional in if is not correct, function: ' + self.actual_fun.name)
        ifthen.then.visit(self)
        ifthen.return_type = ifthen.then.return_type

    
    def visit_Ifthenelse(self, node): #necesario
        pass
        
    def visit_Dec_list(self, node):# no se si es necesario
        pass
        
    def visit_Ubication(self, node): #no se si es necesario
        pass    
        
    def visit_Ubication_vector(self, node): #necesario
        pass  
        
    def visit_Binary_op(self, node):
        pass
        
    def Unary_op(self, node):
        pass
        
    def visit_Cast_int(self, node):
        pass
        
    def visit_Cast_float(self, node):
        pass 
        
    def visit_Expr_list(self, node): # no se si es necesario
        pass
        
    def visit_Else(self, node):
        pass
        
    def visit_Position(self, node): # no se si es necesario
        pass
        
    def visit_Condition(self, node): 
        pass
        
    def visit_Then(self, node):
        pass
        
    def visit_Read(self, node):
        pass                        
    # de aqui pa abajo no se                                                               
    

    def visit_Locals(self,node):
        pass

    def visit_While(self,node):
        pass

    def visit_Call_func(self,node):
        pass

    def visit_Ifthen(self,node):
        pass


    def visit_Ifthenelse(self,node):
        pass

