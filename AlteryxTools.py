import AlteryxField as AF

class AlteryxTool:
   
    def __init__(self, toolId, toolType, x, y, tool_xml):
        self.toolId = toolId
        self.toolType = toolType
        self.x = x
        self.y = y
        self.consIn = {}
        self.consOut = {}
        self.fields = {}
        self.__tool_xml__ = tool_xml
        
        self.__populateFields__()

    def __getFieldElements__(self):
        return self.__getNodesWithAttrib__(attrib = 'field')
        
    def __getNodesWithAttrib__(self, attrib):
        return self.__tool_xml__.findall('.//*[@' + attrib + ']')
        
    def getFieldNames(self):
        return self.fields.keys()
        
    def addConIn(self, toolId, altTool):
        self.consIn[toolId] = altTool
        
    def addConOut(self, toolId, altTool):
        self.consOut[toolId] = altTool 
        
    #If no connections out, tool is considered terminal
    def isTerminal(self):
        #Empty Python dictionaries evaluate as false
        return not bool(self.consOut)
        
    #If no connections in, tool is considered initial
    def isInitial(self):
        return not bool(self.consIn)
    
    def __populateFields__(self):
        fieldNodes = self.__getFieldElements__()
        for fN in fieldNodes:
            altField = AF.AlteryxField(fN, self)
            self.fields[fN.attrib['field']] = altField
            
    def checkOutputFieldNames(self, fieldname):
        #if there are no renames and the fieldname is in the dictionary, then true
        for key in self.fields:
            if self.fields[key].outputName == fieldname:
                return False
        return False
        
    def getFieldFromOutputName(self,fieldname):
        for key in self.fields:
            if self.fields[key].outputName == fieldname:
                return self.fields[key]
        return ""
                        

            
        
