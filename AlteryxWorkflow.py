#version 0.3

import xml.etree.ElementTree as etree
import matplotlib as mp
import pickle
import re
import xml.sax.saxutils as saxutils
import networkx as nx

class AlteryxWorkflow:
    
    def __init__(self, filepath = ""):
        if filepath != "":
            self.load_workflow(filepath)
            
    def save_workflow(self, filepath):
        output = open(filepath, "wb")
        pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def load_workflow(self, filepath):
        tree = etree.parse(filepath)
        root = tree.getroot()     
        prop_xml = root.find('Properties')
        self.workflowGraph = nx.MultiDiGraph(properties_xml = prop_xml, tree_xml = tree)
        
        nodes = root.findall('./Nodes/Node')
        cons = root.findall('./Connections/Connection')
        
        self._nodeScan(nodes)
        
        for con in cons:
            originID = con.find('Origin').attrib['ToolID']
            destID = con.find('Destination').attrib['ToolID']
            conName = con.get('name')

            
            self.workflowGraph.add_edge(originID, destID,
                                        connection_name = conName,
                                        connection_xml = con)
        
    #Adds all of the tools as nodes in the NetworkX graph with the XML
    #Element tree included as an attribute
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
            if tooltype == 'ToolContainer':
                childNodes = node.find('ChildNodes').findall('Node')
                graphChildNodes = self._nodeScan(childNodes)
                tool = AlteryxTool(node.attrib['ToolID'],tooltype,node)
                self._parseToolXML(node, tool)
                self.workflowGraph.add_node(node.attrib['ToolID'],
                                            tool = tool,
                                            childNodes = graphChildNodes)
            else:
                tool = AlteryxTool(node.attrib['ToolID'],tooltype,node)
                self._parseToolXML(node, tool)
                self.workflowGraph.add_node(node.attrib['ToolID'], 
                                            tool = tool)
            graphNodes.append(node.attrib['ToolID'])
        return graphNodes
    
    #Generate object hierarchy at run time to expose the entire ALteryx
    #workflow structure to easy parsing
    def _parseToolXML(self, xml, obj):
        children = xml.getchildren()
        tags = []
        for c in children:
            tags.append(c.tag)
        
        #Need to improve this check 
        #Check if looking at list of fields
        if ("Fields" in xml.tag):
            child_list = []
            var_name = ""
            for c in children:
                var_name = c.tag
                attributes = c.attrib
                elem = attributes
                child_list.append(elem)
            setattr(obj, var_name + "_List", child_list)
            return
        else:                
            for c in children:
                var_name = c.tag
                attributes = c.attrib
                if not var_name == "ChildNodes":
                #print(var_name)
                #print(attributes)
                    setattr(obj, var_name, type(var_name, (), {}))
                    setattr(getattr(obj,var_name), "attributes", attributes)
                    if c.getchildren():
                        self._parseToolXML(c, getattr(obj, var_name))
            return
        #If not unique, assume all are the same Create indexed list of values
        #and add to the object structure


        
    
    #Recursive function to scan fields within tools to discover the dependencies
    def determineFieldDep(self, toolID):
        #toolObj = self.altToolDict[toolID]
        pass
        
    #Returns ToolID list of all tool of particular type
    def getNodesFromType(self, toolType):
        return [n for n,d in self.workflowGraph.nodes(data=True) 
            if d['tool']._toolType == toolType]

    #Returns a list of the toolID's of all nodes in the workflow that include
    #expressions. This includes all Filters, Multi-Row/Field, Formula, etc. tools
    def getNodesWithExp(self):
        g = self.workflowGraph
        n = g.nodes(data = True)
        exp = [x for x,d in n 
            if (d['tool']._toolXML.find('.//Expression') != None 
                or d['tool']._toolXML.find('.//*[@expression]') != None) 
                and d['tool']._toolType != 'ToolContainer']
        return exp
    
    #Returns input text by unescaping XML codes, but also special codes used
    #used by Alteryx. This is especially used for formula expressions.    
    def _normFormulaExp(self, formulaExp):
        tempExp = saxutils.unescape(formulaExp)
        tempExp = tempExp.replace('&quote;', '"')
        tempExp = tempExp.replace('&#xA;', '\n')
        return tempExp
        
    
    #Returns tuples of toolID number, field name and formula expression
    #for each of the expression in formula tools that match the pattern.       
    def searchToolFormula(self, searchPattern, ignoreCase=False):
        #altToolDict = self.getToolDict()
        toolList = []
        g = self.workflowGraph
        #graph_nodes = g.nodes(data = True)
        #form_nodes = [n for n,d in graph_nodes if d['toolType'] == 'Formula']
        form_nodes = self.getNodesFromType('Formula')        
        if ignoreCase:
            caseFlag = re.IGNORECASE
        else:
            caseFlag = 0
        
        for n in form_nodes:
            currTool = g.node[n]['tool'] #gives attribute dictionary for node id n
            if currTool._toolType == 'Formula':
                #form_fields = currTool['node_xml'].findall('.//*[@expression]')
                form_fields = currTool.Properties.Configuration.FormulaFields.FormulaField_List
                for f in form_fields:
                    name = f['field']
                    exp = f['expression']
                    p = re.compile(searchPattern, flags = caseFlag)
                    if p.search(exp):
                        fieldIndex = form_fields.index(f)
                        toolList.append((n, name, fieldIndex, exp)) 
        return toolList
    
    #Returns tuples of toolID number, field name and formula expression
    #for each of the field name in formula tools that match the pattern.
    def searchToolFields(self, searchPattern, ignoreCase=False):
        #altToolDict = self.getToolDict()
        toolList = []
        g = self.workflowGraph
        #graph_nodes = g.nodes(data = True)
        #form_nodes = [n for n,d in graph_nodes if d['toolType'] == 'Formula']
        form_nodes = self.getNodesFromType('Formula')        
        if ignoreCase:
            caseFlag = re.IGNORECASE
        else:
            caseFlag = 0
        
        for n in form_nodes:
            currTool = g.node[n]['tool'] #gives attribute dictionary for node id n
            if currTool._toolType == 'Formula':
                #form_fields = currTool['node_xml'].findall('.//*[@expression]')
                print(n)
                form_fields = currTool.Properties.Configuration.FormulaFields.FormulaField_List
                for f in form_fields:
                    name = f['field']
                    exp = f['expression']
                    p = re.compile(searchPattern, flags = caseFlag)
                    if p.search(name):
                        fieldIndex = form_fields.index(f)
                        toolList.append((n, name, fieldIndex, exp)) 
        return toolList
       
             
    def drawWFGraph(self):
        g = self.workflowGraph
        pos = {}
        for n in g.nodes():
            #node_xml= g.node[n]['node_xml']
            #guiSet = node_xml.find('GuiSettings')
            #x = float(guiSet.find('Position').attrib['x'])
            #y = -float(guiSet.find('Position').attrib['y'])
            tool= g.node[n]['tool']
            guiSet = tool.GuiSettings
            x = float(guiSet.Position.attributes['x'])
            y = -float(guiSet.Position.attributes['y'])
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
       
class AlteryxTool:
    
    def __init__(self, toolID, toolType, toolXML):
        self._toolID = toolID
        self._toolType = toolType
        self._toolXML = toolXML
    
