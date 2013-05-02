
import sys
import mpasparse
import mpaslex

class Table:
    def __init__(self,name,lineno,parent=None):
         self.name = name
         self.vars = [ ]
         self.subTables = [ ]
         self.parent = parent
         self.type = "Void"
         self.numArgs=0
         self.argTypes = []
         self.lineno=lineno

    def appendArgType (self,tipo):
        self.argTypes.append(tipo)

    def appendVar (self, var):
        self.vars.append(var)

    def hasVar (self,varName):
        for var in self.vars:
            if varName==var.name:
                return var
        return None

    def searchVarUp (self,varName):
        var=self.hasVar(varName)
        if var!=None:
            return var
        if not self.parent:
            return None
        return self.parent.searchVarUp(varName)

    def appendTable (self, newTab):
        self.subTables.append(newTab)

    def hasTable(self,tableName):
        for table in self.subTables:
            if tableName==table.name:
                return table
        return None

    def searchTableUp (self,tableName):
        table =self.hasTable(tableName)
        if table!=None:
            return table
        if not self.parent:
            return None
        return self.parent.searchTableUp(tableName)

class Var:
    def __init__(self,name,type,lineno,size=0):
         self.name = name
         self.type = type
         self.size = size
         self.lineno = lineno

#Funcion principal, analiza las declaraciones
#No tiene retorno
def semAnalysis(node,table):

    for i in range(len(node.children)):
        c = node.children[i]
        if c.type=="Funcion":
            addFunAndAnalyse(c,table)

        elif c.type=="Argumentos":
            for defvar in c.children:
                table.numArgs+=1
                addDefVar(defvar,table)
                table.appendArgType(defvar.children[0].leaf)

        elif c.type=="Variables Locales":
            for defvar in c.children:
                if(defvar.type=="Funcion"):
                    addFunAndAnalyse(defvar,table)
                elif(table.hasVar(defvar.leaf)!=None):
                    print "Error Semantico! La variable %s esta siendo redefinida. Linea: %d" %(defvar.leaf,defvar.lineno)
                elif(table.searchVarUp(defvar.leaf)!=None):
                    print "Precaucion! Se esta redefiniendo una variable mas global (%s), el programa tomara la mas interna pero esto puede crear confusiones en su codigo. Linea: %d" %(defvar.leaf,defvar.lineno)
                else:
                    addDefVar(defvar,table)


        elif c.type=="Asignacion":
            #print "linea: %d" %c.lineno
            #print "Ubicacion: %s"% c.children[0].type            
            location=c.children[0] #Asignacion/Ubicacion            
            locType= analyseLoc(location,table)      
            #print "Expresion: %s"% c.children[1].type      
            exp=c.children[1] #Asignacion/Expresion            
            expType=analyseExp(exp,table)
            #print "\n"
            #print "locType:%s  expType:%s" %(locType,expType)
            if locType!=None and expType != None and not compareTypes(locType,expType):
	               print "Error Semantico! se esta asignando un '%s' a la variable '%s' de tipo '%s'. Linea: %d" %(expType,location.leaf,locType, location.lineno)            

        elif c.type=="While":
            analyseRel(c.children[0].children[0],table) #while/'Condicion'/Condicion
            semAnalysis(c.children[1],table) #while/'Then'/Declaracion

        elif c.type=="NodoIfThen":
            analyseRel(c.children[0].children[0],table) #if/Relacion            
            semAnalysis(c.children[1],table) #then/Declaracion

        elif c.type=="NodoIfThenElse":
            analyseRel(c.children[0].children[0],table) #if/Relacion            
            semAnalysis(c.children[1],table) #then/Declaracion
            semAnalysis(c.children[2],table) #else/Declaracion

        elif c.type=="Write":
		    analyseExp(c.children[0],table)

        elif c.type=="Read":
		    analyseLoc(c.children[0],table)

        elif c.type=="Llamado a Funcion":
            analyseFunCall(c,table)

        elif c.type=="Return":
            t=analyseExp(c.children[0],table)
            if t != None:
                if table.type=="Void":
                    table.type=t
                elif table.type!=t:
                    print "Error Semantico! Una funcion no debe retornar tipos diferentes de datos (%s y %s) en funcion %s. Linea: %d" %(table.type,t,table.name,table.lineno)

        else:
            semAnalysis(c,table)

#Agrega una variable, partir de un nodo DefVar
#No tiene retorno
def addDefVar(defvar,table):
    varname=defvar.leaf
    child = defvar.children[0]
    if(child.type=="tipo"): #En este caso es un entero o un float
        newVar=Var(varname,child.leaf,child.lineno)
        table.appendVar(newVar)
    else : #sino, deberia ser un vector y analizo la posicion        
        vartype=child.type #Defvar/vector/
        tipoPos = analyseExp(child.children[0].children[0],table)        
        if tipoPos== "Float":
            print "Error Semantico! El tamanyo de los vectores debe ser entero. Linea: %d" %(defvar.lineno)
        elif tipoPos=="Entero":
            varsize=child.children[0].children[0].leaf #Defvar/Vector/Posicion.valor            
            if varsize!=None:
                if int(varsize)<0:
                    print "Error Semantico! Se esta creando el vector %s de tamanyo negativo. Linea: %d" %(varname,defvar.lineno)
                newVar=Var(varname,vartype,child.lineno,int(varsize))
                table.appendVar(newVar) #nombre,tipo(vec)/tamanyo
        else:                    
            newVar=Var(varname,vartype,child.lineno)
            table.appendVar(newVar) #nombre,tipo(vec)/

#Agrega una nueva tabla a partir de un nodo Funcion
#No tiene retorno
def addFunAndAnalyse(fun,table):    
    if table.searchTableUp(fun.leaf)==None:
        newTab = Table(fun.leaf,fun.lineno,table)
        table.appendTable(newTab)
        semAnalysis(fun,newTab)
    else:
        print "Error Semantico! Se esta redefiniendo la funcion %s. Linea: %d" %(fun.leaf,fun.lineno)

#Analiza relaciones
#Retorna el tipo de dato de las expresiones relacionadas si se pueden determinar y son iguales, de lo contrario retorna None
def analyseRel(rel,table):    
    if rel.type in ("<","<=",">",">=","==","!="): #reglas de relaciones 1 a 6        
        typeLeft= analyseExp(rel.children[0],table)
        typeRight= analyseExp(rel.children[1],table)
        if typeLeft!=None and typeRight!=None and not compareTypes(typeLeft,typeRight):
            print "Error Semantico! Se estan comparando dos tipos diferentes de datos %s y %s. Linea: %d" %(typeLeft,typeRight,rel.lineno)
    elif rel.type in ("and","or"): #reglas de relaciones 7 y 8
        analyseRel(rel.children[0], table) #analizo ambos lados de la relacion
        analyseRel(rel.children[1], table)
    elif rel.type=="not":
        analyseRel(rel.children[0],table)#analizo la relacion
    return None

#Analiza expresiones
#Retorna el tipo de dato de la expresion, si se puede determinar, de lo contrario retorna None
def analyseExp(exp,table):    
    #print exp.type
    if exp.type in ("Entero", "Float"): #Caso base, regla de exp 11. Retorno el tipo del numero
        return exp.type

    elif exp.type in ("Id","Vector"): #reglas de exp 9,10. Retorno el tipo de la variable        
        varExp=table.searchVarUp(exp.leaf)               
        if varExp==None :
            print "Error Semantico! La variable %s no ha sido definida. Linea: %d" %(exp.leaf,exp.lineno)        
            return None
        if (varExp.type == "Entero" and exp.type =="Vector"):
            print "Error Semantico la variable %s se esta tratando como vector. No lo es. Linea %d" %(varExp.name,exp.lineno)
            return None
        #if exp.type == "Id" and varExp.type in ("Vector int","Vector float"):
        #    print "Error Semantico la variable %s es un vector y no se esta tratando como tal. Linea %d" %(varExp.name,exp.lineno)
        if exp.type == "Vector":
            innerExp=exp.children[0].children[0]            
            innerExpType=analyseExp(innerExp,table)            
            if(innerExpType=="Float"):
                print "Error Semantico! La posicion de los vectores debe ser un entero. Linea: %d" %(innerExp.lineno)
            verifyPos(exp,table,varExp.size,varExp.name)        
        return varExp.type

    elif exp.type in ("Suma","Resta","Multiplicacion","Division"): #reglas de exp 1,2,3,4. Se comparan los operandos
        typeLeft= analyseExp(exp.children[0],table)
        typeRight= analyseExp(exp.children[1],table)        
        if typeLeft!=None and typeRight!=None:
            if not compareTypes(typeLeft,typeRight):
                print "Error Semantico! Se estan operando dos tipos diferentes de datos %s y %s. Linea: %d" %(typeLeft,typeRight,exp.lineno)
            else:
                return typeLeft

    elif exp.type in ("ConverInt","ConverFloat"):#reglas de exp 12 y 13, conversiones
        analyseExp(exp.children[0],table)
        if exp.type=="ConverInt":
            return "Entero"
        if exp.type=="ConverFloat":
            return "Float"

    elif exp.type in ("+","-"): #reglas de exp 5 y 6. Operadores unarios
        return analyseExp(exp.children[0],table)

    elif exp.type == "Llamado a Funcion":#regla de exp 8.
        return analyseFunCall(exp,table)

	return None

#Analiza llamados a funciones
#Retorna el tipo de dato de la funcion, si se puede determinar, de lo contrario retorna None
def analyseFunCall(funCall,table):    
    id=funCall.leaf;
    args=funCall.children[0].children #Lista de expresiones
    funTable=table.searchTableUp(id)
    if(funTable==None):
        print "Error Semantico! se esta llamando a una funcion (%s) no definida. Linea: %d" %(id,funCall.lineno)
        return None
    elif(len(args)!=funTable.numArgs):
        print "Error Semantico! Se esta llamando una funcion (%s) que recibe %d argumentos con %d argumentos. Linea: %d" %(id,funTable.numArgs, len(args),funCall.lineno)
    else:
        for i in range(len(args)):
            argType=analyseExp(args[i],table)
            if argType!=None and argType!=funTable.argTypes[i]:
                print "Error Semantico el argumento numero %d no coincide(%s). Se espera un %s, se recibio un %s. Linea: %d" %(i+1,args[i].leaf,funTable.argTypes[i],argType,funCall.lineno)
    return funTable.type

#Analiza ubicaciones
#Retorna el tipo de dato de la variable si la encuentra, de lo contrario retorna None
def analyseLoc(location,table):
    #print location.type
    locName = location.leaf;
    var=table.searchVarUp(locName)
    if(var==None): #Si no la encuentra
        print "Error Semantico! Se esta intentando usar una variable no definida: %s. Linea: %d" %(locName,location.lineno)
        return None           
    elif (location.type=="Ubicacion" and var.type in ("Vector int","Vector float")):
        print "Error Semantico! Las asignaciones en vectores se deben hacer a alguna posicion. Linea: %d" %(location.lineno)
    elif location.type in ("Ubicacionvector","Vector"): #Si el tipo de ubicacion es de vector
        if var.type not in ("Vector int","Vector float"):
            print "Error Semantico! La variable %s no es un vector. Linea: %d" %(locName,location.lineno)
        expLoc =location #Ubicacionvector/expresion
        if location.type=="Vector":
            expLoc=location.children[0]            
        expLocType=analyseExp(expLoc.children[0],table)
        if expLocType=="Float":
            print "Error Semantico! La posicion de los vectores debe ser un entero. Linea: %d" %(location.lineno)
        verifyPos(expLoc,table,var.size,var.name)
    return var.type

#Verifica la posicion de un vector
#No tiene retorno
def verifyPos(expLoc,table,varSize,locName):    
    pos=findPos(expLoc.children[0],table)        
    if(pos!=None and (pos<0 or pos>varSize)):
        #Arreglar para negativos!
        print "Precaucion! Se intenta acceder a un indice fuera de rango en el vector %s. Linea: %d" %(locName,expLoc.lineno)

#Encuentra la posicion de un vector, si es posible
#Retorna la posicion si se puede determinar, de lo contrario retorna None
def findPos(expLoc,table):    
    if expLoc.type=="Entero":
        return int(expLoc.leaf)
    elif expLoc.type =="+":
        return findPos (expLoc.children[0],table)
    elif expLoc.type =="-" and expLoc.children[0].type=="Entero":        
        return  -int(expLoc.children[0].leaf)
    return None

#Verifica que conicidan en el tipo de dato las asignaciones (ambas deben ser enteros o ambas flotantes)
#Retorna verdadero si coincide, falso de lo contrario
def compareTypes(a,b):
    return ((a in ("Vector int", "Entero") and b in("Vector int", "Entero")) or (a in ("Vector float", "Float") and b in("Vector float", "Float")))

#Imprime las tablas a partir del nodo dado
def printTable(node):
    if node.parent==None:
        print "Tabla: %s\tTipo: %s\tPadre: Ninguno\nHijos:" %(node.name,node.type)
    else:
        print "Tabla: %s\tTipo: %s\tPadre: %s\nHijos:" %(node.name,node.type,node.parent.name)
    for var in node.vars:
        if var.size!=0:
            print "Variable: %s\tTipo: %s\tTamanyo: %d\tLinea: %d" %(var.name,var.type,var.size,var.lineno)
        else:
            print "Variable: %s\tTipo: %s\tLinea: %d" %(var.name,var.type,var.lineno)
    for tabla in node.subTables:
        print "\n"
        printTable(tabla)

#Llamado.

if __name__ == "__main__":
    f = open(sys.argv[1])
    s = f.read()
    result = mpasparse.parser.parse(s)
    if result:
        raiz=Table("Programa",0)
        semAnalysis(result,raiz)
        printTable(raiz)
