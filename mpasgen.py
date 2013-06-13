import StringIO
from mpasast import *

data = StringIO.StringIO()
labelNumber=1

cont = -1
sp_cont = 64
l_cont = 0
t_cont = 0

def generate(file,top):
    print >>file, "! Creado por mpascal.py"
    print >>file, "! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)"
    print >>file, '\n     .section ".text"'
    print >>data, '\n     .section ".rodata"\n'
    emit_program(file,top)
    print >>file, data.getvalue()
    
def emit_program(file,root):
    print >>file,"\n! program"
    functions = root.func_list.functions    
    for fun in functions:
        emit_function(file,fun)

def emit_function(file,fun):
    print >>file, "\n! function: %s (start) " % fun.id
    print >>file, '\n .global %s' % fun.id
    f = StringIO.StringIO()

    ret_label = new_label()
    for statement in fun.block.declarations_list:
        if isinstance(statement, Return):
            emit_return(f,statement,ret_label)
        else:
            emit_statement(f, statement)


    stack = -64
    if not isinstance(fun.locals, Empty_locals):
        if isinstance(fun.locals, Local_fun):
            for var in fun.locals.local_fun:
                if isinstance(var,Function):
                    emit_function(file,var)
                elif isinstance(var.typename,Vector):
                    if isinstance(var.typename.length,Integer):
                        stack = stack - 4*var.typename.length.value
                    else:
                        print >>file, '     ! Lenght can not be calculated'
                else:
                    stack = stack - 4
        else:
            for var in fun.locals.local_var:
                if isinstance(var,Function):
                    emit_function(file,var)
                elif isinstance(var.typename,Vector):
                    if isinstance(var.typename.length,Integer):
                        stack = stack - 4*var.typename.length.value
                    else:
                        print >>file, '     ! Lenght can not be calculated'
                else:
                    stack = stack - 4
    
    falta = (stack%8)
    if falta != 0:
        stack = stack - (8-falta)
   
    print >>file, "     save %%sp, %d, %%sp" % stack
    print >>file, f.getvalue()
    
    print >>file, ret_label

    if(fun.id == 'main'):
        print >>file , "     mov 0, %o0 ! solamente aparece en main"
        print >>file , "     call _exit ! solamente aparece en main"
        print >>file , "     nop ! solamente aparece en main"
        
    print >>file, "     ret"
    print >>file, "     restore"
    
    print >>file, "\n! function: %s (end) \n" % fun.id

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
##    elif isinstance(st,Return):
##        emit_return(file,st)
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
    value = s.value
    label = new_label()
    # Drop a literal in the data segment
    print >>file, '! call flprint()' 

    print >>file, '     sethi %%hi(%s), %%o0'%label
    print >>file, '     or %%o0, %%lo(%s), %%o0'%label
    print >>file, '     call flprint'
    print >>file, '     nop'
    
    print >>data, '%s: .asciz "%s"' % (label, value)
    print >>file, "! print (end)"


def emit_read(file,s):
    print >>file, "\n! read (start)"
    loc = s.var_id

    if isinstance(loc,Ubication_vector):
        eval_expression(file, loc.Position.expr)
        print >>file, "!     index := pop"
        index = pop()
        print >>file, "!     read(%s[%%%s])"% (loc.id, index)
    else:
        print >>file, "!     read(%s)"% loc.value
        
    result = pop()

    print >>file, '! call flreadi(int)'
    print >>file, '     call flreadi'
    print >>file, '     nop'
    print >>file, '     st %%o0, %%%s'%result
        
    print >>file, "! read (end)"


def emit_write(file,s):
    print >>file, "! write (start)"
    eval_expression(file, s.value)
    print >>file, "!     expr := pop"
    print >>file, "!     write(expr)"
    print >>file, '!     call flwritei(int)'
    val = pop()
    print >>file, '     mov %%%s, %%o0'%val
    print >>file, '     call flwritei'
    print >>file, '     nop'
    print >>file, "! write (end)"

def emit_while(file,s):
    test = new_label()
    done = new_label()
    print >>file, "\n! while (start)"
    print >>file, "\n %s:\n" %test   
    cond = s.conditional
    then = s.then
    eval_rel(file,cond.relation)
    result = pop()
    print >> file, "     cmp %s, %%g0     ! relop:= pop"%result
    print >> file, "     be %s     ! if not relop: goto %s" %(done,done)
    print >> file, "     nop"
    for statement in then.declaration.declarations_list:
        emit_statement(file,statement)
    print >>file, "\n     ba  %s     ! goto %s" %(test, test)
    print >>file, '     nop'
    print >>file, "\n %s:" %done
    print >>file, "\n! while (end)"

def emit_ifthen(file,s):
    print >>file, "\n! ifthen (start)"
    done = new_label()
    cond = s.conditional
    then = s.then
    eval_rel( file, cond)
    result = pop()
    print >>file, "     cmp %s, g0     !cond:= pop"%result
    print >>file, "     be %s     ! goto %s"%(done,done)
    print >>file, "     nop"
    for statement in then._fields: 
        emit_statement(file,getattr(then, statement) )
    print >>file, "\n %s:"%done
    print >>file, "\n! ifthen (end)"


def emit_ifthenelse(file,s):
    print >>file, "\n! ifthenelse (start)"
    elseLabel = new_label()
    done = new_label()
    cond = s.conditional
    then = s.then
    _else = s._else
    eval_rel(file, cond)
    result = pop()
    print >>file, "     cmp %s, g0     ! cond:= pop"%result
    print >>file, "     be %s     ! if not cond: goto else"%elseLabel
    print >>file, "     nop"
    #then
    
    for statement in then._fields :
        emit_statement(file,getattr(then, statement) )
    
    print >>file, "     ba %s     ! if not cond: goto end:"%done   
    
    
    #else
    print >>file, "\n %s:     ! else:"%elseLabel
    for statement in _else._fields:
        emit_statement(file,getattr(_else, statement) )
        
    print >>file, "\n %s:     ! end:"%done
    print >>file, "! ifthenelse (end)"
    
    
def emit_assign(file,s):
    print >>file, "\n! assign (start)"

    ubication = s.ubication
    expr = s.value   
    result = pop()
    if isinstance(ubication,Ubication_vector):
        eval_expression(file, ubication.Position.expr)
        memdir_index = pop()
        print >>file, "     sll %s, 2, %s" % (memdir_index, memdir_index)
        print >>file, "     add %%fp, %s, %s" % (memdir_index ,memdir_index),
        print >>file, "     ! index := pop"
        eval_expression(file, expr)
        print >>file, "     st %s, [%s + offset]     ! %s[index] := pop" % (result ,memdir_index, ubication.id)
    else:
        eval_expression(file, expr)
        print >>file, "     st %s, [%%fp + offset]     ! %s := pop" % (result, ubication.value)
    print >>file, "! assign (end)"
    
    
def emit_return(file,s,ret_label):
    print >>file, "\n! return (start)"
    expr = s.value
    eval_expression(file, expr)
    memdir = pop()
    print >>file, "     mov %s, %%o0     ! expr := pop" % (memdir)
    print >>file, '     jmp %s     ! return(expr)'% ret_label
    print >>file, '     nop'
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
        memdir_left = pop()
        memdir_right = pop()
        memdir =push(file)
        if expr.op == '+' :
            print >>file, "     add %s, %s, %s     ! add"%(memdir_left, memdir_right, memdir)
          
        elif expr.op == '-':
            print >>file, "     sub %s, %s, %s     ! sub"%(memdir_left, memdir_right, memdir)
            
        elif expr.op == '*' :        
            print >>file, "     mov %s, %%o0"%(memdir_left)
            print >>file, "     call .mul     ! mul"
            print >>file, "     mov %s, %%o0"%(memdir_right)
            print >>file, "     mov %%o0, %s"%(memdir)
            
        elif expr.op == '/':
            print >>file, "     mov %s, %%o0"%(memdir_left)
            print >>file, "     call .div     ! div"
            print >>file, "     mov %s, %%o0"%(memdir_right)
            print >>file, "     mov %%o0, %s"%(memdir)

            
    elif isinstance(expr,Unary_op):
        eval_expression(file,expr.value)
        l = pop()
        tmp = push(file)
        if expr.op == "not":
            print >>file, "    neg %s, %s        ! -%s -> %s" %(l,tmp,l,tmp)
        elif expr.op == '-':
            print >>file, "     sub %s, %s, %s     ! Unary minus"%("%g0", l, l)
        else:
            print >>file, "    %s 0, %s, %s        ! %s %s -> %s" %(un_ops[expr.op],l,tmp,expr.op,l,tmp)
          
    
    elif isinstance(expr, Call_func):
        emit_funcall(file, expr)
        ###
        #dest = push(file)
        #print >>file, 'mov %%o0, %s'%dest ,
        #print >>file, '! push %s()' % expr.func_id
        # Esto se esta haciendo en funcall para que imprima los argumentos
        ####

    
    elif isinstance(expr, Id):
        print >>file , '     ld [%%fp + offset], %s     ! push %s'% (push(file),expr.value)
            
    elif isinstance(expr, Ubication_vector):
        pos = expr.Position
        eval_expression(file, pos.expr)
        result = pop()
        print >>file, "     sll %s, 2, %s" % (result,result)
        print >>file, "     add %%fp, %s, %s" % (result,result),
        print >>file, "     ! index := pop"        
        print >>file, "     ld [%s + offset], %s     ! push %s[index]" % (result, push(file), expr.id),
     
    elif isinstance(expr, Cast_int):
        pass
    
    elif isinstance(expr, Cast_float):
        pass
    
    elif isinstance(expr,Ubication):
        pass
        
    elif isinstance(expr,Integer):
        numb = expr.value
        memdir = push(file)
        if numb >= -4095 and numb <= 4095:
            print >>file, '     mov %d, %s'% (numb , memdir),
            print >>file, '     ! push constant value'
        else:
            label = new_label()
            print >>data, '     %s: .integer "%s"' % (label, numb)
            print >>file, '     sethi %%hi(%s), %%g1'%label
            print >>file, '     or %%g1, %%lo(%s), %%g1'%label
            print >>file, '     ld [%%g1], %s'%memdir
            
      
    elif isinstance(expr,Float):
        numb= expr.value
        memdir=push(file)
        label = new_label()
        print >>data, '     %s: .float "%s"' % (label, numb) 
        print >>file, '     sethi %%hi(%s), %%g1'%label
        print >>file, '     or %%g1, %%lo(%s), %%g1'%label
        print >>file, '     ld [%%g1], %s'%memdir 
    
    
    
def eval_rel(file,rel):
    if isinstance(rel, Binary_op):
        left = rel.left
        right = rel.right
        eval_expression(file,left)
        eval_expression(file,right)
        memdir_left = pop()
        memdir_right = pop()
        memdir = push(file)
        if rel.op == "<":
            print >>file, "     cmp %s, %s"%(memdir_left, memdir_right)
            label=new_label()
            print >>file, "     bl %s     ! <"% label
            print >>file, "     mov 1, %s"%(memdir)
            print >>file, "     mov 0, %s"%(memdir)
            print >>file, " %s:" % label
            
        elif rel.op == "<=":
            print >>file, "     cmp %s, %s"%(memdir_left, memdir_right)
            label=new_label()
            print >>file, "     ble %s     !<="% label
            print >>file, "     mov 1, %s"%(memdir)
            print >>file, "     mov 0, %s"%(memdir)
            print >>file, " %s:" % label
           
        elif rel.op == ">":
            print >>file, "     cmp %s, %s"%(memdir_left, memdir_right)
            label=new_label()
            print >>file, "     bg %s     ! >"% label
            print >>file, "     mov 1, %s"%(memdir)
            print >>file, "     mov 0, %s"%(memdir)
            print >>file, " %s:" % label
            
        elif rel.op == ">=":
            print >>file, "     cmp %s, %s"%(memdir_left, memdir_right)
            label=new_label()
            print >>file, "     bge %s     ! >="% label
            print >>file, "     mov 1, %s"%(memdir)
            print >>file, "     mov 0, %s"%(memdir)
            print >>file, " %s:" % label
            
        elif rel.op == "==":            
            print >>file, "     cmp %s, %s"%(memdir_left, memdir_right)
            label=new_label()
            print >>file, "     be %s     ! =="% label
            print >>file, "     mov 1, %s"%(memdir)
            print >>file, "     mov 0, %s"%(memdir)
            print >>file, " %s:" % label
        
        elif rel.op == "!=":
            print >>file, "     cmp %s, %s"%(memdir_left, memdir_right)
            label=new_label()
            print >>file, "     bne %s     ! !="% label
            print >>file, "     mov 1, %s"%(memdir)
            print >>file, "     mov 0, %s"%(memdir)
            print >>file, " %s:" % label
      
        elif rel.op == 'and':
            print >>file, "     and %s, %s, %s     ! and"%(memdir_left,memdir_right,memdir)
        
        elif rel.op == "or":
            print >>file, "     or %s, %s, %s     ! or"%(memdir_left,memdir_right,memdir)
            
    if isinstance(rel, Unary_op):
        if rel.type == "not":
            sub = rel.value
            eval_rel(file,sub)
            memdir_op=pop()
            memdir=push(file)
            print >>file, "!     not"
            print >>file, "     xor %s, 1, %s"%(memdir_op, memdir)     

def eval_funcall(file,s):

    args = s.varlist
    if isinstance(args,Expression_list):
        i=0
        for arg in args.expr:
            eval_expression(file,arg)
            ori = pop()
            print >>file, '     store %s, %%o%d'%(ori,i),
            print >>file, "     ! arg%d :=pop" %i
            i+=1
        
        print >>file, '     call .%s'%s.func_id
        
        dest = push(file)
        print >>file, '     mov %s, %%o0'%(dest),
        fun = "    ! push %s(" %s.func_id
        tam = len(args.expr)
        for j in (0,tam):
            fun += "arg%d" %j
            if j < tam:
                fun += ", "            
        fun += ")"
        print >>file,fun



def new_label():
    global labelNumber
    newL= ".L%d" %labelNumber
    labelNumber+=1
    return newL
    

def push(out):
    global l_cont
    global t_cont
    global sp_cont
    if l_cont < 8 and t_cont != 8:
        l = '%l'+str(l_cont)
        l_cont +=1        
    else:
        if l_cont == 8:
            l_cont = 0
            t_cont = 8
        l = '%l'+str(l_cont)
        print >> out, "     st %s, [%%fp -%d]" % (l, sp_cont)
        sp_cont +=4
        l_cont +=1        
    return l
    
def pop():
    global l_cont
    global t_cont
    global sp_cont
    if l_cont >= 0 and t_cont == 0:
        l_cont -=1
        l = '%l'+str(l_cont)
    else:
        l_cont = t_cont
        t_cont = 0
        l_cont -=1
        l = '%l'+str(l_cont)
    return l

