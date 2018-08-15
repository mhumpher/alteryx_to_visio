# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:24:50 2018

@author: mhumpher
"""

class AlteryxConnection:
    def __init__(self, con_xml, origin_obj, dest_obj):
        self.__connection_xml__ = con_xml
        self.con_name = self.__connection_xml__.get('name', '')
        self.origID = self.__connection_xml__.find('Origin').attrib['ToolID']
        self.origCon = self.__connection_xml__.find('Origin').attrib['Connection']
        self.destID = self.__connection_xml__.find('Destination').attrib['ToolID']
        self.destCon = self.__connection_xml__.find('Destination').attrib['Connection']
        self.origTool = origin_obj
        self.destTool = dest_obj
        
        if self.origID != self.origTool.toolId:
            raise ValueError('Origin tool object toolID did not match connection xml toolID')
        
        if self.destID != self.destTool.toolId:
            raise ValueError('Destination tool object toolID did not match connection xml toolID')
            
