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
import redis

class Shacol:
    def __init__(self, sha256, bits, inputFile, hashGroup=False, text=False, first=False):
        self.sha256 = sha256
        self.bits = int(bits)
        self.inputFile = inputFile
        self.hashGroup = hashGroup
        self.text = text
        self.first = first

        self.hashPartLength = int(self.bits)/4
        self.shaList = []
        self.hashPart = str()

        with open(self.inputFile, 'r') as dataFromFile:
            if (self.text):
                text = dataFromFile.read()
                self.shaList += hashlib.sha256(text).hexdigest()
            else:
                if (self.sha256):
                    #print dataFromFile.readline()
                    for hash in dataFromFile:
                        self.shaList.append(hash[0:self.hashPartLength])
        dataFromFile.close()

    """ Ready for threading - not be real with set (just with slower database)
    if (len(sha256) % hashPartLength == 0): #seperation of hash to n-bits blocks
        hashPart = [sha256[i:i+hashPartLength] for i in range(0, len(sha256), hashPartLength)]
    else:
        print 'Badly aliquot bit value! Use only the power of two... '
    """

    def getinfo(self):
        printhashes = str()
        for i in self.shaList:
            printhashes += i +'\t'

        print('\nYou are trying to find a collision with %s hash for %db with SHA-2.\n' % ('first' if self.first else
                                                                                           'arbitary', self.bits) +
              'Using %s as input file with %s.' % (self.inputFile,
                                                   'one hash inside' if not self.hashGroup else
                                                   'with one hash per line inside.') +
              '\nInput %s %s' % ('hash is  ' if not self.hashGroup else 'hashes are ', self.hashPart if not self.hashGroup else printhashes))

    def findCollisionFast(self, hashPart=None):
        """
        Best performance function - high RAM load
        """
        try:
            if not hashPart:
                hashPart = self.hashPart
            print '\nInput hashPart:', hashPart
            hashPartSet = Set()
            hashPartSet2 = Set()
            hashPartSet3 = Set()
            hashPartSet4 = Set()
            hashPartSet5 = Set()
            hashPartSet6 = Set()
            hashPartSet7 = Set()
            hashPartSet8 = Set()
            hashPartSet9 = Set()
            hashPartSet10 = Set()
            hashPartSet11 = Set()
            hashPartSet12 = Set()
            hashPartSet13 = Set()
            hashPartSet14 = Set()
            hashPartSet15 = Set()
            hashPartSet16 = Set()
            hashPartSet17 = Set()
            hashPartSet18 = Set()
            hashPartSet19 = Set()
            hashPartSet20 = Set()
            hashPartSet21 = Set()
            hashPartSet22 = Set()
            hashPartSet23 = Set()
            hashPartSet24 = Set()
            hashPartSet25 = Set()
            hashPartSet26 = Set()
            hashPartSet27 = Set()
            hashPartSet28 = Set()
            hashPartSet29 = Set()
            hashPartSet30 = Set()
            hashPartSet31 = Set()
            hashPartSet32 = Set()
            hashPartSet33 = Set()
            hashPartSet34 = Set()
            hashPartSet35 = Set()
            hashPartSet36 = Set()
            hashPartSet37 = Set()
            hashPartSet38 = Set()
            hashPartSet39 = Set()

            hashPartLength = len(hashPart)
            newHashPart = hashPart
            count = 0

            startTime = time.time()
            while newHashPart not in (hashPartSet or hashPartSet2 or hashPartSet3 or hashPartSet4 or hashPartSet5 or hashPartSet6 or hashPartSet7 or hashPartSet8 or hashPartSet9 or hashPartSet10 or hashPartSet11 or hashPartSet12 or hashPartSet13 or hashPartSet14 or hashPartSet15 or hashPartSet16 or hashPartSet17 or hashPartSet18 or hashPartSet19 or hashPartSet20 or hashPartSet21 or hashPartSet22 or hashPartSet23 or hashPartSet24 or hashPartSet25 or hashPartSet26 or hashPartSet27 or hashPartSet28 or hashPartSet29 or hashPartSet30 or hashPartSet31 or hashPartSet32 or hashPartSet33 or hashPartSet34 or hashPartSet35 or hashPartSet36 or hashPartSet37 or hashPartSet38 or hashPartSet39):
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
                elif count <= 2050000000:
                    hashPartSet26.add(newHashPart)
                elif count <= 2050000000:
                    hashPartSet27.add(newHashPart)
                elif count <= 2130000000:
                    hashPartSet28.add(newHashPart)
                elif count <= 2210000000:
                    hashPartSet29.add(newHashPart)
                elif count <= 2290000000:
                    hashPartSet30.add(newHashPart)
                elif count <= 2370000000:
                    hashPartSet31.add(newHashPart)
                elif count <= 2450000000:
                    hashPartSet32.add(newHashPart)
                elif count <= 2530000000:
                    hashPartSet33.add(newHashPart)
                elif count <= 2610000000:
                    hashPartSet34.add(newHashPart)
                elif count <= 2690000000:
                    hashPartSet35.add(newHashPart)
                elif count <= 2770000000:
                    hashPartSet36.add(newHashPart)
                elif count <= 2850000000:
                    hashPartSet37.add(newHashPart)
                elif count <= 2930000000:
                    hashPartSet38.add(newHashPart)
                else:
                    hashPartSet39.add(newHashPart)

                count += 1
                if count % 10000000 == 0 : print count
                newHash = hashlib.sha256(newHashPart).hexdigest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
            #In case of threding is needed the solution for number of position every thread!!!
            totalTime = round(time.time() - startTime, 12)
            print('Fast Method - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            #print 'GetSizeOf:', sys.getsizeof(hashPartSet)
            print 'Count of the cycles:',count
            print 'Collision hash:', newHashPart


            hashPartSet.clear()
            hashPartSet2.clear()
            hashPartSet3.clear()
            hashPartSet4.clear()
            hashPartSet5.clear()
            hashPartSet6.clear()
            hashPartSet7.clear()
            hashPartSet8.clear()
            hashPartSet9.clear()
            hashPartSet10.clear()
            hashPartSet11.clear()
            hashPartSet12.clear()
            hashPartSet13.clear()
            hashPartSet14.clear()
            hashPartSet15.clear()
            hashPartSet16.clear()
            hashPartSet17.clear()
            hashPartSet18.clear()
            hashPartSet19.clear()
            hashPartSet20.clear()
            hashPartSet21.clear()
            hashPartSet22.clear()
            hashPartSet23.clear()
            hashPartSet24.clear()
            hashPartSet25.clear()
            hashPartSet26.clear()
            hashPartSet27.clear()
            hashPartSet28.clear()
            hashPartSet29.clear()
            hashPartSet30.clear()
            hashPartSet31.clear()
            hashPartSet32.clear()
            hashPartSet33.clear()
            hashPartSet34.clear()
            hashPartSet35.clear()
            hashPartSet36.clear()
            hashPartSet37.clear()
            hashPartSet38.clear()
            hashPartSet39.clear()
        except Exception,e:
            print str(e)

    def findCollisionSets(self, hashPart=None): #Hnusna metoda, ktera je rychla a bezi na serveru
        """
        Function to be thread by individually calling - looking for a collision hashPart
        """
        try:
            print 'Input hashPart:', hashPart
            hashPartSet1 = Set([])
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
            hashesInSet = 85000000
            count = 0

            actualSetNumber = 0
            startTime = time.time()
            while newHashPart not in (hashPartSet1 or hashPartSet2 or hashPartSet3 or hashPartSet4 or hashPartSet5 or hashPartSet6 or hashPartSet7 or hashPartSet8 or hashPartSet9 or hashPartSet10 or hashPartSet11 or hashPartSet12 or hashPartSet13 or hashPartSet14 or hashPartSet15 or hashPartSet16 or hashPartSet17 or hashPartSet18 or hashPartSet19 or hashPartSet20 or hashPartSet21 or hashPartSet22 or hashPartSet23 or hashPartSet24 or hashPartSet25):
                if not count % hashesInSet == 0:
                    locals()['hashPartSet%s' % actualSetNumber].add(newHashPart)
                else:
                    actualSetNumber+=1
                    locals()['hashPartSet%s' % actualSetNumber].add(newHashPart)

                count += 1
                if count % 10000000 == 0 : print count
                newHash = hashlib.sha256(newHashPart).hexdigest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
            #In case of threading is needed the solution for number of position every thread!!!
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

            while newHashPart not in setArray[Set() in xrange(setNumber)]:
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

    def findCollisionWithDBSet(self, hashPart=None):
        """
        Function is looking for a collision with hashPart
        """
        try:
            pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
            r = redis.Redis(connection_pool=pool)
            r.flushdb()

            if not hashPart:
                hashPart = r

            count = 0
            hashPartLength = len(hashPart)
            startTime = time.time()
            while not r.sismember('hset', hashPart):
                r.sadd('hset', hashPart)
                count += 1
                if count % 10000000 == 0 : print count
                hashPart = hashlib.sha256(hashPart).hexdigest()[0:hashPartLength]

            totalTime = round(time.time() - startTime, 12)
            print('\nDBSet method - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            #print 'GetSizeOf:', sys.getsizeof(hashPartSet)

            print 'Count of the cycles:', r.scard('hset')
            print 'Collision hash:', hashPart

        except Exception,e:
            print str(e)

def main():
    #Input parameters
    parser = argparse.ArgumentParser(usage='$prog [options] -sha2 -b 32 -i hash.txt',description='SHA collision finder', add_help=True, epilog='SHA collision finder. Written by Jan Stangler, Ondrej Gajdusek, Sarka Chwastova, VUT FEKT, ICT1 project, 2017')
    parser.add_argument('-sha2','--sha256', action='store_true', dest='sha256', help='-sha2 (hash algorithm)', required=True)
    parser.add_argument('-b','--bits', action='store', dest='bits', help='-b 32 (Number of hash bits to find collision)', required=True)
    parser.add_argument('-i','--input', action='store', dest='inputFile', help='-i input.txt The input file with hashes', required=True)
    parser.add_argument('-hg','--hashgroup', action='store_true', dest='hashGroup', help='-h The input file has hashes per line', required=False)
    parser.add_argument('-t','--text', action='store_true', dest='text', help='-t The input file has text inside', required=False)
    parser.add_argument('-f','--first', action='store_true', dest='first', help='-f Collision with the first one hash', required=False)
    args = parser.parse_args()

    shacol = Shacol(args.sha256, args.bits, args.inputFile, args.hashGroup, args.text, args.first) #Instance of the class Shacol
    shacol.getinfo()
    print("Do you want to proceed?")
    raw_input('\nPress Enter to continue...')

    for hashes in shacol.shaList:
        shacol.findCollisionFast(hashes)

    #shacol.findCollisionSetArray()
    #shacol.findCollisionSets()

if __name__ == "__main__":
    main()

#There will be difference and dependence between threads in the index hashPart[0]...
#myData = threading.local()