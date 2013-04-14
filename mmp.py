# mpasparse
import ply.yacc as yacc
import ply.lex as lex
import mpaslex
from mpaslex import tokens
import sys



class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
         self.lineno = 0
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf         

    def __str__(self):
        return "<%s>" % self.type

	# Funcion para concatenar nodos
    def append (self, Node):
        self.children.append(Node)

    def __repr__(self):
        return "<%s>" % self.type


#------------------------------------#
#   Funcion para imprimir el AST     #
#------------------------------------#

def dump_tree(node, indent = ""):
    #print node
    if not hasattr(node, "datatype"):
		datatype = ""
    else:
		datatype = node.datatype
    if not node.leaf:
		print "%s%s  %s" % (indent, node.type, datatype)
    else:
		print "%s%s (%s)  %s" % (indent, node.type, node.leaf, datatype)

    indent = indent.replace("-"," ")
    indent = indent.replace("+"," ")
    for i in range(len(node.children)):
        c = node.children[i]
        if i == len(node.children)-1:
			dump_tree(c, indent + "  +-- ")
        else:
			dump_tree(c, indent + "  |-- ")




precedence = (
		('left', 'OR'),
		('left', 'AND'),
		('left', 'NOT'),
		('left', 'PLUS','MINUS'),
		('left', 'TIMES','DIVIDE'),
		('right', 'UMINUS'),
        ('right', 'ELSE'),
)

start = 'program'

def p_program(p):
    'program : func_list'
    p[0] = Node('Programa', [p[1]])
    p[0].lineno = lexer.lineno

def p_func_list(p):
    'func_list : function'
    p[0] = Node('Funciones', [p[1]])
    p[0].lineno = lexer.lineno

def p_func_list2(p):
    'func_list : func_list function'
    p[1].append(p[2])
    p[0] = p[1]

def p_function(p):
    'function : FUNC ID LPAREN argsop RPAREN locals_op BEGIN dec_list END'
    p[0] = Node ('Funcion', [p[4], p[6], p[8]], p[2])
    p[0].lineno = lexer.lineno

def p_errorFuncion(p):
    'function : FUNC ID LPAREN argsop RPAREN locals_op BEGIN dec_list SEMICOLON END'
    p[0] = Node ('Funcion', [p[4], p[6], p[8]], p[2])
    p[0].lineno = lexer.lineno
    print ("Warning: Line %d. Statments ends with semicolon" %p.lineno(9))

#Argumentos
def p_argsop1(p):
    'argsop : arguments'
    p[0] = p[1]

def p_argsop2(p):
    'argsop : empty'
    p[0] = Node("empty_argument", [], 'empty' )
    p[0].lineno = lexer.lineno

def p_arguments1(p):
    'arguments : var_dec'
    p[0] = Node ('Argumentos', [p[1]])
    p[0].lineno = lexer.lineno

def p_arguments2(p):
    'arguments : arguments COMMA var_dec'
    p[1].append(p[3])
    p[0]=p[1]

def p_arguments3(p):
    'arguments : arguments var_dec'
    p[1].append(p[2])
    p[0]=p[1]
    print ("Los arguments deben separarse por comas (,) Linea: %d" % lexer.lineno)

def p_errorarguments(p):
    'arguments : error'
    print ("Los arguments deben separarse por comas (,) y deben ser del tipo 'id':'tipo'. Linea: %d" % lexer.lineno)
    p[0] = Node ('Error Argumentos', [])

#Locales
def p_locals_op1(p):
    'locals_op : locals'
    p[0]=p[1]

def p_locals_op2(p):
    'locals_op : empty'
    p[0] = Node("localsVacio", [], 'empty' )
    p[0].lineno = lexer.lineno

def p_locals1(p):
    'locals : var_dec SEMICOLON'
    p[0] = Node ('Variables Locales', [p[1]])
    p[0].lineno = lexer.lineno

def p_locals2(p):
    'locals : function SEMICOLON'
    p[0] = Node ('Funciones Locales', [p[1]])
    p[0].lineno = lexer.lineno

def p_locals3(p):
    'locals : locals var_dec SEMICOLON'
    p[1].append(p[2])
    p[0] = p[1]
    p[0].lineno = lexer.lineno

def p_locals4(p):
    'locals : locals function SEMICOLON'
    p[1].append(p[2])
    p[0] = p[1]
    p[0].lineno = lexer.lineno

def p_errorlocals1(p):
    'locals : error'
    print ("Error en definicion de variables locals. Linea: %d" % lexer.lineno)
    p[0] = Node("Error al definir locals", [])
    p[0].lineno = lexer.lineno

def p_var_dec(p):
    'var_dec : ID COLON type'
    p[0] = Node("Def. variable", [p[3]], p[1])
    p[0].lineno = lexer.lineno

def p_errorDefvar(p):
    'var_dec : ID type'
    p[0] = Node("Def. variable", [p[2]], p[1])
    p[0].lineno = lexer.lineno
    print ("Error en definicion de variables locals. Faltan los dos puntos ':' Linea: %d" % lexer.lineno)

def p_tipo1(p):
    'type : INT_TYPE'
    p[0] = Node ('tipo',[], "Entero")
    p[0].lineno = lexer.lineno

def p_tipo2(p):
    'type : FLOAT_TYPE'
    p[0] = Node ('tipo',[], "Float")
    p[0].lineno = lexer.lineno

def p_tipo3(p):
    'type : INT_TYPE LSBRACKET expression RSBRACKET'
    p[0] = Node ('Vector INT_TYPE', [Node('Posicion',[p[3]])], 'Vector INT_TYPE')
    p[0].lineno = lexer.lineno

def p_tipo4(p):
    'type : FLOAT_TYPE LSBRACKET expression RSBRACKET'
    p[0] = Node ('Vector float', [Node('Posicion',[p[3]])],'Vector float')
    p[0].lineno = lexer.lineno

#Statements/Declaraciones

def p_declaration1(p):
    'declaration : WHILE relation DO declaration'
    p[0] = Node ('While', [Node('Condicion',[p[2]]), Node('Then',[p[4]])])
    p[0].lineno = lexer.lineno

def p_declaration2(p):
    'declaration : ifthen'
    p[0] = p[1]

def p_declaration3(p):
    'declaration : ifthenelse'
    p[0] = p[1]

def p_declaration4(p):
    'declaration : ubication ASSIGN expression'
    p[0] = Node ('Asignacion', [p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_declaration5(p):
    'declaration : PRINT LPAREN STRING RPAREN'
    p[0] = Node ('Print',[], p[3])
    p[0].lineno = lexer.lineno

def p_declaration6(p):
    'declaration : WRITE LPAREN expression RPAREN'
    p[0] = Node ('Write', [p[3]])
    p[0].lineno = lexer.lineno

def p_declaration7(p):
    'declaration : READ LPAREN ubication RPAREN'
    p[0] = Node ('Read',[p[3]])
    p[0].lineno = lexer.lineno

def p_declaration8(p):
    'declaration : RETURN expression'
    p[0] = Node ('Return',[p[2]])
    p[0].lineno = lexer.lineno

def p_declaration9(p):
    'declaration : ID LPAREN expressions_listop RPAREN'
    p[0] = Node ('Llamado a Funcion', [p[3]], p[1])
    p[0].lineno = lexer.lineno

def p_declaration10(p):
    'declaration : SKIP'
    p[0] = Node ('Skip',[], p[1])
    p[0].lineno = lexer.lineno

def p_declaration11(p):
    'declaration : BREAK'
    p[0] = Node ('Break',[], p[1])
    p[0].lineno = lexer.lineno

def p_declaration12(p):
    'declaration : BEGIN dec_list END'
    p[0] = p[2]

def p_error_empty_list(p):
    'declaration : BEGIN END'
    print ("Conjunto de declarationes vacias en linea %d" % lexer.lineno)

#def p_errorDeclaracion(p):
#    'declaration : erro'
#    prINT_TYPE ("Error en declaration cerca de la linea %d. Todas las declarationes a excepcion de la ultima (antes de un 'END') deben terminar con punto y coma (;)" % lexer.lineno)
#    p[0] = Node ('Error en declaration',[],p[1])

#.### Ifs ###.#
def p_ifthen(p):
    'ifthen : IF relation THEN declaration %prec ELSE'
    p[0] = Node("NodoIfThen", [Node('Condicion', [p[2]]), Node('Then', [p[4]])])
    p[0].lineno = lexer.lineno

def p_ifthenelse(p):
    'ifthenelse : IF relation THEN declaration ELSE declaration'
    p[0] = Node("NodoIfThenElse", [Node('Condicion', [p[2]]), Node('Then', [p[4]]), Node('Else', [p[6]])])
    p[0].lineno = lexer.lineno

def p_errorifthen(p):
    'ifthen : IF relation declaration %prec ELSE'
    print ("Error en IF cerca de la linea %d. no se encontro 'then'" % lexer.lineno)
    #p[0] = Node("NodoIfthen", [Node('Condicion', [p[2]]), Node('Then', [p[3]])])

def p_errorifthenelse(p):
    'ifthen : IF relation declaration ELSE declaration'
    print ("Error en IF cerca de la linea %d. no se encontro 'then'" % lexer.lineno)

#lista de claraciones
def p_dec_list1(p):
    'dec_list : declaration'
    p[0]= Node ('Declaraciones', [p[1]])

def p_dec_list2(p):
    'dec_list : dec_list SEMICOLON declaration'
    p[1].append(p[3])
    p[0]=p[1]

def p_dec_listerror(p):
    'dec_list : dec_list declaration'    
    print("Error en definicion de variables locals. Falta punto y coma. Linea: %d" % lexer.lineno)
    p[1].append(p[2])
    p[0]=p[1]    

#ubication
def p_ubication1(p):
    'ubication : ID'
    p[0] = Node("Ubicacion", [], p[1])
    p[0].lineno = lexer.lineno

def p_ubication2(p):
    'ubication : ID LSBRACKET expression RSBRACKET'
    p[0] = Node("Ubicacionvector", [p[3]] ,p[1])
    p[0].lineno = lexer.lineno

#expressiones
def p_expression1(p):
    'expression : expression PLUS expression'
    p[0] = Node ('Suma',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_expression2(p):
    'expression : expression MINUS expression'
    p[0] = Node ('Resta',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_expression3(p):
    'expression : expression TIMES expression'
    p[0] = Node ('Multiplicacion',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_expression4(p):
    'expression : expression DIVIDE expression'
    p[0] = Node ('Division',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_expression5(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = Node ('Menos', [p[2]])
    p[0].lineno = lexer.lineno

def p_expression6(p):
    'expression : PLUS expression'
    p[0] = Node ('Mas', [p[2]])

def p_expression7(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression8(p):
    'expression : ID LPAREN expressions_listop RPAREN'
    p[0] = Node ('Llamado a Funcion',[p[3]], p[1])
    p[0].lineno = lexer.lineno

def p_expression9(p):
    'expression : ID'
    p[0] = Node ('Id',[], p[1])
    p[0].lineno = lexer.lineno

def p_expression10(p):
    'expression : ID LSBRACKET expression RSBRACKET'
    p[0] = Node ('Vecto',[Node('Posicion', [p[3]])], p[1])
    p[0].lineno = lexer.lineno

def p_expression11(p):
    'expression : number'
    p[0] = p[1]

def p_expression12(p):
    'expression : INT_TYPE LPAREN expression RPAREN'
    p[0] = Node ('ConverInt',[p[3]])
    p[0].lineno = lexer.lineno

def p_expression13(p):
    'expression : FLOAT_TYPE LPAREN expression RPAREN'
    p[0] = Node ('ConverFloat',[p[3]])
    p[0].lineno = lexer.lineno

#Lista de expressiones
def p_expressions_listop1(p):
    'expressions_listop : expressions_list'
    p[0] = p[1]

def p_expressions_listop2(p):
    'expressions_listop : empty'
    p[0] = Node("Lista de expressiones vacia", [], 'empty' )
    p[0].lineno = lexer.lineno


def p_expressions_list1(p):
    'expressions_list : expression'
    p[0]= Node('Expresiones', [p[1]])
    p[0].lineno = lexer.lineno

def p_expressions_list2(p):
    'expressions_list : expressions_list COMMA expression'
    p[1].append(p[3])
    p[0]=p[1]


def p_relation1(p):
    'relation : expression LT expression'
    p[0] = Node ('<',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation2(p):
    'relation : expression LE expression'
    p[0] = Node ('<=',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation3(p):
    'relation : expression GT expression'
    p[0] = Node ('>',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation4(p):
    'relation : expression GE expression'
    p[0] = Node ('>=',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation5(p):
    'relation : expression EQ expression'
    p[0] = Node ('==',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation6(p):
    'relation : expression NE expression'
    p[0] = Node ('!=',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation7(p):
    'relation : relation AND relation'
    p[0] = Node ('and',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation8(p):
    'relation : relation OR relation'
    p[0] = Node ('o',[p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation9(p):
    'relation : NOT relation'
    p[0] = Node ('not',[p[2]])
    p[0].lineno = lexer.lineno

def p_relation10(p):
    'relation : LPAREN relation RPAREN'
    p[0] = p[2]

def p_errorRelacion(p):
    'relation : error'
    print ("Error de relation en linea %d" % lexer.lineno)

def p_number1(p):
    'number : INTEGER'
    p[0] = Node('Entero',[],p[1])
    p[0].lineno = lexer.lineno

def p_number2(p):
    'number : FLOAT'
    p[0] = Node('Float',[],p[1])
    p[0].lineno = lexer.lineno

def p_empty(p):
    'empty :'

# regla de error general
def p_error(p):
    if p:
        print ("Error de sintaxis con la expression %s en la linea %d" % (p.type, lexer.lineno))

parser = yacc.yacc(debug=1)

# Build the parser
if __name__ == "__main__":
    f = open(sys.argv[1])
    s = f.read()
    lexer = mpaslex.make_lexer()
    result = parser.parse(s)
    if result:
        #Acá se llama al visitor
