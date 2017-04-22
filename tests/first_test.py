import shacol

BITS = 14
inputFile = "../hash.txt"

vysledky = dict()

shacol = shacol.Shacol(BITS, inputFile)

for i in range(10, 21):
    shacol.changeBitLength(i)
    shacol.getInfo()
    vysledky = shacol.findCollisionFast()
    print "pro pocet bitu ", i, vysledky
    print "#####################################################"
