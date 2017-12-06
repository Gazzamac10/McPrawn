import clr

clr.AddReference('ProtoGeometry')
clr.AddReference('ProtoGeometry')
clr.AddReference("RevitNodes")
clr.AddReference("RevitServices")
clr.AddReference("RevitAPI")
import Revit
import System
import RevitServices
import Autodesk
from Revit.Elements import *
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
from Autodesk.DesignScript.Geometry import *

doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application

Path = IN[1]
if IN[0] == True:
    f = open(Path, 'r')
    a = f.readlines()

a = [item.strip() for item in a]
beams = []
columns = []
for item in a:
    if "beam" in item:
        beams.append(item)
    elif "column" in item:
        columns.append(item)
    else:
        break
beamlist = [item.split(",") for item in beams]
columnlist = [item.split(",") for item in columns]


def FromID(x):
    items = x
    elementlist = list()
    unmatched = list()
    for item in items:
        try:
            elementlist.append(doc.GetElement(item).ToDSType(True))
        except:
            unmatched.append(item)
    return (elementlist, unmatched)[0]


def getlevel(levelname):
    alllevels = FilteredElementCollector(doc).OfClass(Level).ToElements()
    alllevelnames = [item.Name for item in alllevels]
    if levelname in alllevelnames:
        for i in range(len(alllevels)):
            if levelname == alllevelnames[i]:
                level = [alllevels[i]]
    else:
        level = [alllevels[0]]
    return level


level = getlevel("Level 0")[0]
level = FromID([UnwrapElement(level).Id])


def gettypesofcat(name):
    userCategories = doc.Settings.Categories
    names, ids, builtInNames = [], [], []
    for i in userCategories:
        names.append(i.Name)
        ids.append(i.Id.IntegerValue)
        tempID = i.Id.IntegerValue
        builtInNames.append(System.Enum.ToObject(BuiltInCategory, tempID))
    catname = name
    if catname in names:
        for i in range(len(names)):
            if catname == names[i]:
                cat = builtInNames[i]
    else:
        cat = "No Category Found"
    return FilteredElementCollector(doc).OfCategory(cat).ToElements()


possbeamtypes = gettypesofcat("Structural Framing")
posscolumntypes = gettypesofcat("Structural Columns")


def getparametervalue(elements, parameter):
    values = []
    if hasattr(elements, "__iter__"):
        output = []
        for elem in elements:
            if hasattr(elem, "__iter__"):
                vals = []
                for e in elem:
                    for p in elem.Parameters:
                        if p.Definition.Name == parameter:
                            parm = p.AsValueString()
                            if (parm is None):
                                parm = p.AsString()
                    vals.append(parm)
                values.append(vals)
            else:
                for p in elem.Parameters:
                    if p.Definition.Name == parameter:
                        parm = p.AsValueString()
                        if (parm is None):
                            parm = p.AsString()
                values.append(parm)
        output.append(values)
    else:
        parm = elements.Parameter[parameter].AsValueString()
        output = parm
    return output[0]


possbeamname = getparametervalue(possbeamtypes, "Type Name")
posscolumnname = getparametervalue(posscolumntypes, "Type Name")


def ifequal(b, a):
    indiceslist = []
    for lA in a:
        counter = 0
        for lB in b:
            if (lA == lB):
                indiceslist.append(counter)
            counter += 1
    return indiceslist


beamsize = []
for item in beamlist:
    if "line" == item[1]:
        beamsize.append(item[8])
    elif "arc" == item[1]:
        beamsize.append(item[11])

columnsize = []
for item in columnlist:
    columnsize.append(item[8])

beamcheck = ifequal(possbeamname, beamsize)
columncheck = ifequal(posscolumnname, columnsize)


def checkmatch(lista, listb):
    if len(lista) == len(listb):
        return "Matched"
    else:
        return "Not Matched"


OUT = checkmatch(beamcheck, beamsize), checkmatch(columncheck, columnsize)