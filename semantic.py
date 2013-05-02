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

    def add(self, n_data):
        if self.table.has_key[n_data.name]:
            raise Semantic_error('Identifier redefined: '+ n_data.name)
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
    #Si vamos a hacer un visitante cada tipo de visita tiene que llamar a visit
    #para recorrer a los hijos, ud con quien vio estructuras?
    #en general su puede usar el metodo generico para las listas (Func_list, Dec_list) y especificos para
    #los nodos concretos

    def __init_(self,node):
        self.main_t = Table('Main_t',None,'program')
        self.actual_t = self.main_t
        self.acutal_fun = None
        self.in_while = False
        self.main = False
        
     #funcion que llama al método correcto de acuerdo al nodo ver visitante mpasast       
    def visit(self, node):
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.visit)
            newname= visitor(node)     
                      


    # Cambio la palabra node en todos para recordar que atributos tengo
    # Hay que llamar a visit
    def visit_Program(self,program):
        for function in program.func_list.functions:
            self.generate_talbe_function(function)

        if not(self.main):
            raise Semantic_error('Function main was not found')
            
    #debe ir primero visit_func_list que le puede mandar cada funcion a generate_table_function
    #o simplemente definir ese generate cono visit_Function y llamar a visit haciendo este
    #metodo inutil
    def visit_Func_list(self, node):
        pass
    
    #podria llamarse visit_Function y llamar el metodo visit para que vaya a los hijos
    def generate_table_function(self,function): 
        function_t = Data(function.id,'function',function.type, function.arglist)
        self.actual_t.find_function_repeated(function_t)
        temporal_table = self.actual_t
        #TODO: verificar si los argumentos están repetidos e.g foo(hola: int, hola:int)
        for field in function.arglist:
            temporal_table.add(Data(field.id , 'variable',field.typename))
        
        if function.id == 'main'
            if self.main:
                raise Semantic_error('The program must have a only one main function')

        #add locals

        #llama para que de aqui en adelante los datos necesarios esten calculados
        function.block.visit(self)

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

    #visita argumentos, no hay necesidad de visita para Empty_arguments     
    def visit_Arguments(self, node):
        pass  
        
    def visit_Local_var(self, node): #no se si sea necesario, mas bien solo visitar Var_dec??
        pass
        
    def visit_Local_fun(self, node): #pasarselo a generate_table_function o visit_Function... no?
        pass
        
    def visit_Var_dec(self, node): #no se si es necesario
        pass
    
    def visit_Vector(self, node): #no se si es necesario, se puede sacar de Var_dec, pero en todo caso 
        pass 
        
    def visit_While(self, node): #necesario
        pass
        
    def visit_Assignation(self, node): #necesario
        pass 
        
    def visit_Print(self, node): #necesario 
        pass 
        
    def visit_Write(self, node): #necesario
        pass  
    
    def visit_Read(self, node): #necesario
        pass            
        
    def visit_Return(self, node): #necesario
        pass
        
    def visit_Call_func(self, node): #necesario
        pass
        
    def visit_Break(self, node): #necesario
        pass
        
    def visit_Ifthen(self, node): #necesario
        pass
    
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
    
    def visit_Block(self,block):
        temporal_table = self.actual_t
        self.actual_t = Table('',self.actual_t,'block')
        temporal_table.add_children(self.actual_t)
        block.table = self.actual_t #ojo aca


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

