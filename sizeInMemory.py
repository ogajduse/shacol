bitcount = 2
triesize = 2
for i in range(2, 70):
    triesize = triesize + 2 ** i
    arraysize = (2 ** bitcount) * bitcount
    print "Bits:  ", bitcount
    print "TRIE:  ", triesize, "b, ", triesize / 8 / 1024 / 1024 / 1024, "GB"
    print "ARRAY: ", arraysize, "b, ", arraysize / 8 / 1024 / 1024 / 1024, "GB"
    bitcount += 1
    print "_______________________________________"
