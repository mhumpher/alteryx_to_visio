import AlteryxFormula

class AlteryxTool:   
    
    def __init__(self, toolId, toolType, x, y):
        self.toolId = toolId
        self.toolType = toolType
        self.x = x
        self.y = y
        self.consIn = {}
        self.consOut = {}
        
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
        
class FormulaTool(AlteryxTool):
    
    def __init__(self, toolId, toolType, x, y):
        self.toolId = toolId
        self.toolType = toolType
        self.x = x
        self.y = y
        self.consIn = {}
        self.consOut = {}
        self.formulas = {}
            
    def addFormula(self, expression, field, size, dataType):
        form = AlteryxFormula(expression, field, size, dataType)
        self.formulas[field] = form
        
class SelectTool(AlteryxTool):
    def __init__(self, toolId, toolType, x, y):
        self.toolId = toolId
        self.toolType = toolType
        self.x = x
        self.y = y
        self.consIn = {}
        self.consOut = {}
        #should we care about the order of the fields?
        self.fields = {}

###############################################################################
#
#Special Tools
#- Documentation
#
###############################################################################        
class DocumentationTool:
    def __init__(self, toolId, toolType, x, y, width, height):
        self.toolId = toolId
        self.toolType = toolType
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
class ToolContainer(DocumentationTool):
    def __init__(self, toolId, toolType, x, y, width, height, caption):
        self.toolId = toolId
        self.toolType = toolType
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.caption = caption
        self.childTools = {}
        
class TextBoxTool(DocumentationTool):
    def __init__(self, toolId, toolType, x, y, width, height, text):
        self.toolId = toolId
        self.toolType = toolType
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        
