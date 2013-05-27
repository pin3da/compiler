# mpasparse
import ply.yacc as yacc
import ply.lex as lex
import mpaslex
from mpaslex import tokens
import sys
from mpasast import *


lexer = mpaslex.make_lexer()

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
    p[0] = Program(p[1])

def p_func_list(p):
    'func_list : function'
    p[0] = Func_list([p[1]])

def p_func_list2(p):
    'func_list : func_list function'
    p[1].append(p[2])
    p[0] = p[1]

def p_function(p):
    'function : FUNC ID LPAREN argsop RPAREN locals_op BEGIN dec_list END'
    p[0] = Function(p[2], p[4],None, p[6], p[8])
    p[0].lineno = p[4].lineno

def p_function2(p):
    'function : FUNC ID LPAREN argsop RPAREN COLON type locals_op BEGIN dec_list END'
    p[0] = Function(p[2],p[4],p[7],p[8],p[10])
    p[0].lineno = p[4].lineno

def p_errorFuncion(p):
    'function : FUNC ID LPAREN argsop RPAREN COLON type locals_op BEGIN dec_list SEMICOLON END'
    p[0] = Function(p[2], p[4],p[7], p[8], p[10])
    p[0].lineno = p[4].lineno   
    sys.stderr.write("Warning: Line %d. Statments ends with semicolon\n" %p.lineno(9))


def p_errorFuncion2(p):
    'function : FUNC ID LPAREN argsop RPAREN locals_op BEGIN dec_list SEMICOLON END'
    p[0] = Function(p[2], p[4],None, p[6], p[8])
    p[0].lineno = p[4].lineno     
    sys.stderr.write("Warning: Line %d. Statments ends with semicolon\n" %p.lineno(9))


def p_errorFuncion3(p):
    'function : FUNC ID LPAREN argsop RPAREN ASSIGN type locals_op BEGIN dec_list SEMICOLON END'
    p[0] = Function(p[2], p[4],p[7], p[8], p[10])
    p[0].lineno = p[4].lineno
    sys.stderr.write("Warning: Line %d. Return type must be preceded by colon (:) \n" %p.lineno(9))


#Argumentos
def p_argsop1(p):
    'argsop : arguments'
    p[0] = p[1]

def p_argsop2(p):
    'argsop : empty'
    p[0] = Empty_arguments([], 'empty')

def p_arguments1(p):
    'arguments : var_dec'
    p[0] = Arguments([p[1]])
    p[0].lineno = p[1].lineno

def p_arguments2(p):
    'arguments : arguments COMMA var_dec'
    p[1].append(p[3])
    p[0]=p[1]

def p_arguments3(p):
    'arguments : arguments var_dec'
    p[1].append(p[2])
    p[0]=p[1]
    sys.stderr.write("Error line %d: Arguments must be separate by comma (,)\n" % p.lineno(1))

#def p_errorarguments(p):
#    'arguments : error'
#    sys.stderr.write ("Error line %d: The arguments must be decalrate ID:TYPE and separate by comma\n" % lexer.lineno)

#Locales
def p_locals_op1(p):
    'locals_op : locals'
    p[0] = p[1]
    p[0].lineno = p[1].lineno

def p_locals_op2(p):
    'locals_op : empty'
    p[0] = Empty_locals( [], 'empty' )

def p_locals1(p):
    'locals : var_dec SEMICOLON'
    p[0] = Local_var( [p[1]])
    p[0].lineno = p[1].lineno

def p_locals2(p):
    'locals : function SEMICOLON'
    p[0] = Local_fun([p[1]])
    p[0].lineno = p[1].lineno

def p_locals3(p):
    'locals : locals var_dec SEMICOLON'
    p[1].append(p[2])
    p[0] = p[1]

def p_locals4(p):
    'locals : locals function SEMICOLON'
    p[1].append(p[2])
    p[0] = p[1]
    
def p_var_dec(p):
    'var_dec : ID COLON type'
    p[0] = Var_dec(p[1], p[3])
    p[0].lineno = p.lineno(1)
        
def p_errorDefvar(p):
    'var_dec : ID type'
    p[0] = Var_dec(p[1], p[3])
    p[0].lineno = p.lineno(1)
    sys.stderr.write ("Error line %d: ':' missing\n" % p.lineno(1))

def p_tipo1(p):
    'type : INT_TYPE'
    p[0] = Type('integer',_leaf=True)
        
def p_tipo2(p):
    'type : FLOAT_TYPE'
    p[0] = Type('float',_leaf=True)
       
def p_tipo3(p):
    'type : INT_TYPE LSBRACKET expression RSBRACKET'
    p[0] = Vector('integer', p[3])
    p[0].lineno = p.lineno(1)
        
def p_tipo4(p):
    'type : FLOAT_TYPE LSBRACKET expression RSBRACKET'
    p[0] = Vector('float',p[3])
    p[0].lineno = p.lineno(1)
        

def p_tipo5(p):
    'type : STRING_TYPE'
    p[0] = Type('string',_leaf=True)
    p[0].lineno = p.lineno(1)

def p_tipo6(p):
    'type : STRING_TYPE LSBRACKET expression RSBRACKET'
    p[0] = Vector('string',p[3])
    p[0].lineno = p.lineno(1)

#Statements/Declaraciones

def p_declaration1(p):
    'declaration : WHILE relation DO declaration'
    p[0] = While(Condition(p[2]),Then(p[4]) )
    p[0].lineno = p.lineno(1)
        
def p_declaration2(p):
    'declaration : ifthen'
    p[0] = p[1]
    p[0].lineno = p.lineno(1)

def p_declaration3(p):
    'declaration : ifthenelse'
    p[0] = p[1]
    p[0].lineno = p.lineno(1)

def p_declaration4(p):
    'declaration : ubication ASSIGN expression'
    p[0] = Assignation(p[1], p[3])
    p[0].lineno = p.lineno(2)
        
def p_declaration_error(p):
    'declaration : ubication COLONEQUAL expression'
    sys.stderr.write("Error line %d: Assignation must be :=\n" % p.lineno(2))
    exit()

def p_declaration5(p):
    'declaration : PRINT LPAREN STRING RPAREN'
    p[0] = Print(p[3],_leaf=True)
    p[0].lineno = p.lineno(1)
        
def p_declaration6(p):
    'declaration : WRITE LPAREN expression RPAREN'
    p[0] = Write(p[3])
    p[0].lineno = p.lineno(1)
        
def p_declaration7(p):
    'declaration : READ LPAREN ubication RPAREN'
    p[0] = Read (p[3])
    p[0].lineno = p.lineno(1)
        
def p_declaration8(p):
    'declaration : RETURN expression'
    p[0] = Return(p[2])
    p[0].lineno = p.lineno(1)
        
def p_declaration9(p):
    'declaration : ID LPAREN expressions_listop RPAREN'
    p[0] = Call_func(p[1], p[3])
    p[0].lineno = p.lineno(1)
        
def p_declaration10(p):
    'declaration : SKIP'
    p[0] = Skip('skip', _leaf=True)
    p[0].lineno = p.lineno(1)

def p_declaration11(p):
    'declaration : BREAK'
    p[0] = Break('break',_leaf=True)
    p[0].lineno = p.lineno(1)
        
def p_declaration12(p):
    'declaration : BEGIN dec_list END'
    p[0] = p[2]

def p_error_empty_list(p):
    'declaration : BEGIN END'
    sys.stderr.write ("Error line %d: No declarations found.\n" % p.lineno(1))

#if
def p_ifthen(p):
    'ifthen : IF relation THEN declaration %prec ELSE'
    p[0] = Ifthen( p[2],Then(p[4]) )
    p[0].lineno = p.lineno(1)

def p_ifthenelse(p):
    'ifthenelse : IF relation THEN declaration ELSE declaration'
    p[0] = Ifthenelse(p[2],Then(p[4]),Else(p[6]))
    p[0].lineno = p.lineno(1)

def p_errorifthen(p):
    'ifthen : IF relation declaration %prec ELSE'
    sys.stderr.write("Error line %d: missing then\n" % p.lineno(2))
    #p[0] = Node("NodoIfthen", [Node('Condicion', [p[2]]), Node('Then', [p[3]])])

def p_errorifthenelse(p):
    'ifthen : IF relation declaration ELSE declaration'
    sys.stderr.write ("Error line %d: missing then\n" % p.lineno(2))

#lista de claraciones
def p_dec_list1(p):
    'dec_list : declaration'
    p[0]= Dec_list([p[1]])

def p_dec_list2(p):
    'dec_list : dec_list SEMICOLON declaration'
    p[1].append(p[3])
    p[0] = p[1]

def p_dec_listerror(p):
    'dec_list : dec_list declaration'    
    sys.stderr.write("Error line %d: Locals definition. Semicolon is missing\n" % p.lineno(2))
    p[1].append(p[2])
    p[0] = p[1]    

#ubication
def p_ubication1(p):
    'ubication : ID'
    p[0] = Ubication(p[1],_leaf=True)
    p[0].lineno = p.lineno(1)

def p_ubication2(p):
    'ubication : ID LSBRACKET expression RSBRACKET'
    p[0] = Ubication_vector(p[1],Position(p[3]))
    p[0].lineno = p.lineno(1)

#expressiones
def p_expression1(p):
    'expression : expression PLUS expression'
    p[0] = Binary_op('+',p[1], p[3])
    p[0].lineno = p.lineno(2)

def p_expression2(p):
    'expression : expression MINUS expression'
    p[0] = Binary_op('-',p[1], p[3])
    p[0].lineno = p.lineno(2)

def p_expression3(p):
    'expression : expression TIMES expression'
    p[0] = Binary_op('*',p[1], p[3])
    p[0].lineno = p.lineno(2)
        
def p_expression4(p):
    'expression : expression DIVIDE expression'
    p[0] = Binary_op('/',p[1],p[3])
    p[0].lineno = p.lineno(2)
        
def p_expression5(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = Unary_op('-',p[2])
    p[0].lineno = p.lineno(2)
       
def p_expression6(p):
    'expression : PLUS expression'
    p[0] = Unary_op('+',p[2])
    p[0].lineno = p.lineno(2)

def p_expression7(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]
    p[0].lineno = p.lineno(2)

def p_expression8(p):
    'expression : ID LPAREN expressions_listop RPAREN'
    p[0] = Call_func(p[1],p[3])
    p[0].lineno = p.lineno(1)
        
def p_expression9(p):
    'expression : ID'
    p[0] = Id(p[1],_leaf=True)
    p[0].lineno = p.lineno(1)
        
def p_expression10(p):
    'expression : ID LSBRACKET expression RSBRACKET'
    p[0] = Ubication_vector(p[1],Position(p[3]))
    p[0].lineno =  p.lineno(1)

def p_expression11(p):
    'expression : number'
    p[0] = p[1]
    p[0].lineno = p.lineno(1)

def p_expression12(p):
    'expression : INT_TYPE LPAREN expression RPAREN'
    p[0] = Cast_int(p[3])
    p[0].lineno = p.lineno(1)
        
def p_expression13(p):
    'expression : FLOAT_TYPE LPAREN expression RPAREN'
    p[0] = Cast_float(p[3])
    p[0].lineno = p.lineno(1)
        
#Lista de expressiones
def p_expressions_listop1(p):
    'expressions_listop : expressions_list'
    p[0] = p[1]

def p_expressions_listop2(p):
    'expressions_listop : empty'
    p[0] = Empty_expr_list()    
        
def p_expressions_list1(p):
    'expressions_list : expression'
    p[0]= Expression_list( [p[1]])
        
def p_expressions_list2(p):
    'expressions_list : expressions_list COMMA expression'
    p[1].append(p[3])
    p[0]=p[1]

def p_relation1(p):
    'relation : expression LT expression'
    p[0] = Binary_op('<', p[1],p[3])
    p[0].lineno = p.lineno(2)
        
def p_relation2(p):
    'relation : expression LE expression'
    p[0] = Binary_op('<=', p[1],p[3])
    p[0].lineno = p.lineno(2)
        
def p_relation3(p):
    'relation : expression GT expression'
    p[0] = Binary_op('>',p[1],p[3])
    p[0].lineno = p.lineno(2)
        
def p_relation4(p):
    'relation : expression GE expression'
    p[0] = Binary_op('>=',p[1],p[3])
    p[0].lineno = p.lineno(2)
        
def p_relation5(p):
    'relation : expression EQ expression'
    p[0] = Binary_op('==',p[1],p[3])
    p[0].lineno = p.lineno(2)
        
def p_relation6(p):
    'relation : expression NE expression'
    p[0] = Binary_op('!=',p[1],p[3])
    p[0].lineno = p.lineno(2)

def p_relation7(p):
    'relation : relation AND relation'
    p[0] = Binary_op('and',p[1],p[3])
    p[0].lineno = p.lineno(2)
    
def p_relation8(p):
    'relation : relation OR relation'
    p[0] = Binary_op('or',p[1],p[3])
    p[0].lineno = p.lineno(2)
   
def p_relation9(p):
    'relation : NOT relation'
    p[0] = Unary_op('not',p[2])
    p[0].lineno =  p.lineno(1)
        
def p_relation10(p):
    'relation : LPAREN relation RPAREN'
    p[0] = p[2]
    p[0].lineno = p.lineno(2)

def p_number1(p):
    'number : INTEGER'
    p[0] = Integer(p[1],_leaf=True)
    p[0].lineno = p.lineno(1)
        
def p_number(p):
    'number : FLOAT'
    p[0] = Float(p[1],_leaf=True)
    p[0].lineno = p.lineno(1)
        
def p_empty(p):
    'empty :'

# regla de error general
def p_error(p):
    if p:
        sys.stderr.write ("Syntax error at line %d:  %s -> %s\n" % (p.lineno, p.type , p.value ))

def make_parser(): 
    lexer = mpaslex.make_lexer()
    parser = yacc.yacc(debug=1)
    return parser

def dump_tree(node, indent = ""):
    #print node
    if not hasattr(node, "datatype"):
		datatype = ""
    else:
		datatype = node.datatype

    if(node.__class__.__name__ != "str" and node.__class__.__name__ != "list"):
        print "%s%s  %s" % (indent, node.__class__.__name__, datatype)

    indent = indent.replace("-"," ")
    indent = indent.replace("+"," ")
    if hasattr(node,'_fields'):
        mio = node._fields
    else:
        mio = node
    if(isinstance(mio,list)):
        for i in range(len(mio)):
            if(isinstance(mio[i],str) ):
                c = getattr(node,mio[i])
            else:
             c = mio[i]
            if i == len(mio)-1:
		    	dump_tree(c, indent + "  +-- ")
            else:
		    	dump_tree(c, indent + "  |-- ")
    else:
        print indent, mio
        

# Build the parser
if __name__ == "__main__":
#    from errors import subscribe_errors
    f = open(sys.argv[1])
    s = f.read()
    lexer = mpaslex.make_lexer()
    parser = make_parser()
    result = parser.parse(s)
    if result:
	    result.graphprint(sys.argv[1]+".png")	
        #dump_tree(result)
        
