#!/usr/bin/env python
import os
import time
#import Queue
import hashlib
import argparse
#import threading
#import linecache
from sets import Set
from collections import deque
from StringIO import StringIO
import re, sys, getopt

#Input parameters
parser = argparse.ArgumentParser(usage='$prog [options] -sha2 -b 32 -i hash.txt',description='SHA collision finder', add_help=True, epilog='SHA collision finder. Made by Jan Stangler, Ondrej Gajdusek, Sarka Chwastova, VUT FEKT, ICT1 project, 2017')
parser.add_argument('-sha2','--sha256', action='store_true', dest='sha256', help='-sha2 (hash algorithm)', required=True)
parser.add_argument('-b','--bits', action='store', dest='bits', help='-b 32 (Number of hash bits to find collision)', required=True)
parser.add_argument('-i','--input', action='store', dest='inputFile', help='-i input.txt The input file with hashes', required=True)
parser.add_argument('-hh','--hash', action='store_true', dest='hash', help='-h The input file has hashes inside', required=False)
parser.add_argument('-t','--text', action='store_true', dest='text', help='-t The input file has text inside', required=False)
parser.add_argument('-f','--first', action='store_true', dest='first', help='-f Collision with the first one hash', required=False)
args = parser.parse_args()

try:
    with open(args.inputFile, 'r') as dataFromFile:
        if (args.text):
            text = dataFromFile.read()
            sha256 = hashlib.sha256(text).hexdigest()
        else:
            if (args.sha256):
                sha256 = dataFromFile.read(64) #Block of hash

        if len(sha256) == 0: #If it got in the end
            print "File is empty! "

    hashPartLength = int(args.bits)/4

    """ Ready for threading
    if (len(sha256) % hashPartLength == 0): #seperation of hash to n-bits blocks
        hashPart = [sha256[i:i+hashPartLength] for i in range(0, len(sha256), hashPartLength)]
    else:
        print 'Badly aliquot bit value! Use only the power of two... '
    """
    hashPart = sha256[0:hashPartLength]

except Exception,e:
    print str(e)

#Printing the seperated hashes (just for testing)
#print '\nInput hash:', hashPart

raw_input('\nPress Enter to continue...')

class Shacol:
    def findCollisionServer(self, hashPart=None): #Hnusna metoda, ktera je rychla a bezi na serveru
        """
        Function to be thread by individually calling - looking for a collision hashPart
        """
        try:
            hashPartSet = Set([])
            hashPartSet2 = Set([])
            hashPartSet3 = Set([])
            hashPartSet4 = Set([])
            hashPartSet5 = Set([])
            hashPartSet6 = Set([])
            hashPartSet7 = Set([])
            hashPartSet8 = Set([])
            hashPartSet9 = Set([])
            hashPartSet10 = Set([])
            hashPartSet11 = Set([])
            hashPartSet12 = Set([])
            hashPartSet13 = Set([])
            hashPartSet14 = Set([])
            hashPartSet15 = Set([])
            hashPartSet16 = Set([])
            hashPartSet17 = Set([])
            hashPartSet18 = Set([])
            hashPartSet19 = Set([])
            hashPartSet20 = Set([])
            hashPartSet21 = Set([])
            hashPartSet22 = Set([])
            hashPartSet23 = Set([])
            hashPartSet24 = Set([])
            hashPartSet25 = Set([])

            hashPartLength = len(hashPart)
            newHashPart = hashPart

            count = 0

            startTime = time.time()
            while newHashPart not in (hashPartSet or hashPartSet2 or hashPartSet3 or hashPartSet4 or hashPartSet5 or hashPartSet6 or hashPartSet7 or hashPartSet8 or hashPartSet9 or hashPartSet10 or hashPartSet11 or hashPartSet12 or hashPartSet13 or hashPartSet14 or hashPartSet15 or hashPartSet16 or hashPartSet17 or hashPartSet18 or hashPartSet19 or hashPartSet20 or hashPartSet21 or hashPartSet22 or hashPartSet23 or hashPartSet24 or hashPartSet25):
                if count <= 85000000:
                    hashPartSet.add(newHashPart)
                elif count <= 170000000:
                    hashPartSet2.add(newHashPart)
                elif count <= 255000000:
                    hashPartSet3.add(newHashPart)
                elif count <= 340000000:
                    hashPartSet4.add(newHashPart)
                elif count <= 425000000:
                    hashPartSet5.add(newHashPart)
                elif count <= 505000000:
                    hashPartSet6.add(newHashPart)
                elif count <= 590000000:
                    hashPartSet7.add(newHashPart)
                elif count <= 675000000:
                    hashPartSet8.add(newHashPart)
                elif count <= 760000000:
                    hashPartSet9.add(newHashPart)
                elif count <= 845000000:
                    hashPartSet10.add(newHashPart)
                elif count <= 930000000:
                    hashPartSet11.add(newHashPart)
                elif count <= 1010000000:
                    hashPartSet12.add(newHashPart)
                elif count <= 1090000000:
                    hashPartSet13.add(newHashPart)
                elif count <= 1170000000:
                    hashPartSet14.add(newHashPart)
                elif count <= 1250000000:
                    hashPartSet15.add(newHashPart)
                elif count <= 1330000000:
                    hashPartSet16.add(newHashPart)
                elif count <= 1410000000:
                    hashPartSet17.add(newHashPart)
                elif count <= 1490000000:
                    hashPartSet18.add(newHashPart)
                elif count <= 1570000000:
                    hashPartSet19.add(newHashPart)
                elif count <= 1650000000:
                    hashPartSet20.add(newHashPart)
                elif count <= 1730000000:
                    hashPartSet21.add(newHashPart)
                elif count <= 1810000000:
                    hashPartSet22.add(newHashPart)
                elif count <= 1890000000:
                    hashPartSet23.add(newHashPart)
                elif count <= 1970000000:
                    hashPartSet24.add(newHashPart)
                elif count <= 2050000000:
                    hashPartSet25.add(newHashPart)

                count += 1
                if count % 10000000 == 0 : print count
                newHash = hashlib.sha256(newHashPart).hexdigest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
            #In case of threding is needed the solution for number of position every thread!!!
            totalTime = round(time.time() - startTime, 12)
            print('\nPrevious Server method - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            #print 'GetSizeOf:', sys.getsizeof(hashPartSet)
            print 'Count of the cycles:',count
            print 'Collision hash:', newHashPart

            #hashPartList = list(hashPartSet)
            #print 'Index of collision part:', hashPartList.index(newHashPart)
            #.clear()
            return newHashPart
        except Exception,e:
            print str(e)

    def findCollisionSetArray(self, hashPart=None): #Tady je ten zadrhel....
        """
        Function to be thread by individually calling - looking for a collision hashPart
        """
        #Promyslet tvorbu vlakna, ktere bude prubezne hlidat zaplneni setu
        try:
            setIter = 0
            count = 0
            setCount = 80000000 #50-85 milions per set
            setNumber = 30 #number of sets

            setArray = [Set() for _ in xrange(setNumber)]

            hashPartLength = len(hashPart)
            newHashPart = hashPart
            startTime = time.time()

            while newHashPart not in setArray[Set() in xrange(setNumber)]: #Zkuste najit chybu, proc to hleda jine kolize :(
                setArray[setIter].add(newHashPart)
                count += 1
                if count == setCount : setIter += 1
                if count % 10000000 == 0 : print count
                newHash = hashlib.sha256(newHashPart).hexdigest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading

            totalTime = round(time.time() - startTime, 12)
            print('\nSetArray method - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            #print 'GetSizeOf:', sys.getsizeof(hashPartSet)

            print 'Count of the cycles:', len(setArray[Set() in xrange(setNumber)])
            print 'Collision hash:', newHashPart

            indexofcollision = int()
            iterace=0
            for i in setArray:
                indexofcollision = list(i).index(newHashPart)
                if indexofcollision:
                    indexofcollision += iterace*setCount
                    break
                iterace += 1

            print 'Index of collision hash:', indexofcollision

            return newHashPart

        except Exception,e:
            print str(e)

    def findCollisionString(self, hashPart=None):
        """
        Function to be thread by individually calling - looking for a collision hashPart
        """

        try:
            hashPartString = ''
            hashPartLength = len(hashPart)
            newHashPart = hashPart
            #count = 0

            #s.find("is") == -1
            startTime = time.time()
            while newHashPart not in hashPartString: #in range(0, len(newHashPart), hashPartLength)):
                hashPartString += newHashPart + '|'
                #hashPartString.join(newHashPart)
                newHash = hashlib.sha256(newHashPart).hexdigest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
                #print hashPartString
                #count += 1
                #print count,' : ',newHashPart
                #In case of threding is needed the solution for number of position every thread!!!
            totalTime = round(time.time() - startTime, 12)
            print('\nSTRING - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            print 'GetSizeOf:', sys.getsizeof(hashPartString)
            #print 'Count of the cycles:', count
            print 'Collision hash:', newHashPart
            #.clear()
            return newHashPart
        except Exception,e:
            print str(e)

    def findCollisionDigest(self, hashPart=None):
        """
        Function to be thread by individually calling - looking for a collision hashPart
        """
        try:
            hashPartSet = Set([])
            hashPartLength = len(hashPart)
            newHashPart = hashPart
            startTime = time.time()
            while newHashPart not in hashPartSet:
                hashPartSet.add(newHashPart)
                #print count,' : ',newHashPart
                #count += 1
                newHash = hashlib.sha256(newHashPart).digest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
            #In case of threding is needed the solution for number of position every thread!!!
            totalTime = round(time.time() - startTime, 12)
            print('\nSET with DIGEST - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            print 'GetSizeOf:', sys.getsizeof(hashPartSet)
            print 'Count of the cycles:', len(hashPartSet)
            print 'Collision hash:', newHashPart
            hashPartList = list(hashPartSet)
            print 'Index of collision part:', hashPartList.index(newHashPart)

            #.clear()
            return newHashPart
        except Exception,e:
            print str(e)

shacol = Shacol() #Instance of the class Shacol

shacol.findCollisionServer(hashPart)
shacol.findCollisionSetArray(hashPart)

#shacol.findCollisionArraySet(hashPart)
#shacol.findCollisionString(hashPart)
#shacol.findCollisionSet(hashPart)
#shacol.findCollisionDigest(hashDigest)


#There will be difference and dependence between threads in the index hashPart[0]...
#myData = threading.local()


"""
shacol.findCollision('4c07a78baec4') #48 bit
shacol.findCollision('4c07a78baec4b63') #60 bit
shacol.findCollision('4c07a78baec4b6309ab6') #80 bit
shacol.findCollision('4c07a78baec4b6309ab60f2a1') #100 bit
"""

#main function???
"""
if __name__ == '__main__':
        try:
    	    account = sys.argv[1]
            n = int(sys.argv[2])
            m = int(sys.argv[3])
            url = sys.argv[4]

        except Exception, e:
    	print e
    	print 'Error... program is going to be exit...'
    	sys.exit()

        try:
            form = sys.argv[5]

        except Exception, e:
            form = 'account'
    """
