# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:59:36 2018

@author: mhumpher
"""

class AlteryxTool:
    #consIn = {}
    #consOut = {}    
    
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
        pass