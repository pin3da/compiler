class DotVisitor(NodeVisitor):
    graph = None
    def __init__(self):
        self.graph = pydot.Dot('AST', graph_type='digraph')
        self.id=0
    def ID(self):
        self.id+=1
        return "n%d" %self.id

 		def visit_non_leaf(self,node):
        name=pydot.Node(self.ID(), shape='circle')
        name.label(node.__class__.__name__)
        for field in getattr(node,"_fields"):
						value = getattr(node,field,None)
           
            if isinstance(value,list):
                newvalues = []
                for item in value:
                    if isinstance(item,AST):
                        self.graph.add_edge(pydot.Edge, node.__class__.__name__, item.__class__.__name__)#not sure
                        newnode = self.visit(item)
                        if newnode is not None:
                            newvalues.append(newnode)
                    else:
                        newvalues.append(n)
                value[:] = newvalues
                                    
            elif isinstance(value,AST):
                self.graph.add_edge(pydot.Edge, node.__class__.__name__ ,value.__class__.__name__)
                newnode = self.visit(value)
                if newnode is None:
                    delattr(node,field)
                else:
                    setattr(node,field,newnode)
        return name

    def visit_leaf(self, node):
        name=pydot.Node(self.ID(), shape='box')
	      name.label(node.__class__.__name__ % node.value)
        return name

    def visit (self, node):
        if(self.leaf)
            visit_leaf(node)
        else
            visit_non_leaf(node)

    
       
