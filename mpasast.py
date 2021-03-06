# mpasast.py
# -*- coding: utf-8 -*-
import pydot
'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
árbol de sintaxis abstracto.  Durante el análisis sintático, se debe 
crear estos nodos y conectarlos.  En general, usted tendrá diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deberá
añadir más.
'''

# NO MODIFICAR
class AST(object):
    '''
    Clase base para todos los nodos del AST.  Cada nodo se espera 
    definir el atributo _fields el cual enumera los nombres de los
    atributos almacenados.  El método a continuación __init__() toma
    argumentos posicionales y los asigna a los campos apropiados.
    Cualquier argumento adicional especificado como keywords son 
    también asignados.
    '''
    _fields = []
    def __init__(self,*args,**kwargs):
        ####
        # Agrego return type en todos los nodos, si es None, no tiene retorno (funciones)
        # Agrego lineno para manejo de errores, -1 para saber en que nodo falta agregarla, no se inicializa con kwargs porque genera problemas con _leaf
        self.return_type = None
        self.lineno = -1
        self.gen_location= None
        self.hasReturn = None
        #
        ####
        assert len(args) == len(self._fields)
        for name,value in zip(self._fields,args):
            setattr(self,name,value)
        # Asigna argumentos adicionales (keywords) si se suministran
        if(len(kwargs)!=0):
            for name,value in kwargs.items():
                setattr(self,name,value)
        else:
            setattr(self,"_leaf",False)

    def pprint(self):
        for depth, node in flatten(self):
            print("%s%s" % (" "*(4*depth),node))

    def graphprint(self,name):
        dotty=DotVisitor()
        dotty.visit(self)
        dotty.graph.write_png(name) 

def validate_fields(**fields):
    def validator(cls):
        old_init = cls.__init__
        def __init__(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            for field,expected_type in fields.items():
                assert isinstance(getattr(self, field), expected_type)
        cls.__init__ = __init__
        return cls
    return validator

# ----------------------------------------------------------------------
# Nodos AST especificos
#
# Para cada nodo es necesario definir una clase y añadir la especificación
# del apropiado _fields = [] que indique que campos deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresión izquierda y derecha, como esto:
# 
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Unos pocos nodos ejemplos



class Program(AST):
    _fields = ['func_list']

@validate_fields(functions=list)
class Func_list(AST):
    _fields = ['functions']

    def append(self,e):
        self.functions.append(e)

class Function(AST):
    _fields = ['id', 'arglist','type', 'locals', 'block']
    def append(self,e):
        self.functions.append(e)

class Empty_arguments(AST):
    _fields = ['arguments', 'empty']

@validate_fields(variables=list)
class Arguments(AST):
    _fields = ['variables']

    def append(self,e):
        self.variables.append(e)        

class Arguments_error(AST):
    _fields = ['error']

class Empty_locals(AST):
    _fields = ['arguments','empty']
        
@validate_fields(local_var=list)
class Local_var(AST):
    _fields = ['local_var']
    
    def append(self,e):
        self.local_var.append(e)

@validate_fields(local_fun=list)
class Local_fun(AST):
    _fields = ['local_fun']

    def append(self,e):
        self.local_fun.append(e)

    
class Error_locals_def(AST):
    _fields = ['error']                
                
class Var_dec(AST):
    _fields = ['id', 'typename']        

class Type(AST):
    _fields = ['value']

class Vector(AST):
    _fields = ['type', 'length']

class While(AST):
    _fields =['conditional', 'then']

class Assignation(AST):
    _fields = ['ubication', 'value']

class Print(AST):
    _fields = ['value']

class Write(AST):
    _fields = ['value']

class Read(AST):
    _fields = ['var_id']

class Return(AST):
    _fields = ['value']

class Call_func(AST):
    _fields = ['func_id', 'varlist']

class Skip(AST):
    _fields=['value']

class Break(AST):
    _fields=['value']

class Ifthen(AST):
    _fields =['conditional', 'then']

class Ifthenelse(AST):
    _fields =['conditional', 'then', '_else']
    
@validate_fields(declarations_list = list)
class Dec_list(AST):
    _fields = ['declarations_list']
    def append(self,e):
        self.declarations_list.append(e)
        
class Ubication(AST):
    _fields = ['value']


class Ubication_vector(AST):
    _fields = ['id', 'Position']

class Binary_op(AST):
    _fields = ['op', 'left', 'right']        

class Unary_op(AST):
    _fields = ['op', 'value']

class Id(AST):
    _fields = ['value'] 

class Cast_int(AST):
    _fields = ['value']

class Cast_float(AST):
    _fields = ['value']

class Empty_expr_list(AST):
    _fields = []

class Expression_list(AST):
    _fields = ['expr']

    def append(self,e):
        self.expr.append(e)


class Integer(AST):
    _fields=['value']

class Float(AST):
    _fields=['value']

class Else(AST):
    _fields =['statement']


class Position(AST):
    _fields = ['expr']

class Condition(AST):
    _fields = ['relation']

class Then(AST):
    _fields = ['declaration']
        
class Read(AST):
    _fields = ['var_id']
        
class Empty(AST):
    _fields = []


# Usted deberá añadir mas nodos aquí.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration, 
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
    '''
    Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
    de una clase similar en la librería estándar ast.NodeVisitor.  Para
    cada nodo, el método visit(node) llama un método visit_NodeName(node)
    el cual debe ser implementado en la subclase.  El método genérico
    generic_visit() es llamado para todos los nodos donde no hay coincidencia
    con el método visit_NodeName().
    
    Es es un ejemplo de un visitante que examina operadores binarios:

        class VisitOps(NodeVisitor):
            visit_Binop(self,node):
                print("Operador binario", node.op)
                self.visit(node.left)
                self.visit(node.right)
            visit_Unaryop(self,node):
                print("Operador unario", node.op)
                self.visit(node.expr)

        tree = parse(txt)
        VisitOps().visit(tree)
    '''
    def visit(self,node):
        '''
        Ejecuta un método de la forma visit_NodeName(node) donde
        NodeName es el nombre de la clase de un nodo particular.
        '''
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None
    
    def generic_visit(self,node):
        '''
        Método ejecutado si no se encuentra médodo aplicable visit_.
        Este examina el nodo para ver si tiene _fields, es una lista,
        o puede ser recorrido completamente.
        '''
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)

# NO MODIFICAR
class NodeTransformer(NodeVisitor):
    '''
    Clase que permite que los nodos del arbol de sintraxis sean 
    reemplazados/reescritos.  Esto es determinado por el valor retornado
    de varias funciones visit_().  Si el valor retornado es None, un
    nodo es borrado. Si se retorna otro valor, reemplaza el nodo
    original.
    
    El uso principal de esta clase es en el código que deseamos aplicar
    transformaciones al arbol de sintaxis.  Por ejemplo, ciertas optimizaciones
    del compilador o ciertas reescrituras de pasos anteriores a la generación
    de código.
    '''
    def generic_visit(self,node):
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value,list):
                newvalues = []
                for item in value:
                    if isinstance(item,AST):
                        newnode = self.visit(item)
                        if newnode is not None:
                            newvalues.append(newnode)
                    else:
                        newvalues.append(n)
                value[:] = newvalues
            elif isinstance(value,AST):
                newnode = self.visit(value)
                if newnode is None:
                    delattr(node,field)
                else:
                    setattr(node,field,newnode)
        return node

# NO MODIFICAR
def flatten(top):
    '''
    Aplana el arbol de sintaxis dentro de una lista para efectos
    de depuración y pruebas.  Este retorna una lista de tuplas de
    la forma (depth, node) donde depth es un entero representando
    la profundidad del arból de sintaxis y node es un node AST
    asociado.
    '''
    class Flattener(NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.nodes = []
        def generic_visit(self,node):
            self.nodes.append((self.depth,node))
            self.depth += 1
            NodeVisitor.generic_visit(self,node)
            self.depth -= 1

    d = Flattener()
    d.visit(top)
    return d.nodes



class DotVisitor():
    graph = None
    def __init__(self):
        self.graph = pydot.Dot('AST', graph_type='digraph')
        self.id=0
    def ID(self):
        self.id+=1
        return self.id
        #return "n%d" %self.id
    
    def visit (self, node):
        if node:
            if(node._leaf):
                newname=self.visit_leaf(node)
            else:
                method = 'visit_' + node.__class__.__name__
                visitor = getattr(self, method, self.visit_non_leaf)
                newname= visitor(node)        
        
        self.graph.add_node(newname)
        return newname
    
    
    def visit_color(self,node,node_name,node_id,color):
        string= "N%d %s ( %s )" % (self.ID(), node_name, node_id)
        name=pydot.Node(string,shape='box3d', style="filled", fillcolor=color)
        for i in xrange (1,len(node._fields)):
            if (not isinstance(getattr(node,node._fields[i]) , list) ):
                newname=self.visit(getattr(node,node._fields[i]))
                self.graph.add_edge(pydot.Edge(name, newname))
            else:
                for foo in getattr(node,node._fields[i]):
                    if isinstance(foo,AST):
                        newname = self.visit(foo)
                        self.graph.add_edge(pydot.Edge(name, newname))
        return name
    
    
    def visit_Function(self, node):
        return self.visit_color(node,"Function",node.id,"#666999")

    def visit_Binary_op(self,node):
        return self.visit_color(node,"Bin Oper ",node.op,"#884221")

    def visit_Call_func(self, node):
        return self.visit_color(node,"Call",node.func_id,"#FFFFFF")        

    def visit_non_leaf(self,node):
        string= "N%d %s" % (self.ID(), node.__class__.__name__)
        name=pydot.Node(string,shape='box3d', style="filled", fillcolor="#0066ff")
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)           
            if isinstance(value,list):
                for item in value:
                    if isinstance(item,AST):
                        newname = self.visit(item)
                        self.graph.add_edge(pydot.Edge(name, newname))
                        
                                                      
            elif isinstance(value,AST):
                newname = self.visit(value)
                self.graph.add_edge(pydot.Edge(name, newname))
        return name
                
               
        

    def visit_leaf(self, node):
        string = "L%d %s ( %s )" % (self.ID(), node.__class__.__name__, node.value)
        return pydot.Node(string, shape='box3d',style="filled", fillcolor="#9ACD32")

