#XML file does not alway provide all of information on fields, such as dataType and size
#May need to develop a way to dynamically fill in this information when searching the workflow
#This will generally not be possible

import xml.sax.saxutils as saxutils
import re

class AlteryxField:
    def __init__(self, name, size = "", dataType = "", selected = True, rename = "", formulaExp = ""):
        self.name = name
        self.dataType = dataType
        self.size = size
        
        if rename == "":
            self.rename = name
        else:
            self.rename = rename
                
        self.selected = selected
        #Each dictionary key will contain a list of ALteryxTool objects that 
        #this field is dependent upon. We need a list of Tools, because with a
        #Union Tool a field may have multiple definitions and this field is
        #dependent upon all of them
        self.fieldDep = {}
        self.formulaExp = self.normFormulaExp(formulaExp)
        
        if formulaExp != "":
            self.parseExpFieldsDep()
            
    def parseExpFieldsDep(self):
        #Need to remove comments
        #both "\\ ... \n" and "\* ... *\" comments
        #pick out fields from use of brackets
        #may also want to look into using in-DB formula tools
        temp = re.sub('//.+?\\n', '', self.formulaExp) #remove comment lines
        temp = re.sub('/\*.+?\*/','', temp) #remove comment blocks
        fieldList = re.sub('\[.*?\]', '',temp)
        for f in fieldList:
            f = f.replace('[', '')
            f = f.replace(']', '')
            self.fieldDep[f] = []
        pass
    
    def normFormulaExp(self, formulaExp):
        tempExp = saxutils.unescape(formulaExp)
        tempExp = tempExp.replace('&quote;', '"')
        tempExp = tempExp.replace('&#xA;', '\n')
        
        
        return tempExp
