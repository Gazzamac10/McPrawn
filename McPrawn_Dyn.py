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


def createbeamcurve(list):
    for i in range(len(list)):
        if list[1] == "line":
            return Line.ByStartPointEndPoint((Point.ByCoordinates(float(list[2]), float(list[3]), float(list[4]))),
                                             (Point.ByCoordinates(float(list[5]), float(list[6]), float(list[7]))))
        elif list[1] == "arc":
            return Arc.ByThreePoints((Point.ByCoordinates(float(list[2]), float(list[3]), float(list[4]))),
                                     (Point.ByCoordinates(float(list[5]), float(list[6]), float(list[7]))),
                                     (Point.ByCoordinates(float(list[8]), float(list[9]), float(list[10]))))


def createbeamsize(list):
    for i in range(len(list)):
        if list[1] == "line":
            return FromID([possbeamtypes[ifequal(possbeamname, [list[8]])[0]].Id])[0]
        elif list[1] == "arc":
            return FromID([possbeamtypes[ifequal(possbeamname, [list[11]])[0]].Id])[0]


def createcolumncurve(list):
    for i in range(len(list)):
        if list[1] == "line":
            return Line.ByStartPointEndPoint((Point.ByCoordinates(float(list[2]), float(list[3]), float(list[4]))),
                                             (Point.ByCoordinates(float(list[5]), float(list[6]), float(list[7]))))


def createcolumnsize(list):
    for i in range(len(list)):
        if list[1] == "line":
            return FromID([posscolumntypes[ifequal(posscolumnname, [list[8]])[0]].Id])[0]


def revitbeam(listA, listB):
    beamlist = []
    for i in range(len(listA)):
        beamlist.append(StructuralFraming.BeamByCurve(Line.Scale(listA[i], 1000), level[0], listB[i]))
    return beamlist


def revitcol(listA, listB):
    collist = []
    for i in range(len(listA)):
        collist.append(StructuralFraming.ColumnByCurve(Line.Scale(listA[i], 1000), level[0], listB[i]))
    return collist


beamgeo = [createbeamcurve(item) for item in beamlist]
beamsize = [createbeamsize(item) for item in beamlist]
colgeo = [createcolumncurve(item) for item in columnlist]
colsize = [createcolumnsize(item) for item in columnlist]

try:
    errorReport = None
    TransactionManager.Instance.EnsureInTransaction(doc)
    revitbeams = revitbeam(beamgeo, beamsize)
    revitcolumns = revitcol(colgeo, colsize)
    TransactionManager.Instance.TransactionTaskDone()
except:
    # if error accurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()


def getparametersfromlist(list):
    for i in range(len(list)):
        if list[1] == "line":
            return [item.split(":")[0] for item in list[9:]]
        elif list[1] == "arc":
            return [item.split(":")[0] for item in list[12:]]


def getparamValsfromlist(list):
    for i in range(len(list)):
        if list[1] == "line":
            return [item.split(":")[1] for item in list[9:]]
        elif list[1] == "arc":
            return [item.split(":")[1] for item in list[12:]]


beamparams = [getparametersfromlist(item) for item in beamlist]
beamvals = [getparamValsfromlist(item) for item in beamlist]
columnparams = [getparametersfromlist(item) for item in columnlist]
columnvals = [getparamValsfromlist(item) for item in columnlist]


def applyparamaterValue(element, listofparams, listofvals):
    newlist = []
    for i in range(len(listofparams)):
        newlist.append(element.SetParameterByName(listofparams[i], listofvals[i]))
    return newlist[0]


def getP(element, param):
    p = element.Parameters
    for item in p:
        if param == item.Name:
            return item.StorageType


def MgetP(element, listofparams):
    list = []
    for i in range(len(listofparams)):
        list.append(getP(element, listofparams[i]))
    return list


def convertST(storagetypes):
    newlist = []
    for item in storagetypes:
        if "String" == item:
            newlist.append(str)
        elif "Integer" == item:
            newlist.append(int)
        else:
            newlist.append(float)
    return newlist


def Valsconverted(listofstoragetypes, listofvalues):
    return [listofstoragetypes[i](listofvalues[i]) for i in range(len(listofstoragetypes))]


if not beamlist:
    listofBparams = []
else:
    listofBparams = beamparams[0]
    STBeams = [MgetP(item, listofBparams) for item in revitbeams]
    STBCon = [convertST(item) for item in STBeams]
    Bconvertedvalues = [Valsconverted(STBCon[i], beamvals[i]) for i in range(len(beamvals))]

if not columnlist:
    listofCparams = []
else:
    listofCparams = columnparams[0]
    STColumns = [MgetP(item, listofCparams) for item in revitcolumns]
    STCCon = [convertST(item) for item in STColumns]
    Cconvertedvalues = [Valsconverted(STCCon[i], columnvals[i]) for i in range(len(columnvals))]

B = []
if not listofBparams:
    pass
else:
    for i in range(len(revitbeams)):
        B.append(applyparamaterValue(revitbeams[i], beamparams[i], Bconvertedvalues[i]))

C = []
if not listofCparams:
    pass
else:
    for i in range(len(revitcolumns)):
        C.append(applyparamaterValue(revitcolumns[i], columnparams[i], Cconvertedvalues[i]))

OUT = revitbeams, revitcolumns