alteryxPath = 'C:\\Program Files\\Alteryx 11.3\\bin\\RuntimeData\\Macros\\CountRecords.yxmc'

import win32com.client
import AlteryxWorkflow as altxWF

def alteryx_to_visio():
    appVisio = win32com.client.Dispatch("Visio.Application")
    appVisio.Visible =1

    doc = appVisio.Documents.Add("Basic Diagram.vst")
    pagObj = doc.Pages.Item(1)
    stnObj = appVisio.Documents("Basic Shapes.vss")
    mastObj = stnObj.Masters("Rectangle")

    altWf = altxWF.AlteryxWorkflow()
    altWf.loadWorkflow(alteryxPath)    

    visio_obj = {}
    
    #Create visio shape objects
    for key in  altWf.altToolDict:
        shpObj = pagObj.Drop(mastObj, altWf.altToolDict[key].x, altWf.altToolDict[key].y)
        shpObj.Text = altWf.altToolDict[key].toolType + " (" + key + ")"
        visio_obj[key] = shpObj
        
    pagObj.ResizeToFitContents()
    
    #create connections between objects
    for origkey in  altWf.altToolDict:
        #connectorMaster = appVisio.Application.ConnectorToolDataObject
        for destKey in altWf.altToolDict[origkey].consOut:
            origObj = visio_obj[origkey]
            destObj = visio_obj[destKey]

            origObj.AutoConnect(destObj,0)

if __name__ == "__main__":
    alteryx_to_visio()
