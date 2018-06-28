#A minor change

import xml.etree.ElementTree as etree
import AlteryxTools as AT
#import AlteryxField as AF
import pickle

class AlteryxWorkflow:
    
    def __init__(self, altToolDict = {}, filepath = ""):
        self.altToolDict = altToolDict
        self.filepath = filepath
        if filepath != "":
            self.loadWorkflow(filepath)
            
    def saveWFObj(self, filepath):
        output = open(filepath, "wb")
        pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        
    #Generates a dictionary of all of the Alteryx Tool objects from the XML
    #into the Alteryx Workflow object. 
    def nodeScan(self, nodes):
        #nodelst = []
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
                #nodelst = nodelst + nodeScan(childNodes)
                self.nodeScan(childNodes)

            #This will need to broken out based on different types of tools
            #for the formula search we will need formula tools and any tool
            #that can rename a field or perform a calculation (e.g. Select, Summarize, etc.)
            toolID = node.attrib['ToolID']
            x = float(guiSet.find('Position').attrib['x'])/40
            #Alteryx is up down positive, whereas Visio is down up
            y = -1*float(guiSet.find('Position').attrib['y'])/40
            altTool = AT.AlteryxTool(toolID, tooltype, x, y, node)
            self.altToolDict[toolID] = altTool
    
    #Recursive function to scan fields within tools to discover the dependencies
    def determineFieldDep(self, toolID):
        toolObj = self.altToolDict[toolID]
        
    
    def loadWorkflow(self, filepath):
        tree = etree.parse(filepath)
        root = tree.getroot()
        self.__workflow_xml_tree__ = tree
        self.__workflow_xml_root__ = root        
        
        nodes = root.findall('./Nodes/Node')
        cons = root.findall('./Connections/Connection')
        
        self.nodeScan(nodes)
        
        for con in cons:
            originID = con.find('Origin').attrib['ToolID']
            destID = con.find('Destination').attrib['ToolID']

            self.altToolDict[originID].consOut[destID] = self.altToolDict[destID]
            self.altToolDict[destID].consIn[originID] = self.altToolDict[originID]

        #Now determine formula dependencies
        #Get all terminal tools
        terminalTools = []
        for toolID in self.altToolDict.keys():
            if self.altToolDict[toolID].isTerminal() and not self.altToolDict[toolID].isInitial():
                terminalTools.append(toolID)
                
        for termTool in terminalTools:
            self.determineFieldDep(termTool)
                 


###############################################################################
#END OF ALTERYX WORKFLOW CLASS DEFINITION
###############################################################################

def loadWFObj(self, filepath):
    input = open(filepath, "rb")
    altWFLoaded = pickle.load(input)
    return altWFLoaded
       
    
