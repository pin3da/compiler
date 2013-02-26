#!/usr/bin/env python
# mpaslex.py
r'''
Proyecto 1 - Escribir un Lexer
==============================
En este primer proyecto, se va a escribir un sencillo lexer para un
lenguaje como mpascal.  El proyecto se presenta como codigo que se
debe leer y completar (este archivo).  Por favor, lea el contenido
completo de este archivo y cuidadosamente siga los pasos indicados
por los comentarios.

Resumen:
--------
El proceso del analisis lexico consiste en tomar una entrada y dividirla
en un flujo de tokens (simbolos). Cada token es como una palabra valida
del diccionario.  Esencialmente, la funcion del analizador lexico es
simplemente asegurar que el texto de entrada se compone de simbolos validos
antes de cualquier procesamiento adicional relacionado con el parsing 
(analisis sintatico).

Cada token esta definido por una expresion regular.  Por lo tanto, su
tarea principal en este primer proyecto es definir un conjunto de expresiones
regulares para el lenguaje.  El trabajo actual del analizador lexico es
manejado por PLY (http://www.dabeaz.com/ply).


Especificacion:
---------------
Su lexer debera reconocer los siguientes simbolos y tokens.  El nombre de la
izquierda es el nombre del token, el valor de la derecha es el texto coincidente.

Palabras Reservadas:
	CONST   : 'const'
	VAR	 : 'var'  
	PRINT   : 'print'
	FUNC	: 'func'
	EXTERN  : 'extern'

Identificadores:  (Las mismas reglas que para Python)
	ID	  : Texto que comience con una letra o '_', seguido de cualquier numero
			  numero de letras, digitos o guion bajo.

Operadores y Delimitadores:
	PLUS	: '+'
	MINUS   : '-'
	TIMES   : '*'
	DIVIDE  : '/'
	ASSIGN  : '='
	SEMI	: ';'
	LPAREN  : '('
	RPAREN  : ')'
	COMMA   : ','

Literales:
	INTEGER : '123'   (decimal)
			  '0123'  (octal)
			  '0x123' (hex)

	FLOAT   : '1.234'
			  '1.234e1'
			  '1.234e+1'
			  '1.234e-1'
			  '1e2'
			  '.1234'
			  '1234.'

	STRING  : '"Hola Mundo\n"'

Comentarios:  Deben ser ignorados por su analizador lexico
	 //			 Salta el resto de la linea
	 /* ... */	  Salta un bloque (anidacion no permitida)

Errores: Su lexer debera reportar los siguientes mensajes de error:

	 lineno: Ilegal char 'c'
	 lineno: Cadena no terminada
	 lineno: Comentario sin terminar
	 lineno: Codigo de escape malo en cadena '\..'

Pruebas
-------
Para el desarrollo inicial, intente ejecutar el lexer con un archivo de 
entrada de ejemplo como:

	 bash % python mpaslex.py sample.pas

Estudie cuidadosamente la salida del lexer y asegurese que tiene sentido.
Una vez que este razonablemente satisfecho con el resultado, trate de 
ejecutarlos con algunas pruebas mas dificiles:

	 bash % python mpaslex.py testlex1.pas
	 bash % python mpaslex.py testlex2.pas

Bonos: Que haria usted para convertir estas pruebas en pruebas unitarias
adecuadas
'''

# ----------------------------------------------------------------------
# El siguiente import carga la funcion errror(lineno,msg) que debe ser
# usada para reportar todos los mensajes de error emitidos por su lexer.
# Pruebas unitarias y otras caracteristicas del compilador se apoyaran
# en esta funcion.  Revise el archivo errors.py para mas documentacion
# acerca del mecanismo del control de errores.
from errors import error

# ----------------------------------------------------------------------
# Analizadores lexicos son definidos usando la libreria ply.lex
#
# Vea http://www.dabeaz.com/ply/ply.html#ply_nn3
from ply.lex import lex

# ----------------------------------------------------------------------
# Lista de token. Esta lista identifica la lista completa de nombres de
# token que deben ser reconocidos por su lexer.  No cambie ninguno de 
# estos nombres. Haciendolo se rompera las pruebas unitarias.

tokens = [
	# keywords
	'ID', 'CONST', 'VAR', 'PRINT', 'FUNC', 'EXTERN','BEGIN','DO','THEN',

	# Control flow
	'IF', 'ELSE', 'WHILE', 'READ', 'WRITE', 'PRINT','SKIP', 'RETURN',

	# Operators and delimiters
	'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
	'ASSIGN', 'SEMI', 'LPAREN', 'RPAREN', 'COMMA', 'COLON', 
	'LSBRACKET' , 'RSBRACKET','COLONEQUAL',

	# Boolean operators
	'LT', 'LE', 'GT', 'GE', 'LAND', 'LOR', 'LNOT',
	'EQ', 'NE',

	# Literals
	'INTEGER', 'FLOAT', 'STRING', 'BOOLEAN',
	#Types
    'INT_TYPE','FLOAT_TYPE','BOOLEAN_TYPE','STRING_TYPE',
	
]

# ----------------------------------------------------------------------
# Ignorando caracteres (whitespace)
#
# Los siguientes caracteres son ignorados completamente por el lexer.
# No lo cambie.

t_ignore = ' \t\r'

# Una o mas lineas en blanco
def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count('\n')

# Comentarios C-style (/* ... */)
def t_COMMENT(t):
	r'/\*(.|\n|\r|\t)*\*/'
	t.lexer.lineno += t.value.count('\n')
	
def t_PASCALCOMMENT(t):
	r'\{(.|\n|\r|\t)*\}'
	t.lexer.lineno += t.value.count('\n')

# Comentarios C++-style (//...)
def t_CPPCOMMENT(t):
	r'//.*\n'
	t.lexer.lineno += 1





# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : Escriba las regexps indicadas a continuacion ***
# 
# Tokens para simbolos sencillos: + - * / = ( ) ;

t_PLUS	  	= r'\+'
t_MINUS	 	= r'-'
t_TIMES	 	= r'\*'
t_DIVIDE	= r'/'
t_ASSIGN	= r'='
t_SEMI	 	= r';'
t_COLON	 	= r':'
t_COLONEQUAL= r':='
t_LPAREN	= r'\('
t_RPAREN	= r'\)'
t_LSBRACKET = r'\['
t_RSBRACKET = r'\]'
t_COMMA	 	= r','
t_LT		= r'<'
t_LE		= r'<='
t_EQ		= r'=='
t_GE		= r'>='
t_GT		= r'>'
t_NE		= r'!='
t_LAND	  	= r'&&'
t_LOR	   	= r'\|\|'
t_LNOT	  	= r'!'

# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : escriba las regexps y codigo adicional para ***
#
# Tokens para literales, INTEGER, FLOAT, STRING. 

# Constantes punto flotante.   Deben ser reconocidos numeros de punto
# flotante en formatos como se muestra en los ejemplos siguientes:
#
#   1.23, 1.23e1, 1.23e+1, 1.23e-1, 123., .123, 1e1, 0.
#
# El valor debe ser convertido a un float de Python cuando se analice
def t_FLOAT(t):
	r'((\d*\.\d+)([eE][-+]?\d+)?)|(\d+\.\d*)|(\d+)([eE][-+]?\d+)'
	t.value = float(t.value)			   # Conversion a float de Python
	return t

# Constantes enteras.  Se debe reconocer enteros en todos los formatos
# siguientes:
#
#	 1234			 (decimal)
#	 01234			(octal)
#	 0x1234 or 0X1234 (hex)
#
# El valor debe ser convertido a un int de Python cuando se analice.
def t_INTEGER(t):
	r'(?:0[xX]?)?\d+'
	# Conversion a int de Python
	if t.value.startswith(('0x','0X')):
		t.value = int(t.value,16)
	elif t.value.startswith('0'):
		t.value = int(t.value,8)
	else:
		t.value = int(t.value)
	return t
	
#	to avoid index out of bounds
#	Can return any non-digit charcter
def my_next(ostring,pos):
    if(pos < len(ostring)):
        return ostring[pos]
    return 'p'
# Constantes string.  Se debe reconocer texto entre comillas.
# Por ejemplo:
#
#	 "Hola Mundo"
#
# A las cadenas se les permite tener codigos de escape los cuales
# estan definidos por un backslash inicial.   Los siguientes 
# codigos backslash deben ser reconocidos:
#	  
#	   \n	= newline (10)
#	   \r	= carriage return (13) 
#	   \t	= tab (9)
#	   \\	= char baskslash (\)
#	   \"	= comilla (")
#	   \bhh  = codigo caracter byte hh  (h es un digito hex)
#
# Todas los otros codigos de escape deberan dar un error. Nota: las 
# literales de string *NO* comprenden el rango completo de codigos de
# caracter soportados por Python.
#
# El valor del token debe ser la cadena con todos los codigo de escape
# reemplazados por su correspondiente codigo de caracter raw.

escapes_not_b = r'nrt\"'
escapes = escapes_not_b + "b"
def _replace_escape_codes(t):
	not_error = True
	newval = ""
	ostring = t.value
	olen = len(t.value)
	i=-1
	while(i < olen -1):
		i+=1
		c = ostring[i]
		flag = False
		rval = ""
		if c=='"':
			error(t.lexer.lineno, "Premature end of String at '%s'" % i,filename=sys.argv[1])
			not_error = False
		elif c=='\\':
			c1 = my_next(ostring,i+1)
			c2 = my_next(ostring,i+2)
			c3 = my_next(ostring,i+3)
			#if c1 not in escapes_not_b:
			if c1 not in escapes:
				error(t.lexer.lineno,"Bad escape sequence code '%s'" % c1,filename=sys.argv[1])
				not_error = False
			else:
				if c1=='n':
					c='\n'
				elif c1=='r':
					c='\r'
				elif c1=='t':
					c='\t'
				elif c1=='\\':
					c='\\'
				elif c1=='"':
					c='"'
				elif c1=='b':
					if str.isdigit(c2) and str.isdigit(c3): 
						flag = True
						rval += (c1 + c2 +c3)
					else:
						error(t.lexer.lineno,"Bad escape sequence code '%s'" % c2+c3,filename=sys.argv[1])
						not_error =  False
			if(flag):
				newval += rval
				i= i+2
				
			else:
				newval += c
			i=i+1
		else:
			newval += c

	t.value = newval
	if (not_error):
		return t


def t_STRING(t):
	#r'".*"'
	r'"[^\n]*?(?<!\\)"'
	# Convierta t.value a una cadena con codigo de escape reemplazado por valor actual.
	t.value = t.value[1:-1]
	if(_replace_escape_codes(t) != None):	# Debe implementar arriba
		return t

def t_BOOLEAN(t):
	r'(true|false)'
	t.value = True if t.value=='true' else False
	return t

# ----------------------------------------------------------------------
# *** DEBE COMPLETAR: Escrina la regexp y agrege la palabra ***
#

# Identificadores y palabras reservadas.
# Coincidir un identificador raw.  Los identificadores siguen las mismas
# reglas de Python. Esto es, ellos comienzan con una letra o subrayado (_)
# y puede contener un numero arbitrario de letras, digitos o subrayado 
# despues de este.
def t_ID(t):
	r'[a-zA-Z_]\w*'
	t.type = reserved.get(t.value,'ID')
	return t

# *** DEBE IMPLEMENTAR ***
# Adicione codigo para coincidir con palabras reservadas como 'var', 'const',
# 'print', 'func', 'extern'

reserved = {
	'if':'IF',
	'else':'ELSE',
	'while':'WHILE',
	'var':'VAR',
	'const':'CONST',
	'do':'DO',
	'then' : 'THEN',
	#Podria ser fun
	'func':'FUNC',
	'extern':'EXTERN',
	'print':'PRINT',
	'begin':'BEGIN',
	'int':'INT_TYPE',
	'float': 'FLOAT_TYPE',
	'boolean': 'BOOLEAN_TYPE',
	'string': 'STRING_TYPE',
	'read':'READ', 
	'write':'WRITE', 
	'print':'PRINT',
	'skip':'SKIP',
	'return':'RETURN',
}

# En realidad este diccionario no se usa
operators = {
	r'+' : "PLUS",
	r'-' : "MINUS",
	r'*' : "TIMES",
	r'/' : "DIVIDE",
	r'=' : "ASSIGN",
	r';' : "SEMI",
	r'(' : "LPAREN",
	r')' : "RPAREN",
	r',' : "COMMA",
	r'<' : "LT",
	r'<=' : "LE",
	r'==' : "EQ",
	r'>=' : "GE",
	r'>' : "GT",
	r'!=' : "NE",
	r'&&' : "LAND",
	r'||' : "LOR",
	r'!' : "LNOT",
}


# ----------------------------------------------------------------------
# *** DEBE COMPLETAR : Agrege las regexps indicadas ***
#
# Manejo de error.  Las condiciones siguientes de error deben ser 
# manejadas por su analizador lexico.

# Caracteres ilegales (manejo errores generico)
def t_error(t):
	error(t.lexer.lineno,"Illegal character %r" % t.value[0],filename=sys.argv[1])
	t.lexer.skip(1)

# Comentario C-style no terminado
def t_COMMENT_UNTERM(t):
	r'/\*[.\n]*(?!\*/)'
	error(t.lexer.lineno,"unfinished commentary",filename=sys.argv[1])
	t.lexer.skip(len(t.value))
	t.lexer.lineno += t.value.count('\n')

# Literal de cadena no terminada
def t_STRING_UNTERM(t):
	r'"((\\")|[^"])*'
	error(t.lexer.lineno,"string literal not finished",filename=sys.argv[1])
	t.lexer.lineno += 1
	



# ----------------------------------------------------------------------
#				NO CAMBIE NADA DEBAJO DE ESTA PARTE
# ----------------------------------------------------------------------
def make_lexer():
	'''
	Funcion de utilidad para crear el objeto lexer
	'''
	return lex(optimize=1)

if __name__ == '__main__':
	import sys
	from errors import subscribe_errors

	if len(sys.argv) != 2:
		sys.stderr.write("Usage: %s filename\n" % sys.argv[0])
		raise SystemExit(1)

	lexer = make_lexer()
	with subscribe_errors(lambda msg: sys.stderr.write(msg+"\n")):
		lexer.input(open(sys.argv[1]).read())
		for tok in iter(lexer.token,None):
			sys.stdout.write("%s\n" % tok)
