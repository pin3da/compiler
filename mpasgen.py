def generate(file,top):
    print >>file, "! Creado por mpascal.py"
    print >>file, "! Manuel Pineda, Carlos Gonzalez, IS744 (2013-1)"
    
def emit_program(file,root):
	print >>file,"\n! program"
	functions = root.func_list
	for fun in functions:
		emit_function(file,fun)

def emit_function(file,fun):
	print >>file, "\n! function: %s (start) " % fun.id
	if fun.id == "main":
		print >>file, "\n		.global main"
	#print >>file, "%s:" %fun.leaf
	for statement in fun.block:
		emit_statement(file, statement)
	print >>file, "!\n function: %s (end) " % fun.leaf

######## Revisado hasta aqui ##############

def emit_statement(out,s):
  #terminar

def emit_print(out,s):
	print >>file, "\n! print (start)"

	print >>file, "! print (end)"

def emit_read(out,s):
	print >>file, "\n! read (start)"
	#loc = s.children[0]
	print >>file, "! read (end)"

def emit_write(out,s):
	print >>file, "! write (start)"
	expr = s.children[0]
	eval_expression(out,expr)
	print >>file, "! 	expr := pop"
	print >>file, "! 	write(expr)"
	print >>file, "! write (end)"

def emit_while(out,s):
	test=new_label()
	done=new_label()
	print >>file, "\n! while (start)"
	print >>file, "\n%s:\n" %test
	cond = s.children[0]
	then = s.children[1]
	eval_rel(out,cond.children[0])
	print >>file, "! 	relop:= pop"
	print >>file, "! 	if not relop: goto %s" %done
	for statement in then.children:
		emit_statement(out,statement)
	print >>file, "\n! goto %s" %test
	print >>file, "\n%s:" %done
	print >>file, "\n! while (end)"

def emit_ifthen(out,s):
	print >>file, "\n! ifthen (start)"
	cond = s.children[0]
	then = s.children[1]
	eval_rel(out,cond.children[0])
	print >>file, "! 	cond:= pop"
	print >>file, "! 	if not cond: goto end"
	for statement in then.children:
		emit_statement(out,statement)
	print >>file, "! end:"
	print >>file, "! ifthen (end)"

def emit_ifthenelse(out,s):
	print >>file, "\n! ifthenelse (start)"
	cond = s.children[0]
	then = s.children[1]
	else_ = s.children[2]
	#rel
	eval_rel(out,cond.children[0])
	print >>file, "! 	cond:= pop"
	print >>file, "! 	if not cond: goto else"
	#then
	for statement in then.children:
		emit_statement(out,statement)
	print >>file, "! goto end:"
	#else
	print >>file, "! else:"
	for statement in else_.children:
		emit_statement(out,statement)
	print >>file, "! end:"
	print >>file, "! ifthenelse (end)"

def emit_asign(out,s):
	print >>file, "\n! asign (start)"
	loc = s.children[0]
	expr = s.children[1]
	eval_expression(out,expr)
	print >>file, "! 	%s:= pop"% loc.leaf
	print >>file, "! asign (end)"

def emit_return(out,s):
	print >>file, "\n! return (start)"
	expr = s.children[0]
	eval_expression(out,expr)
	print >>file, "! 	expr := pop"
	print >>file, "! 	return(expr)"
	print >>file, "! return (end)"

def emit_funcall(out,s):
	print >>file, "\n! funcall (start)"
	eval_funcall(out,s)
	print >>file, "! funcall (end)"

def emit_skip(out,s):
	print >>file, "\n! skip (start)"
	print >>file, "! skip (end)"

def emit_break(out,s):
	print >>file, "\n! break (start)"
	print >>file, "! break (end)"

def eval_expression(out,expr):
	#menos unarios?
	#converInt/Float

    if expr.type in ('Entero','Float'):
		print >>file, "! 	push", expr.leaf

    elif expr.type == 'Id':
        print >>file, "! 	push", expr.leaf

    elif expr.type == 'Suma':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out,left)
        eval_expression(out,right)
        print >>file, "! 	add"

    elif expr.type == 'Resta':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out,left)
        eval_expression(out,right)
        print >>file, "! 	sub"

    elif expr.type == 'Multiplicacion':
        left = expr.children[0]
        right = expr.children[1]
        eval_expression(out,left)
        eval_expression(out,right)
        print >>file, "! 	mul"

    elif expr.type == 'Division':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>file, "! 	div"

    elif expr.type == 'Llamado a Funcion':
		eval_funcall(out,expr)

    elif expr.type == 'Vector':
		pos=expr.children[0]
		eval_expression(out,pos.children[0])
		print >>file, "! 	index := pop"
		print >>file, "! 	push %s[index]"%expr.leaf

def eval_rel(out,rel):
	if rel.type == "<":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>file, "! 	<"

	elif rel.type == "<=":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>file, "! 	<="

	elif rel.type == ">":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>file, "! 	>"

	elif rel.type == ">=":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>file, "! 	>="

	elif rel.type == "==":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>file, "! 	=="

	elif rel.type == "!=":
		left = rel.children[0]
		right = rel.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>file, "! 	!="
		#si el ! es comentario, que poner?

	elif rel.type == "and":
		left = rel.children[0]
		right = rel.children[1]
		eval_rel(out,left)
		eval_rel(out,right)
		print >>file, "! 	and"

	elif rel.type == "or":
		left = rel.children[0]
		right = rel.children[1]
		eval_rel(out,left)
		eval_rel(out,right)
		print >>file, "! 	or"

	elif rel.type == "not":
		sub = rel.children[0]
		eval_rel(out,sub)
		print >>file, "! 	not"

def eval_funcall(out,s):
	args = s.children[0]
	i=1
	for arg in args.children:
		eval_expression(out,arg)
		print >>file, "! 	arg%d :=pop" %i
		i+=1
	sAux = "! 	push %s(" %s.leaf
	length = len(args.children)
	for j in range(1,length+1):		
		sAux+="arg%d" %j
		if j<length:
			sAux+=", "			
	sAux+=")"
	print >>file,sAux

def new_label():
	global labelNumber
	newL= ".L%d" %labelNumber
	labelNumber+=1
	return newL
