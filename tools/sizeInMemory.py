bitcount = 2
triesize = 2
for i in range(2, 101):
    triesize = triesize + 2 ** i
    arraysize = (2 ** bitcount) * bitcount
    print("Bits:  " + str(bitcount))
    print("TRIE:  " + str(triesize) + " b, " + str(triesize / 8 / (1024 ** 3)) + " GB")
    print("ARRAY: " + str(arraysize) + " b, " + str(arraysize / 8 / (1024 ** 3)) + " GB")
    print("You will save with trie: " + str((arraysize - triesize) / 8 / (1024 ** 3))+ " GB")
    bitcount += 1
    print("_______________________________________")
