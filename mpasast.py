# mpasast.py
# -*- coding: utf-8 -*-
'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
�rbol de sintaxis abstracto.  Durante el an�lisis sint�tico, se debe 
crear estos nodos y conectarlos.  En general, usted tendr� diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deber�
a�adir m�s.
'''

# NO MODIFICAR
class AST(object):
	'''
	Clase base para todos los nodos del AST.  Cada nodo se espera 
	definir el atributo _fields el cual enumera los nombres de los
	atributos almacenados.  El m�todo a continuaci�n __init__() toma
	argumentos posicionales y los asigna a los campos apropiados.
	Cualquier argumento adicional especificado como keywords son 
	tambi�n asignados.
	'''
	_fields = []
	def __init__(self,*args,**kwargs):
		assert len(args) == len(self._fields)
		for name,value in zip(self._fields,args):
			setattr(self,name,value)
		# Asigna argumentos adicionales (keywords) si se suministran
		for name,value in kwargs.items():
			setattr(self,name,value)

	def pprint(self):
		for depth, node in flatten(self):
			print("%s%s" % (" "*(4*depth),node))

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
# Para cada nodo es necesario definir una clase y a�adir la especificaci�n
# del apropiado _fields = [] que indique que campos deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresi�n izquierda y derecha, como esto:
# 
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Unos pocos nodos ejemplos

class PrintStatement(AST):
	'''
	print expression ;
	'''
	_fields = ['expr']

class Literal(AST):
	'''
	Un valor constante como 2, 2.5, o "dos"
	'''
	_fields = ['value']

class Program(AST):
	_fields = ['program']

@validate_fields(statements=list)
class Statements(AST):
	_fields = ['statements']

	def append(self,e):
		self.statements.append(e)
	
class Statement(AST):
	_fields = ['statement']

class Extern(AST):
	_fields = ['func_prototype']

class FuncPrototype(AST):
	_fields = ['id', 'params', 'typename']

@validate_fields(param_decls=list)
class Parameters(AST):
	_fields = ['param_decls']

	def append(self,e):
		self.param_decls.append(e)

class ParamDecl(AST):
	_fields = ['id', 'typename']

class AssignmentStatement(AST):
	_fields = ['location', 'value']

class ConstDeclaration(AST):
	_fields = ['id', 'value']

class VarDeclaration(AST):
	_fields = ['id', 'typename', 'value']

class IfStatement(AST):
	_fields = ['condition', 'then_b', 'else_b']

class WhileStatement(AST):
	_fields = ['condition', 'body']

class LoadLocation(AST):
	_fields = ['name']

class StoreVar(AST):
	_fields = ['name']

class UnaryOp(AST):
	_fields = ['op', 'left']

class BinaryOp(AST):
	_fields = ['op', 'left', 'right']

class RelationalOp(AST):
	_fields = ['op', 'left', 'right']
	
class Group(AST):
	_fields = ['expression']

class FunCall(AST):
	_fields = ['id', 'params']

class ExprList(AST):
	_fields = ['expressions']

	def append(self, e):
		self.expressions.append(e)

class Empty(AST):
	_fields = []


# Usted deber� a�adir mas nodos aqu�.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration, 
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el m�dulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
	'''
	Clase para visitar nodos del �rbol de sintaxis.  Se model� a partir
	de una clase similar en la librer�a est�ndar ast.NodeVisitor.  Para
	cada nodo, el m�todo visit(node) llama un m�todo visit_NodeName(node)
	el cual debe ser implementado en la subclase.  El m�todo gen�rico
	generic_visit() es llamado para todos los nodos donde no hay coincidencia
	con el m�todo visit_NodeName().
	
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
		Ejecuta un m�todo de la forma visit_NodeName(node) donde
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
		M�todo ejecutado si no se encuentra m�dodo aplicable visit_.
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
	
	El uso principal de esta clase es en el c�digo que deseamos aplicar
	transformaciones al arbol de sintaxis.  Por ejemplo, ciertas optimizaciones
	del compilador o ciertas reescrituras de pasos anteriores a la generaci�n
	de c�digo.
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
	de depuraci�n y pruebas.  Este retorna una lista de tuplas de
	la forma (depth, node) donde depth es un entero representando
	la profundidad del arb�l de sintaxis y node es un node AST
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
