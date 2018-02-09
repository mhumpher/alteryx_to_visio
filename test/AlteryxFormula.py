import AlteryxField

class AlteryxFormula:
    def __init__(self, expression, field, size, dataType):
        #assume formula is normalized in workflow load
        self.formula = expression
        self.field = AlteryxField(field, size,dataType)
        self.fieldDep = {}
        
    #Parse the field expression to determine field dependencies
    def parseExpFields(self):
        pass
        
