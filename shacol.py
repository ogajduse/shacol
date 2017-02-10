#!/usr/bin/env python

import hashlib
import argparse
from StringIO import StringIO

#Input parameters
parser = argparse.ArgumentParser(usage='$prog [options] -sha2 -b 32 -i hash.txt',description='SHA collision finder', add_help=True, epilog='SHA collision finder. Made by Jan Stangler, Ondrej Gajdusek, Sarka Chwastova, VUT FEKT, ICT1 project, 2017')
parser.add_argument('-sha2','--sha256', action='store_true', help='-sha2 (hash algorithm)', required='True')
parser.add_argument('-b','--bits', action='store', dest='bits', help='-b 32 (Number of hash bits to find collision)', required=True)
parser.add_argument('-i','--input', action='store', dest='inputFile', help='-i input.txt The input file with hashes', required=True)
args = parser.parse_args()
#add option to generate random hash?

"""
Use only power of two for binary choice!!!
"""

hashPartLength = int(args.bits)/4
h = hashlib.new('sha256')

try:
    with open(args.inputFile, 'r') as hashInFile:
        #h.update(hashInFile.read(line???)).hexdigest()
        sha256 = hashInFile.read(64) #Block of hash (find hashlengt from library)
        if len(sha256) == 0: #If it got in the end
            print "File is empty! "

#seperate the input hash in cycles from file - future improvement

    if (len(sha256) % hashPartLength == 0): #seperation of hash to n-bits blocks
        hashPart = [sha256[i:i+hashPartLength] for i in range(0, len(sha256), hashPartLength)]
    else:
        print 'Badly aliquot bit value! Use only the power of two... '
except Exception,e:
    print str(e)

#Printing the seperated hashes
for x in hashPart:
    print x

raw_input("\nPress Enter to continue...")

"""
Existence of a class/function(object) which works with a specific part of hash (hashPart[0])
The input of main class would be hash from hashPart.
Finally should be compatible with threading
"""

#main array to save all hashes to compare, must be implemented inside the object!
hashPartArray = []


"""
>>>HELP<<<
#temp_list = []
#temp_list.append("one")
"""

"""
if __name__ == '__main__':
"""
