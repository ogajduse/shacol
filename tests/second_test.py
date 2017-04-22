import shacol

BITS = 32
inputFile = "../hash.txt"
hashGroup = True

vysledky = dict()

shacol = shacol.Shacol(BITS, inputFile, hashGroup)
print shacol.shaList
shacol.findCollisionStr(shacol.shaList[0])
shacol.findCollisionStr(shacol.shaList[1])
shacol.findCollisionStr(shacol.shaList[2])
