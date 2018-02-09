#XML file does not alway provide all of information on fields, such as dataType and size
#May need to develop a way to dynamically fill in this information when searching the workflow
#This will generally not be possible
class AlteryxField:
    def __init__(self, name, size, dataType):
        self.name = name
        self.dataType = dataType
        self.size = size
        
class SelectField(AlteryxField):
    def __init__(self, name, selected, dataType = "", size = "", rename = ""):
        self.name = name
        self.dataType = dataType
        self.size = size
        self.rename = rename
        self.selected = selected
        
class SummarizeField(AlteryxField):
    def __init__(self, name, selected, dataType = "", size = "", rename = ""):
        self.name = name
        self.dataType = dataType
        self.size = size
        self.rename = rename
