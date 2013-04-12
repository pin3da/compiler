# mpasparse.py

import ply.yacc as yacc

from errors import error

from mpaslex import tokens

from mpasast import *

def p_program(p):
	'''
	program : function
			| function program
	'''
	if(len(p) == 2):
		p[0] = Program(p[1])
	else:
		p[2].append(p[1])
		p[0] = p[2]

def p_function(p):
	'''
	function : FUNC ID LPAREN arg_list RPAREN return_f locals block
			 | FUNC ID LPAREN RPAREN return_f locals block
	'''
	if(len (p) == 9):
		p[0] = Function(p[4],p[6],p[7],p[8])
	else:
		p[0] = Function(None,p[6],p[7],p[8])

def p_empty(p):
	'''
	empty :
	'''
	pass

def p_return_f(p):
	'''
	return_f : COLON type
			 | empty
	'''
	if(len(p) == 3):
		p[0] = p[2]
	else
		p[0] = None
		#Revisar.

def p_block(p):
	'''
	block: BEGIN statements END
	'''
	p[0] = Block(p[2])

def p_arg_list(p):
	'''
	arg_list : var COMMA arg_list
			 | var
	'''
	if(len(p) == 4 ):
		p[3].append(p[1])
		p[0] = p[1]
	else:
		p[0] = Var(p[1])


def p_locals(p):
	'''
	locals : local_list SEMICOLON locals
		   | empty
	'''
	if( len(p) == 4):
		p[3].append(p[1])
		p[0] = p[3]
	else:
		p[0] = None
		#Revisar

def p_local_list(p):
	'''
	local_list : var
			   | var_dec_as
	'''
	p[0] = p[1]


def p_var(p):
	'''
	var : ID COLON TYPE
	'''
	p[0] =  Var(p[1],p[3])
	# El type y name se definen en el constructor del nodo.
	# TYPE deberia ser una produccion.

def p_var_dec_as(p):
	'''
	var_dec_as : ID COLONEQUAL types
			   | ID COLONEQUAL expression
	'''
	p[0] = Var_dec_as(p[1],p[3])
	# Es mejor separarlas ?

def p_statement(p):
	'''
	statement : controlstructure SEMICOLON statement
			  | instruction SEMICOLON statement
			  | empty
	'''	
	if( len(p) == 4 ):
		p[3].append(p[1])
		p[0] = p[3]
	else:
		p[0] = None
		#revisar.

def p_controlstructure(p):
	'''
	controlstructure : WHILE  LPAREN conditional RPAREN DO block SEMICOLON
					 |  IF LPAREN conditional RPAREN THEN block else SEMICOLON
	'''
	if( len(p) == 6):
		p[0] = Cwhile(p[3],p[6])
	else:
		p[0] = Cif(p[3],p[6],p[7]) 

def p_else(p)
	'''
	else : ELSE statement
		 | empty
	'''
	if ( len(p) == 3):
		p[0] = Else(p[2])
	else:
		p[0] = None

def p_conditional(p):
	'''
	conditional :  bool_expr OR bool_expr
				|  bool_expr AND bool_expr
				|  NOT bool_expr
				|  bool_expr
	'''
	if( len(p) == 4):
		if(p[2] == '||' ):
			p[0] = Or(p[1], p[3])
		else:
			p[0] = And(p[1], p[3])
	elif (len(p) == 3):
		p[0] = Not(p[2])
	else:
		p[0] = p[1]
	#Se podria poner como binaryop, o dejarlo en varias clases.

def bool_expr(p):
	'''
	bool_expr : expression GREATER expression
			  | expression LESS expression
			  | expression GREATEREQUAL expression
			  | expression LESSEQUAL expression
			  | expression DIFFERENT expression
			  | expression EQUIVALENT expression
			  | BOOLEAN
	'''
	if (len (p) == 4):
		if(p[2] == '>' ):
			p[0] = BinaryOp(">",p[1],p[3])
		elif (p[2] == '<'):
			p[0] = BinaryOp("<",p[1],p[3])
		elif (p[2] == '>=' ):
			p[0] = BinaryOp(">=",p[1],p[3])
		elif (p[2] == '<='):
			p[0] = BinaryOp("<=",p[1],p[3])
		elif (p[2] == '!='):
			p[0] = BinaryOp("!=",p[1],p[3])
		else:
			p[0] = BinaryOp("==",p[1],p[3])
	else:
		p[0] = Boolean(p[1])

########
# BinaryOp para comparaciones, retorna boolean
# Operation para operaciones, retorna valor
########


def p_expression(p):
	'''
	expression : expression PLUS prod
			   | expression MINUS prod
			   | prod			   
	'''
	if(len(p) == 4):
		if(p[2]== '+'):
			p[0] = Operation("+",p[1],p[3])
		else:
			p[0] = Operation("-",p[1],p[3])
	else:
		p[0] =  Prod(p[1])

def p_prod(p):
	'''
	prod : prod TIMES term
	 	 | prod DIVIDE term
		 | term
	'''
	if(len(p) == 4):
		if(p[2]== '*'):
			p[0] = Operation("*",p[1],p[3])
		else:
			p[0] = Operation("/",p[1],p[3])
	else:
		p[0] =  Term(p[1])

############
# la expresion dentro de parentesis debe estar en expresion no en term, es decir,
# expression : LPAREN expression RPARENT
#			 | las otras cosas
#
# Que es INT_TYPE LPAREN ID RPAREN  y el otro?
# Para que los parentesis ?
###########

def p_term(p):
	'''
	term : ID
		 | FLOAT
		 | INTEGER
	'''
	#toca individual para crear los nodos adecuados


def p_return(p):
	'''
	return : RETURN expression
	'''
	p[0] = Return(p[2])

def p_print_d_e(p):
	'''
	print_d : PRINT LPARENT expression RPARENT
	'''
	p[0] = PrintExpression(p[3])

def p_print_d_s(p):
	'''
	print_d : PRINT LPARENT STRNG RPARENT
	'''
	p[0] = PrintString(p[3])

def p_call_d(p):
	'''
	call_d : ID LPAREN list_var RPARENT
	'''
	p[0] = Call_d(p[1],p[3])
	#Nombre y argumentos funcion

def list_var(p):
	'''
	list_var : ID list_var
			 | expression list_var
			 | empty
	'''
	#terminar, separar

def type(p):
	'''
	type : INT_TYPE
		 | FLOAT_TYPE
		 | STRING_TYPE
		 | BOOLEAN_TYPE
	'''
	#terminar, separar para crear nodos del tipo correspondiente

def line_if(p):
	'''
	line_if : IF bool_expr THEN instructrion
	'''
	p[0] =  Line_if(p[2],p[4])

def line_while(p):
	'''
	line_while : WHILE bool_expr DO instruction
	'''
	p[0] =  Line_while(p[2],p[4])

def assignation(p):
	'''
	assignation : ID EQUAL expression
	'''
	p[0] = Assignation(p[1],p[3])
	#se puede convertir en nodo var


def p_error(p):
	if p:
		error(p.lineno, "Error de sintaxis en la linea")

if __name__=='__main__':
	import mpaslex
	import sys
	from errors import suscribe_errors
	lexer = mpaslex.make_lexer()
	parser = make_parser()

		
