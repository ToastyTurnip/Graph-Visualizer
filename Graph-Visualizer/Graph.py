
STATECAPTURELIMIT = 200
class GraphNode:
    def __init__(self, name):
        self.name = name
        if type(name) != str:
            raise Exception
        self.outEdges = list() #must be a list of edge objects!
        self.params = dict() #param name must be string, value must be str, int, or float

    def AddEdge(self, dstNode): #dstNode here must be a GraphNodeObject!
        new_edge = GraphEdge(self.name + dstNode.name, self, dstNode)
        self.outEdges.append(new_edge)
        return new_edge

    def RemoveEdgeByName(self, name):
        for edge in self.outEdges:
            if edge.name == name:
                self.outEdges.remove(edge)
                return

    def RemoveEdgeByDST(self, dstNodename):
        for edge in self.outEdges:
            if edge.dstNode.name == dstNodename:
                self.outEdges.remove(edge)
                return

    def GetNodeXML(self):
        outEdgesXML = ""
        for edge in self.outEdges:
            outEdgesXML += "\n\t\t<outEdge name = '%s'>" % (edge.name)
        paramsXML = ""
        for key in self.params.keys():
            paramsXML += "\n\t\t<param name = '%s' value = '%s'>" % (key, self.params[key])
        infoString = "\n<Node name = '%s'>\n\t<outEdges>%s\n\t</outEdges>\n\t<Params>%s\n\t</Params>\n</Node>" % (self.name, outEdgesXML, paramsXML)
        return infoString

    def GetChildren(self):
        children = list()
        for edge in self.outEdges:
            if edge.dstNode != None:
                children.append(edge.dstNode)
        return children
    
class GraphEdge:
    def __init__(self, name, srcNode, dstNode):
        self.name = name
        self.srcNode = srcNode #must be a NodeObject!!
        self.dstNode = dstNode #must be a NodeObject!!
        self.params = dict() #param name must be string, value must be str, int, or float

    def GetEdgeXML(self):
        paramsXML = ""
        for key in self.params.keys():
            paramsXML += "\n\t\t<param name = '%s' value = '%s'>" % (key, self.params[key])
        infoString = "\n<Edge name = %s>\n\t<srcNode value = '%s'>\n\t<dstNode value = '%s'>\n\t<Params>%s\n\t</Params>\n</Edge>" % (self.name, self.srcNode.name, self.dstNode.name, paramsXML)
        return infoString
        
class Graph:
    def __init__(self, name):
        self.name = name
        self.nodes = list() #must be a list of strings!
        self.nStateCaptures = 0

    def GetNode(self, nodeName):
        if type(nodeName) != str:
            raise Exception
        for node in self.nodes:
            if node.name == nodeName:
                return node
        else:
            new_node = GraphNode(nodeName)
            self.nodes.append(new_node)
            return new_node
    
    def ConnectNodes(self, nodeName1, nodeName2, name = ""):
        '''Creates a one way edge from node1 to node2, arguments must be string pertaining to the name of the nodes'''
        return self.GetNode(nodeName1).AddEdge(self.GetNode(nodeName2))

    def GetEdge(self, edgeName):
        for node in self.nodes:
            for edge in node.outEdges:
                if edge.name == edgeName:
                    return edge

    def DeleteNode(self, name):
        for node in self.nodes:
            if node.name == name:
                self.nodes.remove(node)
                return
    
    def printALL(self):
        for node in self.nodes:
            print(node.GetNodeXML())
        print("\n")
        for node in self.nodes:
            for edge in node.outEdges:
                print(edge.GetEdgeXML())

    def CaptureState(self):
        '''Returns an XML string of the state of the graph.'''
        XMLnodes = ""
        XMLedges = ""
        for node in self.nodes:
            XMLnodes += node.GetNodeXML()
        for node in self.nodes:
            for edge in node.outEdges:
                XMLedges += edge.GetEdgeXML()
        nodesXML = "<Nodes>%s</Nodes>" % (XMLnodes)
        edgesXML = "<Edges>%s</Edges>" % (XMLedges)
        file = open(self.name+"-States.txt", 'a')
        if self.nStateCaptures < STATECAPTURELIMIT:
            stateXML = "<State number = %s>\n%s\n</State>" % (self.nStateCaptures, nodesXML + "\n" + edgesXML)
            file.write(stateXML)
            file.close()
            self.nStateCaptures += 1
        return nodesXML + "\n" + edgesXML

## Usage: instructions are of the form <Node1><rel><Node2><:><additionalparams>*
## <Node1> and <Node2> will be used as the name of the GraphNode, <rel> can be
## either '=' or '>', if '=' is used, two edges will be created creating two ways
## between two nodes, if '>' is created, then a one-way edge will be created from
## <Node1> to <Node2>.
##
## Optional Parameters: when CreateGraph is called, the user will be prompted to
## enter names for additional parameters separated by spaces, this template will be
## used later for parsing each instruction and storing the parameters.

def CreateGraph(name ,instructions):
    '''This will parse a string of instructions separated by the separator '\n'
    and return a Graph based on the read instructions'''
    NODETEMPLATE = list()
    EDGETEMPLATE = list()
    listOfInstructions = instructions.split('\n')
    graph = Graph(name)
    for inst in listOfInstructions:
        if inst.startswith("//") or inst == '\n' or inst == '': # this is for comments
            continue
        if inst.startswith("NODETEMPLATE:"):
            sub_inst = inst.split()
            if len(sub_inst) > 1:
                NODETEMPLATE = sub_inst[1:]
            continue
        if inst.startswith("EDGETEMPLATE:"):
            sub_inst = inst.split()
            if len(sub_inst) > 1:
                EDGETEMPLATE = sub_inst[1:]
            continue
        if inst.startswith("NODE:"):
            sub_inst = inst.split()
            _node = graph.GetNode(sub_inst[1])
            for paramNo in range(len(NODETEMPLATE)):
                try:
                    _node.params[NODETEMPLATE[paramNo]] = sub_inst[paramNo + 2]
                except Exception:
                    _node.params[NODETEMPLATE[paramNo]] = None
            continue

        if inst.startswith("EDGE:"):
            sub_inst = inst.split()
            _edge = graph.GetEdge(sub_inst[1])
            if _edge == None:
                raise Exception
            for paramNo in range(len(EDGETEMPLATE)):
                try:
                    _edge.params[EDGETEMPLATE[paramNo]] = sub_inst[paramNo + 2]
                except Exception:
                    _edge.params[EDGETEMPLATE[paramNo]] = None
            continue
        
        sub_inst = inst.split(':')
        if '=' in sub_inst[0]:
            _nodeNames = sub_inst[0].split('=')
            _n1 = graph.GetNode(_nodeNames[0])
            _n2 = graph.GetNode(_nodeNames[1])
            _edge1 = graph.ConnectNodes(_nodeNames[0],_nodeNames[1])
            _edge2 = graph.ConnectNodes(_nodeNames[1],_nodeNames[0])
            params = sub_inst[1].split()
            if _edge1 == None or _edge2 == None:
                raise Exception
            for paramNo in range(len(EDGETEMPLATE)):
                try:
                    _edge1.params[EDGETEMPLATE[paramNo]] = params[paramNo]
                    _edge2.params[EDGETEMPLATE[paramNo]] = params[paramNo]
                except Exception:
                    _edge1.params[EDGETEMPLATE[paramNo]] = None
                    _edge2.params[EDGETEMPLATE[paramNo]] = None
        else:
            _nodeNames = sub_inst[0].split('>')
            _n1 = graph.GetNode(_nodeNames[0])
            _n2 = graph.GetNode(_nodeNames[1])
            _edge = graph.ConnectNodes(_nodeNames[0],_nodeNames[1])
            params = sub_inst[1].split()
            if _edge == None:
                raise Exception
            for paramNo in range(len(EDGETEMPLATE)):
                try:
                    _edge.params[EDGETEMPLATE[paramNo]] = params[paramNo]
                except Exception:
                    _edge.params[EDGETEMPLATE[paramNo]] = None
    return graph






































        
        
    
        
