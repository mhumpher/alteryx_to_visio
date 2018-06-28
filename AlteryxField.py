import xml.sax.saxutils as saxutils
import re

class AlteryxField:
    def __init__(self, field_xml, parent):
        self.__field_xml__ = field_xml
        self.__parent__ = parent
        self.name = self.__field_xml__.attrib['field']
        self.outputName = self.__getOutputName__()
        self.attributes = self.__field_xml__.attrib
        #fieldDep will be a dictionary of the field names that this field depends upon.
        #The item of each key will be a dictionary of the toolID (key) with a list of
        #AlteryxField objects (item) that this field depends upon in that Tool. 
        #{'field1':{5:[obj1, obj2]}, 'field2': {7:[obj3, obj4], 8:[obj5]}}
        self.fieldDep = {}        
        
        if 'expression' in self.attributes:
            self.formulaExp = self.__normFormulaExp__(self.attributes['expression'])
            self.__parseExpFieldsDep__()
            
    def __parseExpFieldsDep__(self):
        #Need to remove comments
        #both "\\ ... \n" and "\* ... *\" comments
        #pick out fields from use of brackets
        #may also want to look into using in-DB formula tools
        temp = re.sub('//.+?\\n', '', self.formulaExp) #remove comment lines
        temp = re.sub('/\*.+?\*/','', temp) #remove comment blocks
        fieldList = re.sub('\[.*?\]', '',temp)
        distinctFieldList = list(set(fieldList))
        for f in distinctFieldList:
            f = f.replace('[', '')
            f = f.replace(']', '')
            self.fieldDep[f] = {} 
        #pass
    
    def __normFormulaExp__(self, formulaExp):
        tempExp = saxutils.unescape(formulaExp)
        tempExp = tempExp.replace('&quote;', '"')
        tempExp = tempExp.replace('&#xA;', '\n')
        return tempExp
        
    def toolIdDepend(self, fieldname):
        if bool(self.fieldDep) and fieldname in self.fieldDep:
            return list(self.fieldDep[fieldname].keys())
        else:
            return []
    
    def __getOutputName__(self):
        if 'rename' in self.__field_xml__.attrib:
            return self.__field_xml__.attrib['rename']
        elif 'field' in self.__field_xml__.attrib:
            return self.__field_xml__.attrib['field']
        else:
            return ""
