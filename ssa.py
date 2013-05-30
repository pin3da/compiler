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

	def new_temp(self,typeobj):
		'''
		Crea una nueva variable temporal de un tipo dado.
		'''
		name = "__%s_%d" % (typeobj.name, self.versions[typeobj.name])
		self.versions[typeobj.name] += 1
		return name
	#visit definitions start here
	
	def visit_Var_Dec(self):
	    pass
	    
	def visit_Type(self):
	    pass
	    
    def visit_Assignation(self):
        pass
        
    def visit_Print(self):
        pass
        
    def visit_Write(self):
        pass
        
    def visit_Ubication(self):
        pass          
		
	def visit_Binary_op(self):
	    pass
	    
    def visit_Unary_op(self):
        pass
    
    def visit_Id(self):
        pass
        
    def visit_Integer(self):
        pass 
        
    def visit_Float(self):
        pass        
		
		
