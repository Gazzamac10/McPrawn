import rhinoscriptsyntax as rs
import Grasshopper.Kernel.Data as ghp
import Grasshopper.DataTree as ghdt

inputlist = []
for i in range(len(ghenv.Component.Params.Input)):
    inputlist.append(ghenv.Component.Params.Input[i])


def infoinlist(x):
    b = []
    for item in x.VolatileData:
        b.append(item)
    return b


paramlist = []
for item in inputlist:
    paramlist.append(infoinlist(item))

paramnamelist = []
for item in inputlist:
    paramnamelist.append(item.Name)

c = []
for input in ghenv.Component.Params.Input:
    for s in input.Sources:
        attr = s.Attributes
        if (attr is None) or (attr.GetTopLevel is None):
            pass
        else:
            component = attr.GetTopLevel.DocObject
        c.append(component.NickName)

j = c
k = paramlist


def concat(j, k):
    list = []
    for item in k:
        list.append(c[i] + ":" + str(item))
    return list


paramconcat = []
for i in range(len(k)):
    paramconcat.append(concat(c, k[i]))


def Getendpoints(Curve):
    x = rs.CurveStartPoint(Curve)
    y = rs.CurveEndPoint(Curve)
    z = rs.CurveMidPoint(Curve)
    startP = x.X, x.Y, x.Z
    MidP = z.X, z.Y, z.Z
    EndP = y.X, y.Y, y.Z
    if rs.CurveDegree(Curve) == 2:
        return str(startP) + "," + str(MidP) + "," + str(EndP)
    elif rs.CurveDegree(Curve) == 1:
        return str(startP) + "," + str(EndP)
    else:
        return "Invalid Curve"


def ArcorCurve(Curve):
    if rs.CurveDegree(Curve) == 2:
        return "arc"
    elif rs.CurveDegree(Curve) == 1:
        return "line"
    else:
        return "Invalid Curve"


bc = []
p = []
s = []
for i in range(len(curve)):
    p.append(Getendpoints(curve[i]))
    bc.append("beam")
    s.append("UB127x76x13")

p = [item.strip().replace("(", "") for item in p]
p = [item.strip().replace(")", "") for item in p]
p = [item.replace(" ", "") for item in p]

if len(curve) != len(BeamOrColumn):
    BeamOrColumn = bc
if len(curve) != len(size):
    size = s

Filter = []
for i in range(len(curve)):
    Filter.append(ArcorCurve(curve[i]))

a = [BeamOrColumn[i] + "," + Filter[i] + "," + p[i] + "," + size[i] for i in range(len(curve))]


def tostring(list):
    return [str(item) for item in list]


if len(paramlist) > 3:
    params = map(list, zip(*[tostring(item) for item in (paramconcat[3:(len(paramconcat))])]))
    strparam = [",".join(item) for item in params]
    if strparam:
        comblist = [(a[i] + "," + strparam[i]) for i in range(len(a))]
else:
    comblist = a

a = comblist



