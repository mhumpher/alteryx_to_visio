class AlteryxFormula:
    def __init__(self, expression, field, size, dataType):
        self.formula = expression
        self.field = field
        self.size = size
        self.dataType = dataType
        self.fieldDep = {}
