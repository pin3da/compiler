import mpasast
import mpasblock
from mpasast import *
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
    'and': 'land',
    'or': 'lor',
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
        super(SSAVisitor, self).__init__()

        # version diccionario para temporales
        self.versions = defaultdict(int)

        # El codigo generado (lista de tuplas)
        self.code = BasicBlock()
        self.start_block = self.code

        # Una lista de declaraciones externas (y tipos)
        self.externs = []

    def new_temp(self,return_type):
        '''
        Crea una nueva variable temporal de un tipo dado.
        '''
        name = "__%s_%d" % (return_type, self.versions[return_type])
        self.versions[return_type] += 1
        return name
    #visit definitions start here
    
    def visit_Var_dec(self, node):
        # localice en memoria
        inst = ('alloc_'+node.return_type, node.id)
        self.code.append(inst)
        #se borro el resto pq nosotros en var_dec solo alocamos memoria no mas
        
        
    def visit_Type(self,_type):
        pass
        
    def visit_Assignation(self, node):
        self.visit(node.value)
        if not (isinstance(node.ubication, Ubication_vector)):
            inst = ('store_'+node.value.return_type, node.value.gen_location, node.ubication.value)
            self.code.append(inst)
        else:
            inst = ('store_'+node.value.return_type, node.value.gen_location, node.ubication.id)
            self.code.append(inst) 
        
    def visit_Print(self, node):
        if(isinstance(node.value, AST)):
            self.visit(node.value)
            inst = ('print_string','expression')
        else:
            inst = ('print_string',node.value)

        # Cree el opcode y agregarlo a la lista
        self.code.append(inst)
        
        
    def visit_Write(self,node):
        pass
        
    def visit_Binary_op(self,node):
        # Visita las expresiones izquierda y derecha
        self.visit(node.left)
        self.visit(node.right)
        # Crea un nuevo temporal para almacenar el resultado
        target = self.new_temp(node.return_type)

        # Crea opcode y agrega a la lista
        opcode = binary_ops[node.op] + "_" + node.return_type
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
     
    def visit_Integer(self, node):
        target =  self.new_temp('integer')
        node.gen_location = target
        inst = ('literal_integer', node.value, target)
        self.code.append(inst)
                
    def visit_Float(self,node):
        target = self.new_temp('float')
        node.gen_location =  target
        inst = ('literal_float', node.value, target)
        self.code.append(inst)

    def visit_Call_func(self, node):
        target = self.new_temp(node.return_type)
        inst = ('call_func',node.func_id,target)
        self.code.append(inst)
        node.gen_location = target



    ####
    # Terminar allocator vector
    ###
    
    def visit_Vector(self,node):
        pass
    
    def visit_Ubication_vector(self,node):
        pass

    def visit_Id(self,node):
        target =  self.new_temp(node.return_type)
        inst=('load_'+node.return_type, node.value, target)
        node.gen_location=target
        self.code.append(inst)


def generate_code(node):
    '''
    Genera codigo SSA desde el nodo AST entregado.
    '''
    gen = SSAVisitor()
    gen.visit(node)
    return gen

if __name__ == '__main__':
    import mpaslex
    import mpasparse
    import semantic
    import sys
    from errors import subscribe_errors, errors_reported
    lexer = mpaslex.make_lexer()
    parser = mpasparse.make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())
        # Revise el programa
        num_errors = semantic.check_program(program)
        # Si no ocurre errore, genere codigo
        if num_errors == 0:
            code = generate_code(program)
            # Emite la secuencia de codigo
            #exprblock.PrintBlocks().visit(code.start_block)
            
            for inst in code.code:
                print(inst)
        else:
            sys.stderr.write("Program couldn't be compiled\n")
