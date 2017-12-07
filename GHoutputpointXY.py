import rhinoscriptsyntax as rs
import clr
import os
clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree

import os
import os.path


def getcofromline(string):
    output = []
    for item in string:
        output.append(str(round(float(item.split(",")[2]),6))+","+str(round(float(item.split(",")[3]),6))\
        +","+str(round(float(item.split(",")[5]),6))+","+str(round(float(item.split(",")[6]),6)))
    return output

a = getcofromline(x)

Path = "H:\Scripting\McPrawn Development\Data\outfromGH.txt"

if Activate == True:
    f = open(Path,"w") #opens file with name of "test.txt"
    for item in a:
        f.write("%s\n" % item)
    f.close()