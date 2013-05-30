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

class SSAVisitor(mpasast.NodeVisitor):
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

	def new_temp(self,return_type):
		'''
		Crea una nueva variable temporal de un tipo dado.
		'''
		name = "__%s_%d" % (return_type, self.versions[return_type])
		self.versions[typeobj.name] += 1
		return name
	#visit definitions start here
	
	def visit_Var_Dec(self, node):
	    # localice en memoria
		inst = ('alloc_'+node.return_type, 
		        node.id)
		self.code.append(inst)
		#se borro el resto pq nosotros en var_dec solo alocamos memoria no mas
	    
	    
	def visit_Type(self):
	    pass
	    
    def visit_Assignation(self, node):
        self.visit(node.value)		
		inst = ('store_'+node.value.return_type, node.value.gen_location, node.ubication)
		self.code.append(inst)
        
    def visit_Print(self, node):
        # Visit la expresion print
		self.visit(node.value)

		# Cree el opcode y agregarlo a la lista
		inst = ('print_'+node.value.return_type, node.value.gen_location)
		self.code.append(inst)
        
        
    def visit_Write(self):
        pass
        
    def visit_Ubication(self):
        pass          
		
	def visit_Binary_op(self):
	    # Visita las expresiones izquierda y derecha
		self.visit(node.left)
		self.visit(node.right)

		# Crea un nuevo temporal para almacenar el resultado
		target = self.new_temp(node.return_type)

		# Crea opcode y agrega a la lista
		opcode = binary_ops[node.op] + "_"+node.left.return_type
		inst = (opcode, node.left.gen_location, node.right.gen_location, target)
		self.code.append(inst)

		# Almacena localizacion del resultado en el nodo
		node.gen_location = target
	    
	    
    def visit_Unary_op(self, node):
        self.visit(node.value)
		target = self.new_temp(node.return_type)
		opcode = unary_ops[node.op] + "_" + node.value.return_type
		inst = (opcode, node.value.gen_location)
		self.code.append(inst)
		node.gen_location = target
    
    def visit_Id(self):
        pass
        
    def visit_Integer(self, node):        
        inst = ('literal_integer', node.value, target)
        self.code.append(inst)
                
    def visit_Float(self):
        inst = ('literal_integer', node.value, target)
        self.code.append(inst)
             
		
		
