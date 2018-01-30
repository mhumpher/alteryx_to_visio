#Using Python to generate Visio Documents
#https://technofrustration.blogspot.com/2007/10/using-python-to-automate-visio.html
#Dive Into Python 3 by Mark Pilgrim
#Chapter 12: XML
#http://www.diveintopython3.net/xml.html

#source file
alteryxPath = ""

import xml.etree.ElementTree as etree
import win32com.client

def nodeScan(nodes):
    nodelst = []
    for node in nodes:
        #check if node is a macro
        guiSet = node.find('GuiSettings')
        if bool(guiSet.attrib):
            tooltype = guiSet.attrib['Plugin'].split('.')[-1]
        else: 
            tooltype = node.find("EngineSettings").attrib['Macro']
        
        #check if node is a tool contianer
        if tooltype == 'ToolContainer':
            childNodes = node.find('ChildNodes').findall('Node')
            nodelst = nodelst + nodeScan(childNodes)
        else:
            toolID = node.attrib['ToolID']
            x = float(guiSet.find('Position').attrib['x'])/50
            #Alteryx is up down positive, whereas Visio is down up
            y = -1*float(guiSet.find('Position').attrib['y'])/50 
            nodelst.append([toolID, x, y, tooltype])
    return nodelst

def alteryx_to_visio():
    appVisio = win32com.client.Dispatch("Visio.Application")
    appVisio.Visible =1

    doc = appVisio.Documents.Add("Basic Diagram.vst")
    pagObj = doc.Pages.Item(1)
    stnObj = appVisio.Documents("Basic Shapes.vss")
    mastObj = stnObj.Masters("Rectangle")

    tree = etree.parse(alteryxPath)
    root = tree.getroot()
    nodes = root.findall('./Nodes/Node')
    cons = root.findall('./Connections/Connection')

    visio_obj = {}

    nodelist = nodeScan(nodes)
    for nodeItem in  nodelist:
        toolID = nodeItem[0]
        x = nodeItem[1]
        y = nodeItem[2]
        tooltype = nodeItem[3]
        shpObj = pagObj.Drop(mastObj, x, y)
        shpObj.Text = tooltype
        visio_obj[toolID] = shpObj

    for con in cons:
        connectorMaster = appVisio.Application.ConnectorToolDataObject
        originID = con.find('Origin').attrib['ToolID']
        destID = con.find('Destination').attrib['ToolID']
        origObj = visio_obj[originID]
        destObj = visio_obj[destID]
    
        connector = pagObj.Drop(connectorMaster, 0, 0)
        connector.Cells("BeginX").GlueTo(origObj.Cells("PinX"))
        connector.Cells("EndX").GlueTo(destObj.Cells("PinX"))

if __name__ == "__main__":
    alteryx_to_visio()
    
