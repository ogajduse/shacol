import shacol

sha256 = True
BITS = 14
inputFile = "../input.txt"

vysledky = dict()

shacol = shacol.Shacol(sha256, BITS, inputFile)
vysledky = shacol.findCollisionFast()
