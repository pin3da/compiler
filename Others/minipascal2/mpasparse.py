import ply.yacc as yacc
import sys
import ply.lex as lex
import mpaslex

from mpaslex import tokens
#tokens = mpaslex.tokens

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
		('left', 'or'),
		('left', 'and'),
		('left', 'not'),
		('left', 'SUMA','RESTA'),
		('left', 'MULTI','DIVIDIR'),
		('right', 'UMINUS'),
        ('right', 'else'),
)

start = 'program'

def p_program(p):
    r'program : listadefuns'
    p[0] = Node('Programa', [p[1]])
    p[0].lineno=mpaslex.lexer.lineno

def p_listadefuns(p):
    r'listadefuns : funcion'
    p[0]= Node('Funciones', [p[1]])
    p[0].lineno=mpaslex.lexer.lineno

def p_listadefuns2(p):
    r'listadefuns : listadefuns funcion'
    p[1].append(p[2])
    p[0]=p[1]

def p_funcion(p):
    r'funcion : fun ID PARI argsop PARD localesop begin listadeclaraciones end'
    p[0] = Node ('Funcion', [p[4], p[6], p[8]], p[2])
    p[0].lineno=mpaslex.lexer.lineno

def p_errorFuncion(p):
    r'funcion : fun ID PARI argsop PARD localesop begin listadeclaraciones PYC end'
    p[0] = Node ('Funcion', [p[4], p[6], p[8]], p[2])
    p[0].lineno=mpaslex.lexer.lineno
    print ("Sobra punto y coma ';'al final de la lista de declaraciones. Linea %d" %p.lineno(9))

#Argumentos
def p_argsop1(p):
    r'argsop : argumentos'
    p[0]=p[1]

def p_argsop2(p):
    r'argsop : empty'
    p[0] = Node("argumentoVacio", [], 'empty' )
    p[0].lineno=mpaslex.lexer.lineno

def p_argumentos1(p):
    r'argumentos : defvar'
    p[0] = Node ('Argumentos', [p[1]])
    p[0].lineno=mpaslex.lexer.lineno

def p_argumentos2(p):
    r'argumentos : argumentos COMA defvar'
    p[1].append(p[3])
    p[0]=p[1]

def p_argumentos3(p):
    r'argumentos : argumentos defvar'
    p[1].append(p[2])
    p[0]=p[1]
    print ("Los argumentos deben separarse por comas (,) Linea: %d" %mpaslex.lexer.lineno)

def p_errorargumentos(p):
    r'argumentos : error'
    print ("Los argumentos deben separarse por comas (,) y deben ser del tipo 'id':'tipo'. Linea: %d" %mpaslex.lexer.lineno)
    p[0] = Node ('Error Argumentos', [])

#Locales
def p_localesop1(p):
    r'localesop : locales'
    p[0]=p[1]

def p_localesop2(p):
    r'localesop : empty'
    p[0] = Node("localesVacio", [], 'empty' )
    p[0].lineno=mpaslex.lexer.lineno

def p_locales1(p):
    r'locales : defvar PYC'
    p[0] = Node ('Variables Locales', [p[1]])
    p[0].lineno=mpaslex.lexer.lineno

def p_locales2(p):
    r'locales : funcion PYC'
    p[0] = Node ('Funciones Locales', [p[1]])
    p[0].lineno=mpaslex.lexer.lineno

def p_locales3(p):
    r'locales : locales defvar PYC'
    p[1].append(p[2])
    p[0] = p[1]
    p[0].lineno=mpaslex.lexer.lineno

def p_locales4(p):
    r'locales : locales funcion PYC'
    p[1].append(p[2])
    p[0] = p[1]
    p[0].lineno=mpaslex.lexer.lineno

def p_errorlocales1(p):
    r'locales : error'
    print ("Error en definicion de variables locales. Linea: %d" %mpaslex.lexer.lineno)
    p[0] = Node("Error al definir locales", [])
    p[0].lineno=mpaslex.lexer.lineno

def p_defvar(p):
    r'defvar : ID DOSPUNT tipo'
    p[0] = Node("Def. variable", [p[3]], p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_errorDefvar(p):
    r'defvar : ID tipo'
    p[0] = Node("Def. variable", [p[2]], p[1])
    p[0].lineno=mpaslex.lexer.lineno
    print ("Error en definicion de variables locales. Faltan los dos puntos ':' Linea: %d" %mpaslex.lexer.lineno)

def p_tipo1(p):
    r'tipo : int'
    p[0] = Node ('tipo',[], "Entero")
    p[0].lineno=mpaslex.lexer.lineno

def p_tipo2(p):
    r'tipo : float'
    p[0] = Node ('tipo',[], "Float")
    p[0].lineno=mpaslex.lexer.lineno

def p_tipo3(p):
    r'tipo : int CORI expresion CORD'
    p[0] = Node ('Vector int', [Node('Posicion',[p[3]])], 'Vector int')
    p[0].lineno=mpaslex.lexer.lineno

def p_tipo4(p):
    r'tipo : float CORI expresion CORD'
    p[0] = Node ('Vector float', [Node('Posicion',[p[3]])],'Vector float')
    p[0].lineno=mpaslex.lexer.lineno

#Statements/Declaraciones

def p_declaracion1(p):
    r'declaracion : while relacion do declaracion'
    p[0] = Node ('While', [Node('Condicion',[p[2]]), Node('Then',[p[4]])])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion2(p):
    r'declaracion : ifthen'
    p[0] = p[1]

def p_declaracion3(p):
    r'declaracion : ifthenelse'
    p[0] = p[1]

def p_declaracion4(p):
    r'declaracion : ubicacion ASIG expresion'
    p[0] = Node ('Asignacion', [p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion5(p):
    r'declaracion : print PARI CADENA PARD'
    p[0] = Node ('Print',[], p[3])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion6(p):
    r'declaracion : write PARI expresion PARD'
    p[0] = Node ('Write', [p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion7(p):
    r'declaracion : read PARI ubicacion PARD'
    p[0] = Node ('Read',[p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion8(p):
    r'declaracion : return expresion'
    p[0] = Node ('Return',[p[2]])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion9(p):
    r'declaracion : ID PARI listadeexpresionesop PARD'
    p[0] = Node ('Llamado a Funcion', [p[3]], p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion10(p):
    r'declaracion : skip'
    p[0] = Node ('Skip',[], p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion11(p):
    r'declaracion : break'
    p[0] = Node ('Break',[], p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_declaracion12(p):
    r'declaracion : begin listadeclaraciones end'
    p[0] = p[2]

def p_errorListaVacia(p):
    r'declaracion : begin end'
    print ("Conjunto de declaraciones vacias en linea %d" %mpaslex.lexer.lineno)

#def p_errorDeclaracion(p):
#    r'declaracion : error'
#    print ("Error en declaracion cerca de la linea %d. Todas las declaraciones a excepcion de la ultima (antes de un 'end') deben terminar con punto y coma (;)" %mpaslex.lexer.lineno)
#    p[0] = Node ('Error en declaracion',[],p[1])

#.### Ifs ###.#
def p_ifthen(p):
    r'ifthen : if relacion then declaracion %prec else'
    p[0] = Node("NodoIfThen", [Node('Condicion', [p[2]]), Node('Then', [p[4]])])
    p[0].lineno=mpaslex.lexer.lineno

def p_ifthenelse(p):
    r'ifthenelse : if relacion then declaracion else declaracion'
    p[0] = Node("NodoIfThenElse", [Node('Condicion', [p[2]]), Node('Then', [p[4]]), Node('Else', [p[6]])])
    p[0].lineno=mpaslex.lexer.lineno

def p_errorifthen(p):
    r'ifthen : if relacion declaracion %prec else'
    print ("Error en if cerca de la linea %d. no se encontro 'then'" %mpaslex.lexer.lineno)
    #p[0] = Node("NodoIfthen", [Node('Condicion', [p[2]]), Node('Then', [p[3]])])

def p_errorifthenelse(p):
    r'ifthen : if relacion declaracion else declaracion'
    print ("Error en if cerca de la linea %d. no se encontro 'then'" %mpaslex.lexer.lineno)

#lista de claraciones
def p_listadeclaraciones1(p):
    r'listadeclaraciones : declaracion'
    p[0]= Node ('Declaraciones', [p[1]])

def p_listadeclaraciones2(p):
    r'listadeclaraciones : listadeclaraciones PYC declaracion'
    p[1].append(p[3])
    p[0]=p[1]

def p_listadeclaracioneserror(p):
    r'listadeclaraciones : listadeclaraciones declaracion'    
    print ("Error en definicion de variables locales. Falta punto y coma. Linea: %d" %mpaslex.lexer.lineno)
    p[1].append(p[2])
    p[0]=p[1]    

#ubicacion
def p_ubicacion1(p):
    r'ubicacion : ID'
    p[0] = Node("Ubicacion", [], p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_ubicacion2(p):
    r'ubicacion : ID CORI expresion CORD'
    p[0] = Node("Ubicacionvector", [p[3]] ,p[1])
    p[0].lineno=mpaslex.lexer.lineno

#expresiones
def p_expresion1(p):
    r'expresion : expresion SUMA expresion'
    p[0] = Node ('Suma',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion2(p):
    r'expresion : expresion RESTA expresion'
    p[0] = Node ('Resta',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion3(p):
    r'expresion : expresion MULTI expresion'
    p[0] = Node ('Multiplicacion',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion4(p):
    r'expresion : expresion DIVIDIR expresion'
    p[0] = Node ('Division',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion5(p):
    r'expresion : RESTA expresion %prec UMINUS'
    p[0] = Node ('-', [p[2]])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion6(p):
    r'expresion : SUMA expresion'
    p[0] = Node ('+', [p[2]])

def p_expresion7(p):
    r'expresion : PARI expresion PARD'
    p[0] = p[2]

def p_expresion8(p):
    r'expresion : ID PARI listadeexpresionesop PARD'
    p[0] = Node ('Llamado a Funcion',[p[3]], p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion9(p):
    r'expresion : ID'
    p[0] = Node ('Id',[], p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion10(p):
    r'expresion : ID CORI expresion CORD'
    p[0] = Node ('Vector',[Node('Posicion', [p[3]])], p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion11(p):
    r'expresion : numero'
    p[0] = p[1]

def p_expresion12(p):
    r'expresion : int PARI expresion PARD'
    p[0] = Node ('ConverInt',[p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_expresion13(p):
    r'expresion : float PARI expresion PARD'
    p[0] = Node ('ConverFloat',[p[3]])
    p[0].lineno=mpaslex.lexer.lineno

#Lista de expresiones
def p_listadeexpresionesop1(p):
    r'listadeexpresionesop : listadeexpresiones'
    p[0] = p[1]

def p_listadeexpresionesop2(p):
    r'listadeexpresionesop : empty'
    p[0] = Node("Lista de expresiones vacia", [], 'empty' )
    p[0].lineno=mpaslex.lexer.lineno


def p_listadeexpresiones1(p):
    r'listadeexpresiones : expresion'
    p[0]= Node('Expresiones', [p[1]])
    p[0].lineno=mpaslex.lexer.lineno

def p_listadeexpresiones2(p):
    r'listadeexpresiones : listadeexpresiones COMA expresion'
    p[1].append(p[3])
    p[0]=p[1]


def p_relacion1(p):
    r'relacion : expresion MENQ expresion'
    p[0] = Node ('<',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion2(p):
    r'relacion : expresion MENIG expresion'
    p[0] = Node ('<=',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion3(p):
    r'relacion : expresion MAYQ expresion'
    p[0] = Node ('>',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion4(p):
    r'relacion : expresion MAYIG expresion'
    p[0] = Node ('>=',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion5(p):
    r'relacion : expresion IGU expresion'
    p[0] = Node ('==',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion6(p):
    r'relacion : expresion DIF expresion'
    p[0] = Node ('!=',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion7(p):
    r'relacion : relacion and relacion'
    p[0] = Node ('and',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion8(p):
    r'relacion : relacion or relacion'
    p[0] = Node ('or',[p[1],p[3]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion9(p):
    r'relacion : not relacion'
    p[0] = Node ('not',[p[2]])
    p[0].lineno=mpaslex.lexer.lineno

def p_relacion10(p):
    r'relacion : PARI relacion PARD'
    p[0] = p[2]

def p_errorRelacion(p):
    r'relacion : error'
    print ("Error de relacion en linea %d" %mpaslex.lexer.lineno)

def p_numero1(p):
    r'numero : ENTERO'
    p[0] = Node('Entero',[],p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_numero2(p):
    r'numero : REAL'
    p[0] = Node('Float',[],p[1])
    p[0].lineno=mpaslex.lexer.lineno

def p_empty(p):
    r'empty :'

# regla de error general
def p_error(p):
    if p:
        print("Error de sintaxis con la expresion %s en la linea %d" % (p.type,mpaslex.lexer.lineno))

parser = yacc.yacc(debug=1)

# Build the parser
if __name__ == "__main__":
    f = open(sys.argv[1])
    s = f.read()
    result = parser.parse(s)
    if result:
        dump_tree(result)
