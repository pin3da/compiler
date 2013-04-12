# mpasparse.py

import ply.yacc as yacc

from errors import error

from mpaslex import tokens

from mpasast import *


#########
# Se agrega nodo initial para tener una unica raiz.
#########

precedence = (
		('left', 'OR'),
		('left', 'AND'),
		('left', 'NOT'),
		('left', 'PLUS','MINUS'),
		('left', 'TIMES','DIVIDE'),
        ('right', 'ELSE'),
)

def p_initial(p):
    '''
    initial : program
    '''
    p[0] = Program(p[1])

def p_program(p):
    '''
    program : function
            | function program
    '''
    if(len(p) == 2):
        p[0] = [ p[1] ] 
    else:
        p[2].append( p[1] )
        p[0] = p[2]

def p_function(p):
    '''
    function : FUNC ID LPAREN arg_list RPAREN return_f locals block
             | FUNC ID LPAREN RPAREN return_f locals block
    '''
    if(len (p) == 9):
        p[0] = Function(p[4],p[6],p[7],p[8])
    else:
        p[0] = Function([],p[6],p[7],p[8])

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
    else:
        p[0] = Empty()

def p_block(p):
    '''
    block : BEGIN statement END
    '''
    p[0] = Block(p[2])

def p_arg_list(p):
    '''
    arg_list : var COMMA arg_list
             | var
    '''
    if(len(p) == 4 ):
        p[3].append(Arg_list( p[1]) )
        p[0] = p[3]
    else:
        p[0] = [ Arg_list(p[1]) ]


def p_locals(p):
    '''
    locals : local_list SEMICOLON locals
           | empty
    '''
    if( len(p) == 4):
        p[3].append( Locals(p[1]) )
        p[0] = p[3]
    else:
        p[0] = []

def p_local_list(p):
    '''
    local_list : var
               | var_dec_as
    '''
    p[0] = p[1]


def p_var(p):
    '''
    var : ID COLON type
    '''
    p[0] =  Var(p[1],p[3])

def p_var_dec_as(p):
    '''
    var_dec_as : ID COLONEQUAL type 
               | ID COLONEQUAL expression
    '''
    p[0] = Var_dec_as(p[1],p[3])
    #En el constructor del nodo podemos usar "isinstance(segundo_argumento, Clase)"

def p_statement(p):
    '''
    statement : controlstructure SEMICOLON statement 
              | instruction SEMICOLON statement
              | empty
    '''    
    if( len(p) == 4 ):
        p[3].append( p[1] ) # aca no se crea un nodo porque controlstructure se encarga de eso
        p[0] = p[3]
    else:
        p[0] = [ ]

def p_controlstructure(p):
    '''
    controlstructure : WHILE  LPAREN conditional RPAREN DO block SEMICOLON
                     |  IF LPAREN conditional RPAREN THEN block else SEMICOLON
    '''
    if( len(p) == 6):
        p[0] = Cwhile(p[3],p[6])
    else:
        p[0] = Cif(p[3],p[6],p[7]) 

def p_instruction(p):
    '''
        instruction : write_d
                    | read_d
                    | line_if
                    | line_while
                    | return_d
                    | print_d
                    | assignation
                    | SKIP
                    | BREAK
                    | call_d
    '''
    p[0] = Instruction(p[1])

def p_else(p):
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
        if(p[2] == '|' ):
            p[0] = BinaryOp('||', p[1], p[3])
        else:
            p[0] = BinaryOp('&&', p[1], p[3])
    elif (len(p) == 3):
        p[0] = UnaryOp('!',p[2])
    else:
        p[0] = Bool_expr( p[1] )
    
def p_bool_expr(p):
    '''
    bool_expr : expression GT expression
              | expression LT expression
              | expression GE expression
              | expression LE expression
              | expression NE expression
              | expression EQ expression
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
               | LPAREN expression RPAREN
               | MINUS expression 
               | prod               
    '''
    if(len(p) == 4):
        if(p[2]== '+'):
            p[0] = Operation("+",p[1],p[3])
        elif (p[2] == '-'):
            p[0] = Operation("-",p[1],p[3])
        else:
            p[0] = p[2]

    elif(len (p) == 3):
        p[0] = UnaryOp('-',p[2])
        p[0] = p[1]

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
        p[0] =  p[1]

def p_term(p):
    '''
    term : ID
         | FLOAT
         | INTEGER
    '''
    p[0] = Term( p[1] ) #esto no puede ser term entonces cambie los de arriba

def p_return_d(p):
    '''
    return_d : RETURN expression
		   | RETURN ID 
    '''
    p[0] = Return(p[2]) 

def p_write_d(p):
    '''
    write_d : WRITE LPAREN expression RPAREN
            | WRITE LPAREN STRING RPAREN
    '''
    p[0] = Write_d(p[3])

def p_read_d(p):
    '''
    read_d : READ LPAREN ID RPAREN
    '''
    p[0] = Read_d(p[3])


def p_print_d(p):
    '''
    print_d : PRINT LPAREN expression RPAREN
            | PRINT LPAREN STRING RPAREN
            | PRINT LPAREN ID RPAREN
    '''
    p[0] = Print_d(p[3])

def p_call_d(p):
    '''
    call_d : ID LPAREN list_var RPAREN
    '''
    p[0] = Call_d(p[1],p[3])

def p_list_var(p):
    '''
    list_var : ID list_var
             | expression list_var
             | empty
    '''
    if( len(p) == 3):
        p[2].append(p[1])
        p[0] = p[2]
    else:
        p[0] = [ ]


def p_type(p):
    '''
    type : INT_TYPE
         | FLOAT_TYPE
         | STRING_TYPE
         | BOOLEAN_TYPE
    '''
    p[0] = Type(p[1])

def p_line_if(p):
    '''
    line_if : IF conditional THEN instruction
    '''
    p[0] =  Line_if(p[2],p[4])

def p_line_while(p):
    '''
    line_while : WHILE conditional DO instruction
    '''
    p[0] =  Line_while(p[2],p[4])

def p_assignation(p):
    '''
    assignation : ID EQ expression
    '''
    p[0] = Assignation(p[1],p[3])
    #se puede convertir en nodo var, a esto le faltan cosas: ID=ID, faltan var_dec_as vendrian siendo ctes


def p_error(p):
    if p:
        error(p.lineno, "Error de sintaxis en la linea")

def make_parser():
    "Funcion para crear parser"
    return yacc.yacc()

if __name__=='__main__':
    import mpaslex
    import sys
    from errors import *
       
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s filename\n" % sys.argv[0])
        raise SystemExit(1)
    
    f = open(sys.argv[1])
    s = f.read()

    lexer = mpaslex.make_lexer()
    parser = make_parser()
    result = parser.parse(s)
    if result :
        #Plot
        print ("ok")
    else:
        print ("wrong")

    
