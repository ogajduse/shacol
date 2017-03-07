bitcount = 2
triesize = 2
for i in range(2, 101):
    triesize = triesize + 2 ** i
    arraysize = (2 ** bitcount) * bitcount
    print "Bits:  ", bitcount
    print "TRIE:  ", triesize, "b, ", triesize / 8 / (1024**3), "GB"
    print "ARRAY: ", arraysize, "b, ", arraysize / 8 /(1024**3), "GB"
    print "You will save with trie: ", (arraysize - triesize)/8/(1024**3), "GB"
    bitcount += 1
    print "_______________________________________"
