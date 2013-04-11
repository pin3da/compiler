import StringIO
data = StringIO.StringIO()

labelNumber=1

def generate(out,top):
	print >>out, "! Creado por mpascal.py"
	print >>out, "! Steven, IS744 (2012-1)"
	emit_program(out,top)
	print >>data, '\n 	.section ".rodata"'
	print >>out,data.getvalue()

def emit_program(out,top):
	print >>data,"\n! program"
	funciones = top.children[0]
	for fun in funciones.children:
		emit_function(out,fun)

def emit_function(out,fun):
	print >>data,"\n! function: %s (start) " % fun.leaf
	if fun.leaf == "main":
		print >>data,"\n		.global main"
	print >>data,"%s:" %fun.leaf
	for statement in fun.children:
		emit_statement(out,statement)
	print >>data,"!\n function: %s (end) " % fun.leaf

def emit_statement(out,s):
    if s.type == 'Print':
		emit_print(out,s)
    elif s.type == 'Read':
        emit_read(out,s)
    elif s.type == 'Write':
        emit_write(out,s)
    elif s.type == 'While':
	   emit_while(out,s)
    elif s.type == 'NodoIfThen':
		emit_ifthen(out,s)
    elif s.type == 'NodoIfThenElse':
    	emit_ifthenelse(out,s)
    elif s.type == 'Asignacion':
		emit_asign(out,s)
    elif s.type == 'Return':
		emit_return(out,s)
    elif s.type == 'Llamado a funcion':
    	emit_funcall(out,s)
    elif s.type == 'Skip':
		emit_skip(out,s)
    elif s.type == 'Break':
		emit_break(out,s)
    elif s.type == 'Declaraciones':
		for statement in s.children:
			emit_statement(out,statement)

def emit_print(out,s):
	print >>data, "\n! print (start)"

	print >>data, "! print (end)"

def emit_read(out,s):
	print >>data, "\n! read (start)"
	#loc = s.children[0]
	print >>data, "! read (end)"

def emit_write(out,s):
	print >>data, "! write (start)"
	expr = s.children[0]
	eval_expression(out,expr)
	print >>data, "! 	expr := pop"
	print >>data, "! 	write(expr)"
	print >>data, "! write (end)"

def emit_while(out,s):
	test=new_label()
	done=new_label()
	print >>data, "\n! while (start)"
	print >>data, "\n%s:\n" %test
	cond = s.children[0]
	then = s.children[1]
	eval_rel(out,cond.children[0])
	print >>data, "! 	relop:= pop"
	print >>data, "! 	if not relop: goto %s" %done
	for statement in then.children:
		emit_statement(out,statement)
	print >>data, "\n! goto %s" %test
	print >>data, "\n%s:" %done
	print >>data, "\n! while (end)"

def emit_ifthen(out,s):
	print >>data, "\n! ifthen (start)"
	cond = s.children[0]
	then = s.children[1]
	eval_rel(out,cond.children[0])
	print >>data, "! 	cond:= pop"
	print >>data, "! 	if not cond: goto end"
	for statement in then.children:
		emit_statement(out,statement)
	print >>data, "! end:"
	print >>data, "! ifthen (end)"

def emit_ifthenelse(out,s):
	print >>data, "\n! ifthenelse (start)"
	cond = s.children[0]
	then = s.children[1]
	else_ = s.children[2]
	#rel
	eval_rel(out,cond.children[0])
	print >>data, "! 	cond:= pop"
	print >>data, "! 	if not cond: goto else"
	#then
	for statement in then.children:
		emit_statement(out,statement)
	print >>data, "! goto end:"
	#else
	print >>data, "! else:"
	for statement in else_.children:
		emit_statement(out,statement)
	print >>data, "! end:"
	print >>data, "! ifthenelse (end)"

def emit_asign(out,s):
	print >>data, "\n! asign (start)"
	loc = s.children[0]
	expr = s.children[1]
	eval_expression(out,expr)
	print >>data, "! 	%s:= pop"% loc.leaf
	print >>data, "! asign (end)"

def emit_return(out,s):
	print >>data, "\n! return (start)"
	expr = s.children[0]
	eval_expression(out,expr)
	print >>data, "! 	expr := pop"
	print >>data, "! 	return(expr)"
	print >>data, "! return (end)"

def emit_funcall(out,s):
	print >>data, "\n! funcall (start)"
	eval_funcall(out,s)
	print >>data, "! funcall (end)"

def emit_skip(out,s):
	print >>data, "\n! skip (start)"
	print >>data, "! skip (end)"

def emit_break(out,s):
	print >>data, "\n! break (start)"
	print >>data, "! break (end)"

def eval_expression(out,expr):
	#menos unarios?
	#converInt/Float

    if expr.type in ('Entero','Float'):
		print >>data, "! 	push", expr.leaf

    elif expr.type == 'Id':
        print >>data, "! 	push", expr.leaf

    elif expr.type == 'Suma':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out,left)
        eval_expression(out,right)
        print >>data, "! 	add"

    elif expr.type == 'Resta':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out,left)
        eval_expression(out,right)
        print >>data, "! 	sub"

    elif expr.type == 'Multiplicacion':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out,left)
        eval_expression(out,right)
        print >>data, "! 	mul"

    elif expr.type == 'Division':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>data, "! 	div"

    elif expr.type == 'Llamado a Funcion':
		eval_funcall(out,expr)

    elif expr.type == 'Vector':
		pos=expr.children[0]
		eval_expression(out,pos.children[0])
		print >>data, "! 	index := pop"
		print >>data, "! 	push %s[index]"%expr.leaf

def eval_rel(out,rel):
	if rel.type == "<":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>data, "! 	<"

	elif rel.type == "<=":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>data, "! 	<="

	elif rel.type == ">":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>data, "! 	>"

	elif rel.type == ">=":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>data, "! 	>="

	elif rel.type == "==":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>data, "! 	=="

	elif rel.type == "!=":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>data, "! 	!="
		#si el ! es comentario, que poner?

	elif rel.type == "and":
		left = rel.children[0]
		right = rel.children[1]
		eval_rel(out,left)
		eval_rel(out,right)
		print >>data, "! 	and"

	elif rel.type == "or":
		left = rel.children[0]
		right = rel.children[1]
		eval_rel(out,left)
		eval_rel(out,right)
		print >>data, "! 	or"

	elif rel.type == "not":
		sub = rel.children[0]
		eval_rel(out,sub)
		print >>data, "! 	not"

def eval_funcall(out,s):
	args = s.children[0]
	i=1
	for arg in args.children:
		eval_expression(out,arg)
		print >>data, "! 	arg%d :=pop" %i
		i+=1
	sAux = "! 	push %s(" %s.leaf
	length = len(args.children)
	for j in range(1,length+1):		
		sAux+="arg%d" %j
		if j<length:
			sAux+=", "			
	sAux+=")"
	print >>data,sAux

def new_label():
	global labelNumber
	newL= ".L%d" %labelNumber
	labelNumber+=1
	return newL