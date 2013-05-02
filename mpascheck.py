# mpascheck.py
# -*- coding: utf-8 -*-
'''
Proyecto 3 : Chequeo del Programa
=================================
En este proyecto es necesario realizar comprobaciones sem�nticas en su programa. 
Hay algunos aspectos diferentes para hacer esto.

En primer lugar, tendr� que definir una tabla de s�mbolos que haga un seguimiento
de declaraciones de identificadores previamente declarados.  Se consultar� la 
tabla de s�mbolos siempre que el compilador necesite buscar informaci�n sobre 
variables y declaraci�n de constantes.

A continuaci�n, tendr� que definir los objetos que representen los diferentes 
tipos de datos incorporados y registrar informaci�n acerca de sus capacidades.
Revise el archivo mpastype.py.

Por �ltimo, tendr� que escribir c�digo que camine por el AST y haga cumplir un
conjunto de reglas sem�nticas.  Aqu� est� una lista completa de todo los que
deber� comprobar:

1.  Nombres y s�mbolos:

    Todos los identificadores deben ser definidos antes de ser usados.  Esto incluye variables, 
    constantes y nombres de tipo.  Por ejemplo, esta clase de c�digo genera un error:
    
       a = 3;              // Error. 'a' no est� definido.
       var a int;

    Nota: los nombres de tipo como "int", "float" y "string" son nombres incorporados que
    deben ser definidos al comienzo de un programa (funci�n).
    
2.  Tipos de constantes

    A todos los s�mbolos constantes se le debe asignar un tipo como "int", "float" o "string".
    Por ejemplo:

       const a = 42;         // Tipo "int"
       const b = 4.2;        // Tipo "float"
       const c = "forty";    // Tipo "string"

    Para hacer esta asignaci�n, revise el tipo de Python del valor constante y adjunte el
    nombre de tipo apropiado.

3.  Chequeo de tipo operaci�n binaria.

    Operaciones binarias solamente operan sobre operandos del mismo tipo y produce un
    resultado del mismo tipo.  De lo contrario, se tiene un error de tipo.  Por ejemplo:

		var a int = 2;
		var b float = 3.14;

		var c int = a + 3;    // OK
		var d int = a + b;    // Error.  int + float
		var e int = b + 4.5;  // Error.  int = float

4.  Chequeo de tipo operador unario.

    Operadores unarios retornan un resultado que es del mismo tipo del operando.

5.  Operadores soportados

    Estos son los operadores soportados por cada tipo:

    int:      binario { +, -, *, /}, unario { +, -}
    float:    binario { +, -, *, /}, unario { +, -}
    string:   binario { + }, unario { }

    Los intentos de usar operadores no soportados deber�a dar lugar a un error.
    Por ejemplo:

		var string a = "Hello" + "World";     // OK
		var string b = "Hello" * "World";     // Error (op * no soportado)

6.  Asignaci�n.

    Los lados izquierdo y derecho de una operaci�n de asignaci�n deben ser 
    declarados del mismo tipo.

    Los valores s�lo se pueden asignar a las declaraciones de variables, no
    a constantes.

Para recorrer el AST, use la clase NodeVisitor definida en mpasast.py.
Un caparaz�n de c�digo se proporciona a continuaci�n.
'''

import sys, re, string, types
from errors import error
from mpasast import *
import mpastype
import mpaslex

class SymbolTable(object):
	'''
	Clase que representa una tabla de s�mbolos.  Debe proporcionar funcionabilidad
	para agregar y buscar nodos asociados con identificadores.
	'''
	
	class SymbolDefinedError(Exception):
		'''
		Exception disparada cuando el codigo trara de agragar un simbol 
		a la tabla de simbolos, y este ya esta definido
		'''
		pass
	
	class SymbolConflictError(Exception):
		'''
		'''
		pass
	
	def __init__(self, parent=None):
		'''
		Crea una tabla de simbolos vacia con la tabla padre dada
		'''
		self.symtab = {}
		self.parent = parent
		if self.parent != None:
			self.parent.children.append(self)
		self.children = []
		
	def add(self, a, v):
		'''
		Agrega un simbol con el valor dado a la tabla de simbolos
		
		func foo(x:int, y:int)
		x:float;
		
		'''
		if self.symtab.has_key[a]:
			if self.symtab[a].type.get_string() != v.type.get_string():
				raise SymbolTable.SymbolConflictError()
			else:
				raise SymbolTable.SymbolDefinedError()
		self.symtab[a] = v

	def lookup(self, a):
		if self.symtab.has_key(a):
			return self.symtab[a]
		else:
			if self.parent != None:
				return self.parent.lookup(a)
			else:
				return None

class CheckProgramVisitor(NodeVisitor):
	'''
	Clase de Revisi�n de programa.  Esta clase usa el patr�n cisitor como est�
	descrito en mpasast.py.  Es necesario definir m�todos de la forma visit_NodeName()
	para cada tipo de nodo del AST que se desee procesar.

	Nota: Usted tendr� que ajustar los nombres de los nodos del AST si ha elegido
	nombres diferentes.
	'''
	def __init__(self):
		# Inicializa la tabla de simbolos
		pass
		
	def push_symtab(self, node):
		self.current = SymbolTable(self.current)
		node.symtab = self.current
		
	def pop_symbol(self):
		self.current = self.current.parent

	def visit_Program(self,node):
	
		self.push_symtab(node)
		# Agrega nombre de tipos incorporados ((int, float, string) a la tabla de simbolos
		node.symtab.add("int",mpastype.int_type)
		node.symtab.add("float",mpastype.float_type)
		node.symtab.add("string",mpastype.string_type)
		node.symtab.add("bool",mpastype.boolean_type)

		# 1. Visita todas las declaraciones (statements)
		# 2. Registra la tabla de simbolos asociada
		self.visit(node.program)

	def visit_IfStatement(self, node):
		self.visit(node.condition)
		if not node.condition.type == mpastype.boolean_type:
			error(node.lineno, "Tipo incorrecto para condici�n if")
		else:
			self.visit(node.then_b)
			if node.else_b:
				self.visit(node.else_b)

	def visit_WhileStatement(self, node):
		self.visit(node.condition)
		if not node.condition.type == mpastype.boolean_type:
			error(node.lineno, "Tipo incorrecto para condici�n while")
		else:
			self.visit(node.body)

	def visit_UnaryOp(self, node):
		# 1. Aseg�rese que la operaci�n es compatible con el tipo
		# 2. Ajuste el tipo resultante al mismo del operando
		self.visit(node.left)
		if not mpaslex.operators[node.op] in node.left.type.un_ops:
			error(node.lineno, "Operaci�n no soportada con este tipo")
		self.type = node.left.type

	def visit_BinaryOp(self, node):
		# 1. Aseg�rese que los operandos left y right tienen el mismo tipo
		# 2. Aseg�rese que la operaci�n est� soportada
		# 3. Asigne el tipo resultante
		self.visit(node.left)
		self.visit(node.right)
		node.type = node.left.type

	def visit_AssignmentStatement(self,node):
		# 1. Aseg�rese que la localizaci�n de la asignaci�n est� definida
		sym = self.symtab.lookup(node.location)
		assert sym, "Asignado a un sym desconocido"
		# 2. Revise que la asignaci�n es permitida, pe. sym no es una constante
		# 3. Revise que los tipos coincidan.
		self.visit(node.value)
		assert sym.type == node.value.type, "Tipos no coinciden en asignaci�n"

	def visit_ConstDeclaration(self,node):
		# 1. Revise que el nombre de la constante no se ha definido
		if self.symtab.lookup(node.id):
			error(node.lineno, "S�mbol %s ya definido" % node.id)
		# 2. Agrege una entrada a la tabla de s�mbolos
		else:
			self.symtab.add(node.id, node)
		self.visit(node.value)
		node.type = node.value.type

	def visit_VarDeclaration(self,node):
		# 1. Revise que el nombre de la variable no se ha definido
		if self.symtab.lookup(node.id):
			error(node.lineno, "S�mbol %s ya definido" % node.id)
		# 2. Agrege la entrada a la tabla de s�mbolos
		else:
			self.symtab.add(node.id, node)
		# 2. Revise que el tipo de la expresi�n (si lo hay) es el mismo
		if node.value:
			self.visit(node.value)
			assert(node.typename == node.value.type.name)
		# 4. Si no hay expresi�n, establecer un valor inicial para el valor
		else:
			node.value = None
		node.type = self.symtab.lookup(node.typename)
		assert(node.type)

	def visit_Typename(self,node):
		# 1. Revisar que el nombre de tipo es v�lido que es actualmente un tipo
		pass

	def visit_Location(self,node):
		# 1. Revisar que la localizaci�n es una variable v�lida o un valor constante
		# 2. Asigne el tipo de la localizaci�n al nodo
		pass

	def visit_LoadLocation(self,node):
		# 1. Revisar que loa localizaci�n cargada es v�lida.
		# 2. Asignar el tipo apropiado
		sym = self.symtab.lookup(node.name)
		assert(sym)
		node.type = sym.type

	def visit_Literal(self,node):
		# Adjunte un tipo apropiado a la constante
		if isinstance(node.value, types.BooleanType):
			node.type = self.symtab.lookup("bool")
		elif isinstance(node.value, types.IntType):
			node.type = self.symtab.lookup("int")
		elif isinstance(node.value, types.FloatType):
			node.type = self.symtab.lookup("float")
		elif isinstance(node.value, types.StringTypes):
			node.type = self.symtab.lookup("string")

	def visit_PrintStatement(self, node):
		self.visit(node.expr)

	def visit_Extern(self, node):
		# obtener el tipo retornado
		# registe el nombre de la funci�n
		self.visit(node.func_prototype)

	def visit_FuncPrototype(self, node):
		print 'foooooo'
		if self.symtab.lookup(node.id):
			error(node.lineno, "S�mbol %s ya definido" % node.id)
		self.visit(node.params)
		node.type = self.symtab.lookup(node.typename)

	def visit_Parameters(self, node):
		for p in node.param_decls:
			self.visit(p)

	def visit_ParamDecl(self, node):
		node.type = self.symtab.lookup(node.typename)

	def visit_Group(self, node):
		self.visit(node.expression)
		node.type = node.expression.type

	def visit_RelationalOp(self, node):
		self.visit(node.left)
		self.visit(node.right)
		if not node.left.type == node.right.type:
			error(node.lineno, "Operandos de relaci�n no son del mismo tipo")
		elif not mpaslex.operators[node.op] in node.left.type.bin_ops:
			error(node.lineno, "Operaci�n no soportada con este tipo")
		node.type = self.symtab.lookup('bool')

	def visit_FunCall(self, node):
		pass
	def visit_ExprList(self, node):
		pass
	def visit_Empty(self, node):
		pass

# ----------------------------------------------------------------------
#                       NO MODIFICAR NADA DE LO DE ABAJO
# ----------------------------------------------------------------------

def check_program(node):
	'''
	Comprueba el programa suministrado (en forma de un AST)
	'''
	checker = CheckProgramVisitor()
	checker.visit(node)

def main():
	import mpasparse
	import sys
	from errors import subscribe_errors
	lexer = mpaslex.make_lexer()
	parser = mpasparse.make_parser()
	with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
		program = parser.parse(open(sys.argv[1]).read())
		# Revisa el programa
		check_program(program)

if __name__ == '__main__':
	main()
