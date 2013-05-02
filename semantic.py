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
        self.childrens = []
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


    #Busca si un cambo se ha definido varias veces
    def find_repeated(self, name):
        if self.table.has_key[name]:
            raise Semantic_error('Identifier was declared multiple times')
        else:
            if self.parent != None:
                self.parent.find_repeated(name)


    def add_children(self, children):
        self.childrens.append(children)

    def find_children(self, name):
        #Toca buscar -a mano- porque compara por nombre
        for children in self.childrens:
            if children.name == name
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

    def visit_program(self,program):
        for function in program.func_list.functions:
            self.generate_talbe_function(function)

        if not(self.main):
            raise Semantic_error('Function main was not found')

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
