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
    def findCollisionSet(self, hashPart=None):
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

            hashPartLength = len(hashPart)
            newHashPart = hashPart

            count = 0

            startTime = time.time()
            while newHashPart not in (hashPartSet or hashPartSet2 or hashPartSet3 or hashPartSet4 or hashPartSet5 or hashPartSet6 or hashPartSet7 or hashPartSet8 or hashPartSet9 or hashPartSet10):
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
                elif count < 1000000000:
                    hashPartSet10.add(newHashPart)
                else:
                    break;

                count += 1
                if count % 1000000 == 0 : print count
                if count == 85000000 : print 'First set capacity reached!'
                if count == 170000000 : print 'Second set capacity reached!'
                if count == 255000000 : print 'Third set capacity reached!'
                if count == 340000000 : print 'Fourth set capacity reached!'
                if count == 425000000 : print 'Fifth set capacity reached! You are going to the hell bro!'
                if count == 430000000 : print 'You are lucky man!'
                if count == 500000000 : print 'It is not real! I am kidding you all the time... '
                if count == 800000000 : print 'Take it easy like Mr. Easy... '
                if count == 850000000 : print 'Real limit of the algorithm reached!'
                if count == 1000000000 : print 'Process was stopped!'

                #print count,' : ',newHashPart
                newHash = hashlib.sha256(newHashPart).hexdigest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
            #In case of threding is needed the solution for number of position every thread!!!
            totalTime = round(time.time() - startTime, 12)
            print('\nSET - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            #print 'GetSizeOf:', sys.getsizeof(hashPartSet)
            print 'Count of the cycles:',count
            #print 'Count of the hashPartSet',len(hashPartSet)
            #print 'Count of the hashPartSet2',len(hashPartSet2)
            #print 'Count of the hashPartSet3',len(hashPartSet3)
            #print 'Count of the hashPartSet4',len(hashPartSet4)
            #print 'Count of the hashPartSet5',len(hashPartSet5)
            print 'Collision hash:', newHashPart

            #hashPartList = list(hashPartSet)
            #print 'Index of collision part:', hashPartList.index(newHashPart)
            #.clear()
            return newHashPart
        except Exception,e:
            print str(e)

    def findCollisionList(self, hashPart=None):
        """
        Function to be thread by individually calling - looking for a collision hashPart
        """

        try:
            hashPartList = [] #List
            hashPartLength = len(hashPart)
            newHashPart = hashPart
            startTime = time.time()
            while newHashPart not in hashPartList:
                hashPartList.append(newHashPart)
                #print count,' : ',newHashPart
                #count += 1
                newHash = hashlib.sha256(newHashPart).hexdigest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
                #In case of threding is needed the solution for number of position every thread!!!
            totalTime = round(time.time() - startTime, 12)
            print('\nLIST - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            print 'GetSizeOf:', sys.getsizeof(hashPartList)
            print 'Count of the cycles:', len(hashPartList)
            print 'Collision hash:', newHashPart
            #print 'Index of collision part:', hashPartList.index(newHashPart)
            #.clear()
            return newHashPart
        except Exception,e:
            print str(e)


    def findCollisionDeque(self, hashPart=None):
        """
        Function to be thread by individually calling - looking for a collision hashPart
        """

        try:
            hashPartDeque = deque()
            hashPartLength = len(hashPart)
            newHashPart = hashPart

            startTime = time.time()
            while newHashPart not in hashPartDeque:
                hashPartDeque.append(newHashPart)
                #print count,' : ',newHashPart
                #count += 1
                newHash = hashlib.sha256(newHashPart).hexdigest()
                newHashPart = newHash[0:hashPartLength] #Special ID as input parameter for threading
                #In case of threding is needed the solution for number of position every thread!!!
            totalTime = round(time.time() - startTime, 12)
            print('\nDEQUE - Collision found process succeeded!\n')
            print("Collision found after %s seconds" % (totalTime))
            print 'GetSizeOf:', sys.getsizeof(hashPartDeque)
            print 'Count of the cycles:', hashPartDeque.count(newHashPart)
            print 'Collision hash:', newHashPart
            #hashPartList = list(hashPartDeque)
            #print 'Index of collision part:', hashPartList.index(newHashPart)
            #.clear()
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

shacol.findCollisionSet(hashPart)
#shacol.findCollisionList(hashPart)
#shacol.findCollisionDeque(hashPart)
#shacol.findCollisionString(hashPart)
#shacol.findCollisionDigest(hashDigest)



#print shacol.findCollisionInt(hashPart)
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


"""
argsdict???
newJob = argsdict['new']
inFile = argsdict['input'] #shortcut for input directory
podle vseho se newJob vytvari vzdy pri argumentu "new"
taktez nacitani vsecho co se nachazi za argumentem se ulozi do dane promenne


readLine = linecache.getline(inFile, lineNum).rstrip()

while readLine is not "": #File reading
	lineNum = lineNum + 1 #Calculate number of lines in url file
	mainApps.append(readLine) #Include URLs from file into list
	diter = parseToDomain(readLine)
	if isURL(readLine):
		jobTrack[diter] = "Not Tested"
	else:
		jobTrack[diter] = "Invalid"
		print readLine + " is invalid"
	readLine = linecache.getline(inFile, lineNum).rstrip()

totalLines = lineNum - 1
print "\nThere is/are %d hashes in the file." % (totalLines)

raw_input("\nPress Enter to start...")
#startTime = time.time()

#Queuing and threading
q = Queue.LifoQueue()
#put items to queue
for key in jobTrack:
	if jobTrack[key] != "Invalid":
		q.put(str(key))
	else:
		print str(key) + " is not added to queue as its invalid"

for i in range(100):
	t1 = threading.Thread(target=runScan,args=(q,))
	t1.daemon = True
	t1.start() # Start the thread

q.join()

print "\nFinally"
print jobTrack

#nutno zajistit aby po dokonceni alespon jednoho vlakna  doslo k preruseni vsech ostatnich vlaken

with open(outFilename, 'w') as outFile:
    while True:
        chunk = inFile.read(chunksize)
        if len(chunk) == 0:
            break
        outFile.write(decryptor.decrypt(chunk))

totalTime = round(time.time() - startTime, 6)
print("Collision found after %s seconds" % (totalTime))
#vypis koliznich hashu

#using option parser
"""
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
