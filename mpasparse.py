# mpasparse.py

import ply.yacc as yacc

from errors import error

from mpaslex import tokens

from mpasast import *

def p_program(p):
	'''
	program : function
	'''
	p[0]=Program(p[1])

def p_program_1(p):
	'''
	program : program function
	'''
	p[1].append(p[2])
	p[0]=p[1]

def p_function(p):
	'''
	function : FUNC ID LPAREN args RPAREN locals BEGIN statement END
	'''
	p[0]=Function(p[4],p[6],p[8])

def p_function_1(p):
	'''
	function : FUNC ID LPAREN RPAREN locals BEGIN statement END
	'''
	p[0]=Function(None,p[6],p[8])

def p_args(p):
	'''
	args : var COMMA args	
	'''
 	p[3].append(p[1])
	p[0]=p[3]

def p_args_1(p):
	'''
	args : var
	'''
	p[0]=Args(p[1])

def p_locals(p):
	'''
	locals : varass SEMICOLON locals
	'''
	p[3].append(p[1]) #habr�a que hacer un nodo para esto
	p[0]=p[3]

def p_locals(p):
	'''
	locals : empty
	'''
	p[0]=Locals([])

def p_varass(p):
	'''
	varass : var
	'''
	p[0]=Varass(p[1]) #Hay que hacer un nodo pa esto

def p_varass_1(p):
	'''
	varass : assignation
	'''
	p[0]=Varass(p[1]) #Hay que hacer un nodo pa esto

def p_var(p):
	'''
	var : ID COLON INT_TYPE
	'''
	p[0]=Var(p[1], p[3])# no se si depronto sea redundante
	p[0].datatype=p[3] #No se si ya hay un nodo pa esto
	p[0].name=p[1]

def p_assignation_integer(p):
	'''
	assignation : ID COLONEQUAL INTEGER
	'''
	p[0]=Assignation(p[1], p[3])
	p[0].name=p[1]
	p[0].value=p[3]

def p_assignation_float(p):
	'''
	assignation : ID COLONEQUAL FLOAT
	'''
	p[0]=Assignation(p[1], p[3])
	p[0].name=p[1]
	p[0].value=p[3]	

def p_assignation_string(p):
	'''
	assignation : ID COLONEQUAL STRING
	'''
	p[0]=Assignation(p[1], p[3])
	p[0].name=p[1]
	p[0].value=p[3]	

def p_assignation_boolean(p):
	'''
	assignation : ID COLONEQUAL BOOLEAN
	'''
	p[0]=Assignation(p[1], p[3])
	p[0].name=p[1]
	p[0].value=p[3]	

def p_assignation_ID(p):
	'''
	assignation : ID COLONEQUAL ID
	'''
	p[0]=Assignation(p[1], p[3])

def p_assignation_expression(p):
	'''
	assignation : ID COLONEQUAL expression
	'''
	p[0]=Assignation(p[1], p[3])

def p_statement_1(p):
	'''
	statement : controlstructure statement
	'''
	p[2].append(p[1])
	p[0]=p[2]

def p_statement_2(p):
	'''
	statement : instruction statement
	'''
	p[2].append(p[1])
	p[0]=p[2]

def p_statement_3(p):
	'''
	statement : empty
	'''
	p[0]=Statement([])

def p_controlstructure_1(p):
		'''
		controlstructure : cif
		'''
		p[0]=Controlstructure(p[1])

def p_controlstructure_2(p):
		'''
		controlstructure : cwhile
		'''
		p[0]=Controlstructure(p[1])	

def p_cwhile_1(p):
	'''
	cwhile : WHILE LPAREN conditional RPAREN DO BEGIN statement END SEMICOLON
	'''
	p[0]=Cwhile(p[3], p[7])
	

def p_cwhile_2(p):
	'''
	cwhile : WHILE conditional DO BEGIN statement END SEMICOLON
	'''
	p[0]=Cwhile(p[2], p[5])

def p_cwhile_3(p):
	'''
	cwhile : WHILE RPAREN conditional LPAREN DO instruction 
	'''
	p[0]=Cwhile(p[3], p[5])

def p_cwhile_4(p):
	'''
	cwhile : WHILE conditional DO insruction
	'''
	p[0]=Cwhile(p[2], p[4])

def p_cif_1(p):
	'''
	cif : IF RPAREN conditional LPAREN THEN BEGIN statement END SEMICOLON
	'''
	p[0]=Cif(p[3], p[7])

def p_cif_2(p):
	'''
	cif : IF conditional THEN BEGIN statement END SEMICOLON
	'''
	p[0]=Cif(p[2], p[5])

def p_cif_3(p):
	'''
	cif : IF RPAREN conditional LPAREN THEN instruction
	'''
	p[0]=Cif(p[3], p[5])

def p_cif_4(p):
	'''
	cif : IF conditional THEN instruction
	'''
	p[0]=Cif(p[2], p[4])

def p_conditional_greater(p):
	'''
	conditional : expression GREATER expression
	'''
	p[0]= BinaryOperator('>', p[1], p[3])

def p_conditional_less(p):
	'''
	conditional : expression LESS expression
	'''
	p[0]= BinaryOperator('<', p[1], p[3])

def p_conditional_greater_equal(p):
	'''
	conditional : expression GREATEREQUAL expression
	'''
	p[0]= BinaryOperator('>=', p[1], p[3])

def p_conditional_less_equal(p):
	'''
	conditional : expression LESSEQUAL expression
	'''
	p[0]= BinaryOperator('<=', p[1], p[3])

def p_conditional_different(p):
	'''
	conditional : expression DIFFERENT expression
	'''
	p[0]= BinaryOperator('!=', p[1], p[3])

def p_conditional_different(p):
	'''
	conditional : expression DIFFERENT expression
	'''
	p[0]= BinaryOperator('!=', p[1], p[3])

def p_conditional_equivalent(p):
	'''
	conditional : expression EQUIVALENT expression
	'''
	p[0]= BinaryOperator('==', p[1], p[3])

def p_conditional_boolean(p):
	'''
	conditional : BOOLEAN
	'''
	p[0]= Boolean(p[1])	#no se si esto esta bien
	p[0].value=p[1]

def p_expression_plus(p):
	'''
	expression : expression PLUS prod
	'''
	p[0]=  BinaryOperator('+', p[1], p[3])

def p_expression_minus(p):
	'''
	expression : expression PLUS prod
	'''
	p[0]=  BinaryOperator('-', p[1], p[3])

def p_expression_prod(p):
	'''
	expression : prod
	'''
	p[0]=  Expression(p[1])	#de nuevo no se si sea correcto
	

def p_prod_multiply(p):
	'''
	prod : prod MULTIPLY term
	'''
	p[0]=  BinaryOperator('*', p[1], p[3])

def p_prod_divided(p):
	'''
	prod : prod DIVIDED term
	'''
	p[0]=  BinaryOperator('/', p[1], p[3])

def p_prod_term(p):
	'''
	expression : term
	'''
	p[0]=  Prod(p[1])	#de nuevo no se si sea correcto	

def p_error(p):
	if p:
		error(p.lineno, "Error de sintaxis en la linea")

if __name__=='__main__':
	import mpaslex
	import sys
	from errors import suscribe_errors
	lexer = mpaslex.make_lexer()
	parser = make_parser()

		
