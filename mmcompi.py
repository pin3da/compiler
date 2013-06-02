# mpascode.py
# -*- coding: utf-8 -*-

import mpasast
import mpasblock
from mpasblock import BasicBlock, IfBlock, WhileBlock
from collections import defaultdict

binary_ops = {
	'+' : 'add',
	'-' : 'sub',
	'*' : 'mul',
	'/' : 'div',
	'<' : 'lt',
	'>' : 'gt',
	'==': 'eq',
	'!=': 'ne',
	'<=': 'le',
	'>=': 'ge',
	'&&': 'land',
	'||': 'lor',
}

unary_ops = {
	'+' : 'uadd',
	'-' : 'usub',
	'!' : 'lnot',
}

class GenerateCode(mpasast.NodeVisitor):
	'''
	Clase Visitor Node que crea secuencias de instrucciones de 3-direcciones.
	'''
	def __init__(self):
		super(GenerateCode, self).__init__()

		# version diccionario para temporales
		self.versions = defaultdict(int)

		# El código generado (lista de tuplas)
		self.code = BasicBlock()
		self.start_block = self.code

		# Una lista de declaraciones externas (y tipos)
		self.externs = []

	def new_temp(self,typeobj):
		'''
		Crea una nueva variable temporal de un tipo dado.
		'''
		name = "__%s_%d" % (typeobj.name, self.versions[typeobj.name])
		self.versions[typeobj.name] += 1
		return name

	# Debe implementar métodos visit_Nodename para todos los demas nodos
	# del AST.  En su código, se tendrá que hacer las instrucciones y
	# agregarlas a la lista self.code.
	#
	# Siguen algunos métodos de ejemplo.  Deberá ajustarlos dependiendo
	# de los nombres de los nodos AST que se haya definido.

	def visit_Literal(self,node):
		# Crea un nuevo nombre de variable temporal
		target = self.new_temp(node.type)

		# Crea el opcode SSA y lo agrega a la lista de instrucciones generadas
		inst = ('literal_'+node.type.name, node.value, target)
		self.code.append(inst)

		# Graba el nombre de la variable temporal donde el valor fue colocado
		node.gen_location = target

	def visit_BinaryOp(self,node):
		# Visita las expresiones izquierda y derecha
		self.visit(node.left)
		self.visit(node.right)

		# Crea un nuevo temporal para almacenar el resultado
		target = self.new_temp(node.type)

		# Crea opcode y agrega a la lista
		opcode = binary_ops[node.op] + "_"+node.left.type.name
		inst = (opcode, node.left.gen_location, node.right.gen_location, target)
		self.code.append(inst)

		# Almacena localizacion del resultado en el nodo
		node.gen_location = target

	def visit_RelationalOp(self,node):
		# Visit las expresiones izquierda y derecha
		self.visit(node.left)
		self.visit(node.right)

		# Cree un temporal nuevo para almacer el resultado
		target = self.new_temp(node.type)

		# Cree el opcode y agregarlo a la lista
		#opcode = binary_ops[node.op] + "_"+node.left.type.name
		opcode = "cmp" + "_"+node.left.type.name
		inst = (opcode, binary_ops[node.op], node.left.gen_location, node.right.gen_location, target)
		self.code.append(inst)

		# Almacene localizacion del resultado al nodo
		node.gen_location = target

	def visit_PrintStatement(self,node):
		# Visit la expresion print
		self.visit(node.expr)

		# Cree el opcode y agregarlo a la lista
		inst = ('print_'+node.expr.type.name, node.expr.gen_location)
		self.code.append(inst)

	def visit_Program(self,node):
		self.visit(node.program)

	#def visit_Statements(self,node):
	#    self.visit(node.expr)
	#    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	#    self.code.append(inst)

	#def visit_Statement(self,node):
	#    self.visit(node.expr)
	#    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	#    self.code.append(inst)

	def visit_ConstDeclaration(self,node):
		# localice en memoria
		inst = ('alloc_'+node.type.name, 
		        node.id)
		self.code.append(inst)
		# almacene valor inicial
		self.visit(node.value)
		inst = ('store_'+node.type.name,
		        node.value.gen_location,
		        node.id)
		self.code.append(inst)

	def visit_VarDeclaration(self,node):
		# localice en memoria
		inst = ('alloc_'+node.type.name, 
		        node.id)
		self.code.append(inst)
		# almacene pot. val inicial
		if node.value:
		    self.visit(node.value)
		    inst = ('store_'+node.type.name,
		            node.value.gen_location,
		            node.id)
		    self.code.append(inst)

	def visit_LoadLocation(self,node):
		target = self.new_temp(node.type)
		inst = ('load_'+node.type.name,
		        node.name,
		        target)
		self.code.append(inst)
		node.gen_location = target

	#def visit_Extern(self,node):
	#    self.visit(node.expr)
	#    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	#    self.code.append(inst)

	#def visit_FuncPrototype(self,node):
	#    self.visit(node.expr)
	#    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	#    self.code.append(inst)

	#def visit_Parameters(self,node):
	#    self.visit(node.expr)
	#    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	#    self.code.append(inst)
	#    node.gen_location = target

	#def visit_ParamDecl(self,node):
	#    self.visit(node.expr)
	#    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	#    self.code.append(inst)

	def visit_AssignmentStatement(self,node):
		self.visit(node.value)
		
		inst = ('store_'+node.value.type.name, 
		        node.value.gen_location, 
		        node.location)
		self.code.append(inst)

	def visit_UnaryOp(self,node):
		self.visit(node.left)
		target = self.new_temp(node.type)
		opcode = unary_ops[node.op] + "_" + node.left.type.name
		inst = (opcode, node.left.gen_location)
		self.code.append(inst)
		node.gen_location = target

	def visit_IfStatement(self,node):
		if_block = IfBlock()
		self.code.next_block = if_block
		# condition
		self.switch_block(if_block)
		self.visit(node.condition)
		if_block.test = node.condition.gen_location
		# then branch
		if_block.if_branch = BasicBlock()
		self.switch_block(if_block.if_branch)
		self.visit(node.then_b)
		# else branch
		if node.else_b:
		    if_block.else_branch = BasicBlock()
		    self.switch_block(if_block.else_branch)
		    self.visit(node.else_b)
		# fija el siguiente bloque
		if_block.next_block = BasicBlock()
		self.switch_block(if_block.next_block)

	def visit_WhileStatement(self, node):
		while_block = WhileBlock()
		self.code.next_block = while_block
		# condition
		self.switch_block(while_block)
		self.visit(node.condition)
		while_block.test = node.condition.gen_location
		# body
		while_block.body = BasicBlock()
		self.switch_block(while_block.body)
		self.visit(node.body)
		while_block.next_block = BasicBlock()
		self.switch_block(while_block.next_block)

	def switch_block(self, next_block):
		self.code = next_block

	def visit_Group(self,node):
		self.visit(node.expression)
		node.gen_location = node.expression.gen_location

	#def visit_FunCall(self,node):
	#    self.visit(node.expr)
	#    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	#    self.code.append(inst)

	#def visit_ExprList(self,node):
	#    self.visit(node.expr)
	#    inst = ('print_'+node.expr.type.name, node.expr.gen_location)
	#    self.code.append(inst)


# STEP 3: Probar
# 
# Trate de correr este programa con un archivo adecuado para tal efecto y vea
# la secuencia del codigo SSA resultante.
#
#     bash % python mpascode.py good.pas
#     ... vea la salida ...
#
# ----------------------------------------------------------------------
#            NO MODIFIQUE NADA DE AQUI EN ADELANTE
# ----------------------------------------------------------------------
def generate_code(node):
	'''
	Genera código SSA desde el nodo AST entregado.
	'''
	gen = GenerateCode()
	gen.visit(node)
	return gen

if __name__ == '__main__':
	import mpaslex
	import mpasparse
	import mpascheck
	import sys
	from errors import subscribe_errors, errors_reported
	lexer = mpaslex.make_lexer()
	parser = mpasparse.make_parser()
	with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
		program = parser.parse(open(sys.argv[1]).read())
		# Revise el programa
		exprcheck.check_program(program)
		# Si no ocurre errore, genere código
		if not errors_reported():
			code = generate_code(program)
			# Emite la secuencia de código
			exprblock.PrintBlocks().visit(code.start_block)
			#for inst in code.code:
			#    print(inst)
