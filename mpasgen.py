import StringIO
from mpasast import *

data = StringIO.StringIO()
labelNumber=1

def generate(file,top):
    print >>file, "! Creado por mpascal.py"
    print >>file, "! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)"
    emit_program(file,top)
    print >>data, '\n .section ".rodata"'
    print >>file,data.getvalue()
    
def emit_program(file,root):
    print >>file,"\n! program"
    functions = root.func_list.functions
    for fun in functions:
        emit_function(file,fun)

def emit_function(file,fun):
    print >>file, "\n! function: %s (start) " % fun.id
    if fun.id == "main":
        print >>file, "\n        .global main"
    #print >>file, "%s:" %fun.leaf
    for statement in fun.block.declarations_list:
        emit_statement(file, statement)

    print >>file, "\n! function: %s (end) " % fun.id

def emit_statement(file, st):
    if isinstance(st,Print):
        emit_print(file,st)
    elif isinstance(st,Read):
        emit_read(file,st)
    elif isinstance(st,Write):
        emit_write(file,st)
    elif isinstance(st,While):
       emit_while(file,st)
    elif isinstance(st,Ifthen):
        emit_ifthen(file,st)
    elif isinstance(st,Ifthenelse):
        emit_ifthenelse(file,st)
    elif isinstance(st,Assignation):
        emit_assign(file,st)
    elif isinstance(st,Return):
        emit_return(file,st)
    elif isinstance(st,Call_func):
        emit_funcall(file,st)
    elif isinstance(st,Skip):
        emit_skip(file,st)
    elif isinstance(st,Break):
        emit_break(file,st)
    elif isinstance(st,Dec_list):
        for statement in st.declarations_list:
            emit_statement(file,statement)



def emit_print(file,s):
    print >>file, "\n! print (start)"
    print >>file, '!     print(%s)'% s.value
    print >>file, "! print (end)"


def emit_read(file,s):
    print >>file, "\n! read (start)"
    loc = s.var_id

    if isinstance(loc,Ubication_vector):
        eval_expression(file, loc.Position.expr)
        print >>file, "!     index := pop"
        print >>file, "!     read(%s[index])"% loc.id
    else:
        print >>file, "!     read(%s)"% loc.value
        
    print >>file, "! read (end)"


def emit_write(file,s):
    print >>file, "! write (start)"
    eval_expression(file, s.value)
    print >>file, "!     expr := pop"
    print >>file, "!     write(expr)"
    print >>file, "! write (end)"

def emit_while(file,s):
    test = new_label()
    done = new_label()
    print >>file, "\n! while (start)"
    print >>file, "\n%s:\n" %test   
    

    cond = s.conditional
    then = s.then
    eval_rel(file,cond.relation)
    print >>file, "!     relop:= pop"
    print >>file, "!     if not relop: goto %s" %done

    
    for statement in then.declaration.declarations_list:
        emit_statement(file,statement)
    
    print >>file, "\n! goto %s" %test
    print >>file, "\n%s:" %done
    print >>file, "\n! while (end)"

def emit_ifthen(file,s):
    print >>file, "\n! ifthen (start)"
    
    cond = s.conditional
    then = s.then
    eval_rel( file, cond)
    
    print >>file, "!     cond:= pop"
    print >>file, "!     if not cond: goto end"
    for statement in then._fields:
        emit_statement(file,getattr(then, statement) )
    print >>file, "! end:"
    print >>file, "! ifthen (end)"


def emit_ifthenelse(file,s):
    print >>file, "\n! ifthenelse (start)"
    cond = s.conditional
    then = s.then
    _else = s._else
    eval_rel(file, cond)
    print >>file, "!     cond:= pop"
    print >>file, "!     if not cond: goto else"
    #then
    
    for statement in then._fields :
        emit_statement(file,getattr(then, statement) )
        
    print >>file, "! goto end:"
    
    #else
    print >>file, "! else:"
    
    for statement in _else._fields:
        emit_statement(file,getattr(_else, statement) )
        
    print >>file, "! end:"
    print >>file, "! ifthenelse (end)"
    
    
def emit_assign(file,s):
    print >>file, "\n! assign (start)"

    ubication = s.ubication
    expr = s.value   
    if isinstance(ubication,Ubication_vector):
        eval_expression(file, ubication.Position.expr)
        print >>file, "!     index := pop"
        eval_expression(file, expr)
        print >>file, "!     %s[index]:= pop"% ubication.id
    else:
        eval_expression(file, expr)
        print >>file, "!     %s:= pop"% ubication.value
    print >>file, "! assign (end)"
    
    
def emit_return(file,s):
    print >>file, "\n! return (start)"
    expr = s.value
    eval_expression(file, expr)
    
    print >>file, "!     expr := pop"
    print >>file, "!     return(expr)"
    print >>file, "! return (end)"
    
    
def emit_funcall(file,s):
    print >>file, "\n! funcall (%s) (start)"%s.func_id
    eval_funcall(file,s)
    print >>file, "! funcall (end)"
    
    
def emit_skip(file,s):
    print >>file, "\n! skip (start)"
    print >>file, "! skip (end)"
    
def emit_break(file,s):
    print >>file, "\n! break (start)"
    print >>file, "! break (end)"
    
    
def eval_expression(file,expr):
    
    if ( isinstance(expr, Binary_op)):
        left = expr.left
        right = expr.right
        eval_expression(file,left)
        eval_expression(file,right)
        if expr.op == '+' :
          print >>file, "!     add"
        elif expr.op == '-':
            print >>file, "!     sub"
        elif expr.op == '*' :        
            print >>file, "!     mul"
        elif expr.op == '/':
            print >>file, "!     div"

            
    elif isinstance(expr,Unary_op):
        pass
    
    elif isinstance(expr, Call_func):
        emit_funcall(file, expr)
        print >>file, '! push %s()' % expr.func_id

    
    elif isinstance(expr, Id):
        print >>file , '!     push', expr.value
            
    elif isinstance(expr, Ubication_vector):
        pos = expr.Position
        eval_expression(file, pos.expr)
        print >>file, "!     index := pop"
        print >>file, "!     push %s[index]" % Ubication_vector.id
    
    elif isinstance(expr, Cast_int):
        pass
    
    elif isinstance(expr, Cast_float):
        pass
    
    elif isinstance(expr,Ubication):
        pass
    
def eval_rel(file,rel):
    if isinstance(rel, Binary_op):
        left = rel.left
        right = rel.right
        eval_expression(file,left)
        eval_expression(file,right)
        if rel.op == "<":
            print >>file, "!     <"
            
        elif rel.op == "<=":
           print >>file, "!     <="
           
        elif rel.op == ">":
            print >>file, "!     >"
            
        elif rel.op == ">=":
            print >>file, "!     >="
            
        elif rel.op == "==":
           print >>file, "!     =="
        
        elif rel.type == "!=":
            print >>file, "!     !="
      
        elif rel.op == 'and':
            print >>file, "!     and"
        
        elif rel.op == "or":
            print >>file, "!     or"
            
    if isinstance(rel, Unary_op):
        if rel.type == "not":
            sub = rel.children[0]
            eval_rel(file,sub)
            print >>file, "!     not"

def eval_funcall(file,s):
    print >>file, "call_func"
    '''
    args = s.varlist
    i=1
    
    ###
    # Este for esta malo
    ###
    for arg in args.children:
        eval_expression(file,arg)
        print >>file, "!     arg%d :=pop" %i
        i+=1
    sAux = "!     push %s(" %s.leaf
    length = len(args.children)
    for j in range(1,length+1):        
        sAux+="arg%d" %j
        if j<length:
            sAux+=", "            
    sAux+=")"
    print >>file,sAux
    '''
    pass

def new_label():
    global labelNumber
    newL= ".L%d" %labelNumber
    labelNumber+=1
    return newL

