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
        altTool = altWf.altToolDict[key]
        shpObj = pagObj.Drop(mastObj, altTool.x, altTool.y)
        if altTool.toolType == 'Formula':
            text = altTool.toolType + " (" + key + ")"
            for f in altTool.fields:
                text = text + "\n " + altTool.fields[f].name + " = " + altTool.fields[f].formulaExp
            shpObj.Text = text
        elif altTool.toolType == 'AlteryxSelect':
            text = altTool.toolType + " (" + key + ")"
            for f in altTool.fields:
                text = text + "\n " + altTool.fields[f].name
            shpObj.Text = text
        else:
            shpObj.Text = altTool.toolType + " (" + key + ")"
        visio_obj[key] = shpObj
        
    pagObj.ResizeToFitContents()
    
    #create connections between objects
    for origkey in  altWf.altToolDict:
        for destKey in altWf.altToolDict[origkey].consOut:
            origObj = visio_obj[origkey]
            destObj = visio_obj[destKey]

            origObj.AutoConnect(destObj,0)
            
if __name__ == "__main__":
    alteryx_to_visio()
