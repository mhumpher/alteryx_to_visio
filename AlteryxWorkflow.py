#Version 0.2

import xml.etree.ElementTree as etree
import matplotlib as mp
import pickle
import re
import xml.sax.saxutils as saxutils
import networkx as nx

class AlteryxWorkflow:
    
    def __init__(self, filepath = ""):
        #self.workflowGraph = nx.DiGraph() 
        #self.filepath = filepath
        if filepath != "":
            self.load_workflow(filepath)
            
    def save_workflow(self, filepath):
        output = open(filepath, "wb")
        pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load_workflow(self, filepath):
        tree = etree.parse(filepath)
        root = tree.getroot()     
        prop_xml = root.find('Properties')
        self.workflowGraph = nx.DiGraph(properties_xml = prop_xml, tree_xml = tree)
        
        nodes = root.findall('./Nodes/Node')
        cons = root.findall('./Connections/Connection')
        
        self._nodeScan(nodes)
        
        for con in cons:
            originID = con.find('Origin').attrib['ToolID']
            originName = con.find('Origin').get('name')
            destID = con.find('Destination').attrib['ToolID']
            destName = con.find('Destination').get('name')
            conName = con.get('name')
            wirelessFlag = con.get('Wireless', 'False')

            
            self.workflowGraph.add_edge(originID, destID,
                                        origin_name = originName,
                                        destination_name = destName,
                                        connection_name = conName,
                                        wireless = wirelessFlag)
        
    #Generates a dictionary of all of the Alteryx Tool objects from the XML
    #into the Alteryx Workflow object. 
    def _nodeScan(self, nodes):
        graphNodes = []
        for node in nodes:
        #check if node is a macro
            guiSet = node.find('GuiSettings')
            if bool(guiSet.attrib):
                tooltype = guiSet.attrib['Plugin'].split('.')[-1]
            else: 
                tooltype = node.find("EngineSettings").attrib['Macro']
        
            #check if node is a tool contianer
            #Ignore Tool Containers for now
            if tooltype == 'ToolContainer':
                childNodes = node.find('ChildNodes').findall('Node')
                graphChildNodes = self._nodeScan(childNodes)
                self.workflowGraph.add_node(node.attrib['ToolID'], 
                    toolType = tooltype, 
                    __node_xml__ = node, 
                    childNodes = graphChildNodes)
            else:
            #This will need to broken out based on different types of tools
            #for the formula search we will need formula tools and any tool
            #that can rename a field or perform a calculation (e.g. Select, Summarize, etc.)
                self.workflowGraph.add_node(node.attrib['ToolID'], 
                                            toolType = tooltype, 
                                            __node_xml__ = node)
            graphNodes.append(node.attrib['ToolID'])
        return graphNodes
            
    
    #Recursive function to scan fields within tools to discover the dependencies
    def determineFieldDep(self, toolID):
        #toolObj = self.altToolDict[toolID]
        pass
        
    #Returns ToolID list of all tool of particular type
    def getNodesFromType(self, toolType):
        return [n for n,d in self.workflowGraph.nodes(data=True) if d['toolType']== toolType]

    #Returns a list of the toolID's of all nodes in the workflow that include
    #expressions. This includes all Filters, Multi-Row/Field, Formula, etc. tools
    def getNodesWithExp(self):
        g = self.workflowGraph
        n = g.nodes(data = True)
        exp = [x for x,d in n 
            if (d['__node_xml__'].find('.//Expression') != None 
                or d['__node_xml__'].find('.//*[@expression]') != None) 
                and d['toolType'] != 'ToolContainer']
        return exp
    
    #Returns input text by unescaping XML codes, but also special codes used
    #used by Alteryx. This is especially used for formula expressions.    
    def _normFormulaExp(self, formulaExp):
        tempExp = saxutils.unescape(formulaExp)
        tempExp = tempExp.replace('&quote;', '"')
        tempExp = tempExp.replace('&#xA;', '\n')
        return tempExp
        
    '''
    def getToolDict(self):
        toolDict = {}
        for t in self.workflowGraph.nodes():
            toolDict[t] = self.workflowGraph.node[t]['toolObj']
        return toolDict
    ''' 
    
    #Returns tuples of toolID number, field name and formula expression
    #for each of the expression in formula tools that match the pattern.       
    def searchToolFormula(self, searchPattern, ignoreCase=False):
        #altToolDict = self.getToolDict()
        toolList = []
        g = self.workflowGraph
        graph_nodes = g.nodes(data = True)
        form_nodes = [n for n,d in graph_nodes if d['toolType'] == 'Formula']
        if ignoreCase:
            caseFlag = re.IGNORECASE
        else:
            caseFlag = 0
        for n in form_nodes:
            currTool = g.node[n] #gives attribute dictionary for node id n
            if currTool['toolType'] == 'Formula':
                form_fields = currTool['__node_xml__'].findall('.//*[@expression]')
                print(form_fields)
                for f in form_fields:
                    name = f.get('name')
                    exp = f.get('expression')
                    p = re.compile(searchPattern, flags = caseFlag)
                    if p.search(exp):
                        toolList.append((n, name, exp)) 
        return toolList
    
    #Returns tuples of toolID number, field name and formula expression
    #for each of the field name in formula tools that match the pattern.
    def searchToolFields(self, searchPattern, ignoreCase=False):
        toolList = []
        g = self.workflowGraph
        graph_nodes = g.nodes(data = True)
        form_nodes = [n for n,d in graph_nodes if d['toolType'] == 'Formula']
        if ignoreCase:
            caseFlag = re.IGNORECASE
        else:
            caseFlag = 0
        for n in form_nodes:
            currTool = g.node[n] #gives attribute dictionary for node id n
            if currTool['toolType'] == 'Formula':
                form_fields = currTool['__node_xml__'].findall('.//*[@expression]')
                print(form_fields)
                for f in form_fields:
                    name = f.get('name')
                    exp = f.get('expression')
                    p = re.compile(searchPattern, flags = caseFlag)
                    if p.search(name):
                        toolList.append((n, name, exp)) 
        return toolList
       
             
    def drawWFGraph(self):
        g = self.workflowGraph
        pos = {}
        for n in g.nodes():
            node_xml= g.node[n]['__node_xml__']
            guiSet = node_xml.find('GuiSettings')
            x = float(guiSet.find('Position').attrib['x'])
            y = -float(guiSet.find('Position').attrib['y'])
            pos[n] = (x,y)
        nx.draw(g, pos)
        mp.pyplot.show()


###############################################################################
#END OF ALTERYX WORKFLOW CLASS DEFINITION
###############################################################################

def loadWFObj(self, filepath):
    input = open(filepath, "rb")
    altWFLoaded = pickle.load(input)
    return altWFLoaded
       
    
