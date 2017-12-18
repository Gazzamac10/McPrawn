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

x = IN[0]

x = [item for sublist in x for item in sublist]

marks = [item.GetParameterValueByName("Mark") for item in x]
marks = [float(item) for item in marks]


def getitemlocation(list):
    loc = []
    Slocp = []
    for j in list:
        loc.append(j.Location)
    for k in loc:
        Slocp.append(str((round(k.StartPoint.X / 1000,6))) + "," + str((round(k.StartPoint.Y / 1000,6))) + "," + str(
            (round(k.EndPoint.X / 1000,6))) + "," + str((round(k.EndPoint.Y / 1000,6))))
    return Slocp


output = getitemlocation(x)


t = [x for y, x in sorted(zip(marks, output))]

OUT = t

Path = "H:\Scripting\McPrawn Development\Data\outfromRevit.txt"

Activate = IN[1]

if Activate == True:
	f = open(Path,"w") #opens file with name of "test.txt"
	for item in OUT:
	    f.write("%s\n" % item)
	f.close()


