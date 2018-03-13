import xml.etree.ElementTree as etree
import AlteryxTools as AT
import AlteryxField as AF
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
            else:
                #This will need to broken out based on different types of tools
                #for the formula search we will need formula tools and any tool
                #that can rename a field or perform a calculation (e.g. Select, Summarize, etc.)
                toolID = node.attrib['ToolID']
                x = float(guiSet.find('Position').attrib['x'])/40
                #Alteryx is up down positive, whereas Visio is down up
                y = -1*float(guiSet.find('Position').attrib['y'])/40
                altTool = AT.AlteryxTool(toolID, tooltype, x, y)

                if tooltype == 'Formula':
                    formulaFields = node.find('./Properties/Configuration/FormulaFields')
                    for formulaField in formulaFields:
                        formulaExp = formulaField.attrib['expression']
                        fieldName = formulaField.attrib['field']
                        fieldSize = formulaField.attrib['size']
                        fieldType = formulaField.attrib['type']
                        altField = AF.AlteryxField(name = fieldName, size = fieldSize, dataType = fieldType, formulaExp = formulaExp)
                        altTool.fields[fieldName] = altField
                elif tooltype == 'AlteryxSelect':
                    selectFields = node.find('./Properties/Configuration/SelectFields')
                    for selectField in selectFields:
                        fieldName = selectField.attrib['field']
                        fieldSelect = (selectField.attrib['selected'] == 'True')
                        fieldSize = selectField.attrib.get('size', '')
                        fieldType = selectField.attrib.get('type', '')
                        fieldRename = selectField.attrib.get('rename', fieldName)
                                
                        altField = AF.AlteryxField(name = fieldName, size = fieldSize, \
                                dataType = fieldType, selected = fieldSelect, rename = fieldRename)
                        altTool.fields[fieldName] = altField
                
                self.altToolDict[toolID] = altTool
    
    def loadWorkflow(self, filepath):
        tree = etree.parse(filepath)
        root = tree.getroot()
        nodes = root.findall('./Nodes/Node')
        cons = root.findall('./Connections/Connection')
        
        self.nodeScan(nodes)
        
        for con in cons:
            originID = con.find('Origin').attrib['ToolID']
            destID = con.find('Destination').attrib['ToolID']

            self.altToolDict[originID].consOut[destID] = self.altToolDict[destID]
            self.altToolDict[destID].consIn[originID] = self.altToolDict[originID]

        #Now determine formula dependencies

###############################################################################
#END OF ALTERYX WORKFLOW CLASS DEFINITION
###############################################################################

def loadWFObj(self, filepath):
    input = open(filepath, "rb")
    altWFLoaded = pickle.load(input)
    return altWFLoaded   
