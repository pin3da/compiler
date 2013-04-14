# mpasparse
import ply.yacc as yacc
import ply.lex as lex
import mpaslex
from mpaslex import tokens
import sys
from ast import *


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
    p[0].lineno = lexer.lineno

def p_func_list(p):
    'func_list : function'
    p[0] = Func_list(p[1])
    p[0].lineno = lexer.lineno

def p_func_list2(p):
    'func_list : func_list function'
    p[1].append(p[2])
    p[0] = p[1]

def p_function(p):
    'function : FUNC ID LPAREN argsop RPAREN locals_op BEGIN dec_list END'
    p[0] = Function([p[2], p[4], p[6]], p[8])
    p[0].lineno = lexer.lineno

def p_errorFuncion(p):
    'function : FUNC ID LPAREN argsop RPAREN locals_op BEGIN dec_list SEMICOLON END'
    p[0] = Function([p[2], p[4], p[6]], p[8])
    p[0].lineno = lexer.lineno
    print ("Warning: Line %d. Statments ends with semicolon" %p.lineno(9))

#Argumentos
def p_argsop1(p):
    'argsop : arguments'
    p[0] = p[1]

def p_argsop2(p):
    'argsop : empty'
    p[0] = Empty_arguments([], 'empty')
    p[0].lineno = lexer.lineno

def p_arguments1(p):
    'arguments : var_dec'
    p[0] = Arguments( p[1] )
    p[0].lineno = lexer.lineno

def p_arguments2(p):
    'arguments : arguments COMMA var_dec'
    p[1].append(p[3])
    p[0]=p[1]

def p_arguments3(p):
    'arguments : arguments var_dec'
    p[1].append(p[2])
    p[0]=p[1]
    print ("Error line %d: Arguments must be separate by comma (,)" % lexer.lineno)

def p_errorarguments(p):
    'arguments : error'
    print ("Error line %d: The arguments must be decalrate ID:TYPE and separate by comma" % lexer.lineno)
    p[0] = Nrguments_error([])

#Locales
def p_locals_op1(p):
    'locals_op : locals'
    p[0] = p[1]

def p_locals_op2(p):
    'locals_op : empty'
    p[0] = Empty_locals( [], 'empty' )
    p[0].lineno = lexer.lineno

def p_locals1(p):
    'locals : var_dec SEMICOLON'
    p[0] = Local_var( p[1])
    p[0].lineno = lexer.lineno

def p_locals2(p):
    'locals : function SEMICOLON'
    p[0] = Local_fun(p[1])
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
    print ("Error line %d: Locals definition are wrong" % lexer.lineno)
    p[0] = Error_locals_def([])
    p[0].lineno = lexer.lineno

def p_var_dec(p):
    'var_dec : ID COLON type'
    p[0] = Var_dec(p[1], p[3])
    p[0].lineno = lexer.lineno

def p_errorDefvar(p):
    'var_dec : ID type'
    p[0] = Var_dec(p[1], p[3])
    p[0].lineno = lexer.lineno
    print ("Error line %d: ':' missing" % lexer.lineno)

def p_tipo1(p):
    'type : INT_TYPE'
    p[0] = Type('Integer_type')
    p[0].lineno = lexer.lineno

def p_tipo2(p):
    'type : FLOAT_TYPE'
    p[0] = Type('Float_type')
    p[0].lineno = lexer.lineno

def p_tipo3(p):
    'type : INT_TYPE LSBRACKET expression RSBRACKET'
    p[0] = Vector('Integer_type', p[3])
    p[0].lineno = lexer.lineno

def p_tipo4(p):
    'type : FLOAT_TYPE LSBRACKET expression RSBRACKET'
    p[0] = Vector('Float_type',p[3])
    p[0].lineno = lexer.lineno

#Statements/Declaraciones

def p_declaration1(p):
    'declaration : WHILE relation DO declaration'
    p[0] = While(Condition(p[2]),Then(p[4]) ) #se crea el nodo condition para efectos de visualizacion
    p[0].lineno = lexer.lineno

def p_declaration2(p):
    'declaration : ifthen'
    p[0] = p[1]

def p_declaration3(p):
    'declaration : ifthenelse'
    p[0] = p[1]

def p_declaration4(p):
    'declaration : ubication ASSIGN expression'
    p[0] = Asignation(p[1], p[3])
    p[0].lineno = lexer.lineno

def p_declaration5(p):
    'declaration : PRINT LPAREN STRING RPAREN'
    p[0] = Print(p[3])
    p[0].lineno = lexer.lineno

def p_declaration6(p):
    'declaration : WRITE LPAREN expression RPAREN'
    p[0] = Write(p[3])
    p[0].lineno = lexer.lineno

def p_declaration7(p):
    'declaration : READ LPAREN ubication RPAREN'
    p[0] = Read (p[3])
    p[0].lineno = lexer.lineno

def p_declaration8(p):
    'declaration : RETURN expression'
    p[0] = Return(p[2])
    p[0].lineno = lexer.lineno

def p_declaration9(p):
    'declaration : ID LPAREN expressions_listop RPAREN'
    p[0] = call_func (p[1], p[3])
    p[0].lineno = lexer.lineno

def p_declaration10(p):
    'declaration : SKIP'
    p[0] = Skip()
    p[0].lineno = lexer.lineno

def p_declaration11(p):
    'declaration : BREAK'
    p[0] = Break()
    p[0].lineno = lexer.lineno

def p_declaration12(p):
    'declaration : BEGIN dec_list END'
    p[0] = p[2]

def p_error_empty_list(p):
    'declaration : BEGIN END'
    print ("Conjunto de declarationes vacias en linea %d" % lexer.lineno)

#if
def p_ifthen(p):
    'ifthen : IF relation THEN declaration %prec ELSE'
    p[0] = Ifthen( Condition(p[2]),Then(p[4]) )
    p[0].lineno = lexer.lineno

def p_ifthenelse(p):
    'ifthenelse : IF relation THEN declaration ELSE declaration'
    p[0] = Ifthenelse(Condition(p[2]),Then(p[4]),Else(p[6]))
    p[0].lineno = lexer.lineno

def p_errorifthen(p):
    'ifthen : IF relation declaration %prec ELSE'
    print ("Error line %d: missing then'" % lexer.lineno)
    #p[0] = Node("NodoIfthen", [Node('Condicion', [p[2]]), Node('Then', [p[3]])])

def p_errorifthenelse(p):
    'ifthen : IF relation declaration ELSE declaration'
    print ("Error line %d: missing then" % lexer.lineno)

#lista de claraciones
def p_dec_list1(p):
    'dec_list : declaration'
    p[0]= Dec_list([p[1]])

def p_dec_list2(p):
    'dec_list : dec_list SEMICOLON declaration'
    p[1].append(p[3])
    p[0]=p[1]

def p_dec_listerror(p):
    'dec_list : dec_list declaration'    
    print("Error line %d: Locals definition. Semicolon is missing" % lexer.lineno)
    p[1].append(p[2])
    p[0]=p[1]    

#ubication
def p_ubication1(p):
    'ubication : ID'
    p[0] = Ubication(p[1],True)
    p[0].lineno = lexer.lineno

def p_ubication2(p):
    'ubication : ID LSBRACKET expression RSBRACKET'
    p[0] = Ubication_vector(p[1],Position(p[3]))
    p[0].lineno = lexer.lineno

#expressiones
def p_expression1(p):
    'expression : expression PLUS expression'
    p[0] = Plus(p[1], p[3])
    p[0].lineno = lexer.lineno

def p_expression2(p):
    'expression : expression MINUS expression'
    p[0] = Minus(p[1], p[3])
    p[0].lineno = lexer.lineno

def p_expression3(p):
    'expression : expression TIMES expression'
    p[0] = Times(p[1], p[3])
    p[0].lineno = lexer.lineno

def p_expression4(p):
    'expression : expression DIVIDE expression'
    p[0] = Divide(p[1],p[3])
    p[0].lineno = lexer.lineno

def p_expression5(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = Unary_op('-',p[2])
    p[0].lineno = lexer.lineno

def p_expression6(p):
    'expression : PLUS expression'
    p[0] = Unary_op('+',p[2])

def p_expression7(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression8(p):
    'expression : ID LPAREN expressions_listop RPAREN'
    p[0] = call_func(p[1],p[3])
    p[0].lineno = lexer.lineno

def p_expression9(p):
    'expression : ID'
    p[0] = Id(p[1])
    p[0].lineno = lexer.lineno

def p_expression10(p):
    'expression : ID LSBRACKET expression RSBRACKET'
    p[0] = Vector(p[1],Position(p[3]))
    p[0].lineno = lexer.lineno

def p_expression11(p):
    'expression : number'
    p[0] = p[1]

def p_expression12(p):
    'expression : INT_TYPE LPAREN expression RPAREN'
    p[0] = Cast_int(p[3])
    p[0].lineno = lexer.lineno

def p_expression13(p):
    'expression : FLOAT_TYPE LPAREN expression RPAREN'
    p[0] = Cast_float(p[3])
    p[0].lineno = lexer.lineno

#Lista de expressiones
def p_expressions_listop1(p):
    'expressions_listop : expressions_list'
    p[0] = p[1]

def p_expressions_listop2(p):
    'expressions_listop : empty'
    p[0] = Empty_expr_list()
    p[0].lineno = lexer.lineno


def p_expressions_list1(p):
    'expressions_list : expression'
    p[0]= Expression_list( [p[1]])
    p[0].lineno = lexer.lineno

def p_expressions_list2(p):
    'expressions_list : expressions_list COMMA expression'
    p[1].append(p[3])
    p[0]=p[1]


def p_relation1(p):
    'relation : expression LT expression'
    p[0] = Binary_op('<', p[1],p[3])
    p[0].lineno = lexer.lineno

def p_relation2(p):
    'relation : expression LE expression'
    p[0] = Binary_op('<=', p[1],p[3])
    p[0].lineno = lexer.lineno

def p_relation3(p):
    'relation : expression GT expression'
    p[0] = BinaryOp('>',p[1],p[3])
    p[0].lineno = lexer.lineno

def p_relation4(p):
    'relation : expression GE expression'
    p[0] = Binary_op('>=',p[1],p[3])
    p[0].lineno = lexer.lineno

def p_relation5(p):
    'relation : expression EQ expression'
    p[0] = Binary_op('==',p[1],p[3])
    p[0].lineno = lexer.lineno

def p_relation6(p):
    'relation : expression NE expression'
    p[0] = Binary_op('!=',p[1],p[3])
    p[0].lineno = lexer.lineno

def p_relation7(p):
    'relation : relation AND relation'
    p[0] = Binary_op('and',p[1],p[3]])
    p[0].lineno = lexer.lineno

def p_relation8(p):
    'relation : relation OR relation'
    p[0] = Binary_op('or',p[1],p[3])
    p[0].lineno = lexer.lineno

def p_relation9(p):
    'relation : NOT relation'
    p[0] = Unary_op('not',p[2])
    p[0].lineno = lexer.lineno

def p_relation10(p):
    'relation : LPAREN relation RPAREN'
    p[0] = p[2]

def p_errorRelacion(p):
    'relation : error'
    print ("Error line:  %d" % lexer.lineno)

def p_number1(p):
    'number : INTEGER'
    p[0] = Integer(p[1])
    p[0].lineno = lexer.lineno

def p_number2(p):
    'number : FLOAT'
    p[0] = Float(p[1])
    p[0].lineno = lexer.lineno

def p_empty(p):
    'empty :'

# regla de error general
def p_error(p):
    if p:
        print ("Syntax error at line %d:  %s" % (lexer.lineno,p.type))

parser = yacc.yacc(debug=1)

# Build the parser
if __name__ == "__main__":
    f = open(sys.argv[1])
    s = f.read()
    lexer = mpaslex.make_lexer()
    result = parser.parse(s)
    if result:
        dump_tree(result)
