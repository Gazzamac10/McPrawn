import rhinoscriptsyntax as rs
import clr
import os
clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree

import os
import os.path

a = [str(rs.coerce3dpoint(x[i]).X)+","+str(rs.coerce3dpoint(x[i]).Y)+","+\
str(rs.coerce3dpoint(y[i]).X)+","+str(rs.coerce3dpoint(y[i]).Y)for i in range(len(x))]


Path = "H:\Scripting\McPrawn Development\Data\outfromGH.txt"

f = open(Path,"w") #opens file with name of "test.txt"
for item in a:
    f.write("%s\n" % item)
f.close()