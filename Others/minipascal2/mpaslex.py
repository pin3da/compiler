import ply.lex as lex
keywords = (
    'fun','begin','end','while','do','then','if', 'print','read','write', 'else','return','skip','break','int','float', 'or', 'and','not')

tokens = keywords + (
     'IGU', 'ASIG', 'SUMA','RESTA','MULTI','DIVIDIR',
     'PARI','PARD','MENQ','MENIG','MAYQ','MAYIG','DIF',
     'COMA','PYC', 'REAL','ENTERO', 'CADENA',
     'ID','DOSPUNT','CORI','CORD'
)

t_ignore = ' \t\r'


#Literales

t_SUMA      = r'\+'
t_RESTA     = r'-'
t_MULTI     = r'\*'
t_DIVIDIR   = r'/'
t_PARI      = r'\('
t_PARD      = r'\)'
t_CORI      = r'\['
t_CORD      = r'\]'
t_COMA      = r'\,'
t_DOSPUNT   = r':'
t_PYC       = r';'

#Comparadores logicos
t_MENQ      = r'<'
t_MENIG     = r'<='
t_MAYQ      =  r'>'
t_MAYIG     = r'>='
t_DIF       = r'!='

def t_IGU(t):
    r"=="
    return t

def t_ASIG(t):
    r":="
    return t

def t_ERRORIG(t):
    r"="
    print "Error lexico de igual en linea %d. La asignacion debe ser ':=' y la comparacion de igualdad debe ser '=='" % lexer.lineno
    pass

def t_REAL(t):
    r'((\d*\.\d+)([e|E][\+-]?\d+)?|([1-9]\d*[e|E][\+-]?\d+))'
    cerosIni=0
    s = str(t.value)
    for i in range(len(s)-1):
        if s[i]=='0':
            cerosIni+=1
        else:
            break
    if cerosIni>1:
        print "Error lexico en numero real en linea %d" % lexer.lineno
        t.lexer.skip(len(t.value))
    else:
        return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value
    return t

def t_ERRORID(t):
    r'[0-9][a-zA-Z]+'
    print("Error lexico en la linea %d, identificador no valido" % lexer.lineno)
    pass

def t_ENTERO(t):
    r'[1-9][0-9]*|0'
    return t

def t_CADENA(t):
    r'\"([^\\\n]|(\\[^\n]))*?\"'
    band=True
    s = str(t.value)
    for i in range(len(s)-1):
        if s[i]=='\\':
            if s[i+1]!= 'n' and s[i+1]!= '"' and s[i+1] != '\\':
                print("Error lexico en la linea %d, cadena no valida" % lexer.lineno)
                band=False
                break
    if band:
        return t
    t.lexer.skip(len(t.value))

def t_ERRORCAD(t):
    r' "\w* | \w*" '
    print("Error lexico en la linea %d, cadena no valida" % lexer.lineno)
    t.lexer.skip(len(t.value))
    pass

def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    pass

def t_ERRORCOMM1(t):    
    r'/\*.*'
    print("Error lexico en la linea %d, Comentario sin cerrar" % lexer.lineno)
    t.lexer.skip(len(t.value))
    pass


def t_NUEVALINEA(t):
    r'\n'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Error lexico. Caracter ilegal %s. Tipo de error: %s" % (t.value[0] , t.type))
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == "__main__":
    lex.runmain()

