import os

Path1 = "H:\\Scripting\\McPrawn Development\\Data\\outfromGH.txt"
Path2 = "H:\\Scripting\\McPrawn Development\\Data\\outfromRevit.txt"

f = open(Path1, 'r')
a = f.readlines()

e = open(Path2, 'r')
b = e.readlines()


a = [item.strip() for item in a]
b = [item.strip() for item in b]


unmatched = []
for i in range(len(a)):
    if a[i] != b[i]:
        unmatched.append("unmatched")

print (len(unmatched))

