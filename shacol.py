#!/usr/bin/env python
import os
import time
#import Queue
import hashlib
import argparse
#import threading
#import linecache
from sets import Set
from StringIO import StringIO
#import re, sys, getopt

#Input parameters
parser = argparse.ArgumentParser(usage='$prog [options] -sha2 -b 32 -i hash.txt -h',description='SHA collision finder', add_help=True, epilog='SHA collision finder. Made by Jan Stangler, Ondrej Gajdusek, Sarka Chwastova, VUT FEKT, ICT1 project, 2017')
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
        else (args.hash):
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
print '\nHash to be break down:', hashPart

raw_input('\nPress Enter to continue...')

class Shacol:
    def findCollision(self, hashPart=None):
        """
        Function to be thread by individually calling - looking for a collision hashPart
        """

        hashPartSet = Set([])
        hashPartLength = len(hashPart)
        newHashPart = hashPart

        startTime = time.time()
        while newHashPart not in hashPartSet:
            hashPartSet.add(newHashPart)
            newHash = hashlib.sha256(newHashPart).hexdigest()
            newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
            #In case of threding is needed the solution for number of position every thread!!!
        totalTime = round(time.time() - startTime, 12)
        print('\nCollision found process succeeded!\n')
        print("Collision found after %s seconds" % (totalTime))
        print 'Count of the cycles:', len(hashPartSet)
        print 'Collision hash:', newHashPart
        hashPartList = list(hashPartSet)
        print 'Index of collision part:', hashPartList.index(newHashPart)

        #.clear()
        return newHashPart

    def findCollisionFirst(self, hashPart=None):
        """
        Function to be thread by individually calling - looking for a collision with the first hashPart
        """

        hashPartLength = len(hashPart)
        newHash = hashlib.sha256(hashPart).hexdigest()
        newHashPart = newHash[0:hashPartLength]
        count = 0

        startTime = time.time()
        while newHashPart != hashPart:
            newHash = hashlib.sha256(newHashPart).hexdigest()
            newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
            count += 1
            #In case of threding is needed the solution for number of position every thread!!!
        totalTime = round(time.time() - startTime, 12)
        print('\nCollision found process succeeded!\n')
        print("Collision found after %s seconds" % (totalTime))
        print 'Collision hash:', newHashPart
        print 'Couint of cycles:', count

        #.clear()
        return newHashPart

shacol = Shacol() #Instance of the class Shacol

if (args.first):
    shacol.findCollisionFirst(hashPart)
else:
    shacol.findCollision(hashPart)
#There will be difference and dependence between threads in the index hashPart[0]...

#myData = threading.local()

#Function monitoring the status of threads? Simple animation? Finally threading


"""
shacol.findCollision('4c07a78baec4') #48 bit
shacol.findCollision('4c07a78baec4b63') #60 bit
shacol.findCollision('4c07a78baec4b6309ab6') #80 bit
shacol.findCollision('4c07a78baec4b6309ab60f2a1') #100 bit
"""
#main function???
