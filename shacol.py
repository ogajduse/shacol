# !/usr/bin/env python

import argparse
import binascii
import hashlib
import random
import sys
import timeit

import cuckoofilter
import psutil
import pybloof
import redis


class Shacol(object):
    def __init__(self, bits, inputFile, hashGroup=False, text=False, first=False):
        """
        The constructor function that provides all unnecessary inputs.

        :param bits: bit length to investigate
        :param inputFile: directory or input string
        :param hashGroup: true/false value defines input file with hashes per lines
        :param text: true/false value defines input in string format
        :param first: true/false value decribes the use of first hash collision function

        """

        self.bits = int(bits)
        self.inputFile = inputFile
        self.hashGroup = hashGroup
        self.text = text
        self.first = first

        self.bestTime = sys.maxsize
        self.hashPartLength = int(int(self.bits) / 4)
        self.shaList = []
        self.hashPart = str()

        if '.txt' in str(inputFile):
            with open(self.inputFile, 'r', encoding='utf-8') as dataFromFile:
                if self.hashGroup:
                    if self.text:
                        for textInFile in dataFromFile:
                            self.shaList.append(
                                hashlib.sha256(textInFile.encode('utf-8').hexdigest()[0:self.hashPartLength]))
                    else:
                        for hashInFile in dataFromFile:
                            self.shaList.append(hashInFile[0:self.hashPartLength])
                else:
                    if self.text:
                        self.hashPart = hashlib.sha256(dataFromFile.read().encode('utf-8')).hexdigest()[
                                        0:self.hashPartLength]
                    else:
                        self.hashPart = dataFromFile.readline()[0:self.hashPartLength]
            dataFromFile.close()
        elif inputFile:
            self.hashPart = hashlib.sha256(inputFile.encode('utf-8')).hexdigest()[
                            0:self.hashPartLength]


    def getInfo(self):
        """
        Print the basic information about process at the beggining of activity.

        """

        printHashes = str()
        for i in self.shaList:
            printHashes += i + '\t'
        # print absolute path to input file
        print('\nYou are trying to find a collision with %s hash for %db with SHA-2.\n' %
              ('first' if self.first else 'arbitary', self.bits) +
              'Using %s as input file with %s.' %
              (self.inputFile,
               'one hash inside' if not self.hashGroup else 'with one hash per line inside.') +
              '\nInput %s %s' % ('hash is  '
                                 if not self.hashGroup else 'hashes are ',
                                 self.hashPart if not self.hashGroup else printHashes))


    def changeBitLength(self, newBitLength):
        """
        The function that cuts full length hash into chosen length.

        :param newBitLength: chosen bit length

        """

        self.bits = newBitLength
        self.hashPartLength = int(int(self.bits) / 4)


    def findCollisionStr(self, hashPart=None):
        """
        Function with the best performance - storing hashes in SET by STRING

        :param hashPart: the input hash loaded from a file
        :return: inputString, inputHash, totalTime, indexOfFirst, indexOfLast,
        newHashPart, indexOfLast-indexOfFirst, firstTemp, lastTemp, totalMemory

        """

        try:
            # Checking the constructor parameters that can be used
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            if '.txt' not in str(self.inputFile):
                inputString = self.inputFile
            else:
                inputString = ''

            status = 1
            strHashSet = {str()}  # length start with 1
            newHashPart = hashPart
            lastTemp = ''

            start = timeit.default_timer()

            while newHashPart not in strHashSet:
                strHashSet.add(newHashPart)
                status += 1
                if status == 10000000: # Prints a status of process in sequence 10 000 000 hashes by default
                    print('\n' * 3)
                    print('SET length:', len(strHashSet))
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')
                    status = 0
                lastTemp = newHashPart # Saves temporarily the parental hash
                newHash = hashlib.sha256(newHashPart.encode('utf-8')).hexdigest() # Calculate a new hash from last hashed part
                newHashPart = newHash[0:hashPartLength] # Cuts a new hash to specific length

            stop = timeit.default_timer()

            totalTime = round(stop - start, 12) # Calculates summary of time consumption
            totalMemory = round(sys.getsizeof(strHashSet) / 1024 / 1024, 3) # Calculates the size of used memory

            # Initialization of new values to find first index of collision
            indexOfFirst = 0
            firstTemp = ''
            indexOfLast = len(strHashSet) - 1
            lastCollision = newHashPart
            newHashPart = hashPart

            print('\n\n##### findCollisionStr - Collision found process succeeded! #####\n')
            if inputString:
                print('Input string:', inputString)
            print('Input hashPart:', hashPart)
            print("Collision found after %s seconds" % (totalTime))
            print('Collision hash:', lastCollision)

            while newHashPart != lastCollision: # Cycle for finding the index of first collision
                indexOfFirst += 1
                firstTemp = newHashPart
                newHash = hashlib.sha256(newHashPart.encode('utf-8')).hexdigest()
                newHashPart = newHash[0:hashPartLength]

            print('Index of first collision:', indexOfFirst)
            print('Index of last collision:', indexOfLast)
            print('Cycles between collision hashes:', indexOfLast - indexOfFirst)
            print('Hash 1 before collision:', firstTemp)
            print('Hash 2 before collision:', lastTemp)
            print('\nSet string structure used', round(sys.getsizeof(strHashSet) / 1024 / 1024, 3), 'MB')
            del strHashSet

            return {"inputString": inputString, "inputHash": hashPart, "time": totalTime, "indexOfFirst": indexOfFirst,
                    "indexOfLast": indexOfLast, "collisionHash": newHashPart,
                    "cyclesBetCol": indexOfLast - indexOfFirst,
                    "firstTemp": firstTemp, "lastTemp": lastTemp, "dataStructConsum": totalMemory}

        except Exception as e:
            print(str(e))


    def findCollisionInt(self, hashPart=None):
        """
        The most effective versions of storing hash - INT in SET

        :param hashPart: the input hash loaded from a file
        :return: inputString, inputHash, totalTime, indexOfFirst, indexOfLast,
        newHashPart, indexOfLast-indexOfFirst, firstTemp, lastTemp, totalMemory

        """

        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            if '.txt' not in str(self.inputFile):
                inputString = self.inputFile
            else:
                inputString = ''

            status = 1
            lastTemp = ''
            intHashSet = {int()}
            newHashPart = int(binascii.hexlify(bytes(hashPart, 'utf-8')), 16)

            start = timeit.default_timer()

            while newHashPart not in intHashSet:
                intHashSet.add(newHashPart)
                status += 1
                if status == 10000000:
                    print('\n' * 3)
                    print('Set length:', len(intHashSet))
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')
                    status = 0
                strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                lastTemp = strHashPart.decode('utf-8')
                newHash = hashlib.sha256(strHashPart).hexdigest()
                newHash = newHash[0:hashPartLength]
                newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            totalMemory = round(sys.getsizeof(intHashSet) / 1024 / 1024, 3)
            indexOfFirst = 0
            firstTemp = ''
            indexOfLast = len(intHashSet) - 1
            lastCollision = newHash
            newHashPart = hashPart

            print('\n\n##### findCollisionInt - Collision found process succeeded! #####\n')
            if inputString:
                print('Input string:', inputString)
            print('Input hashPart:', hashPart)
            print("Collision found after %s seconds" % (totalTime))
            print('Collision hash:', lastCollision)

            while newHashPart != lastCollision:
                indexOfFirst += 1
                firstTemp = newHashPart
                newHash = hashlib.sha256(newHashPart.encode('utf-8')).hexdigest()
                newHashPart = newHash[0:hashPartLength]

            print('Index of first collision:', indexOfFirst)
            print('Index of last collision:', indexOfLast)
            print('Cycles between collision hashes:', indexOfLast - indexOfFirst)
            print('Hash 1 before collision:', firstTemp)
            print('Hash 2 before collision:', lastTemp)

            print('\nSet int structure used', round(sys.getsizeof(intHashSet) / 1024 / 1024, 3), 'MB')
            del intHashSet

            return {"inputString": inputString, "inputHash": hashPart, "time": totalTime, "indexOfFirst": indexOfFirst,
                    "indexOfLast": indexOfLast, "collisionHash": lastCollision,
                    "cyclesBetCol": indexOfLast - indexOfFirst,
                    "firstTemp": firstTemp, "lastTemp": lastTemp, "dataStructConsum": totalMemory}

        except Exception as e:
            print(str(e))

    def findBestHash(self, maxSet=100000000, memoryCheck=False):
        """
        Function provides the best possible input string with the least time consumption.
        Offers memory check in intervals.

        :param maxSet: the maximal count of set with stored hashes
        :param memoryCheck: check free memory in sequence

        """
        try:
            memOver = False
            hashPartLength = self.hashPartLength
            charStr = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/!@#$%&?'
            bestTime = sys.maxsize
            random.seed()

            while True:
                rndStr = ''
                intHashSet = {int()}
                charLen = random.randint(1, 64)
                for number in range(charLen):
                    rndStr += ''.join(random.sample(charStr, 1))
                print('\nGenerate new string input: ', rndStr, '\n')

                firstHash = hashlib.sha256(rndStr.encode('utf-8')).hexdigest()
                firstHashPart = firstHash[0:hashPartLength]
                newHashPart = int(binascii.hexlify(bytes(firstHashPart, 'utf-8')), 16)

                print('Finding collision started')
                start = timeit.default_timer()
                while newHashPart not in intHashSet:
                    if memoryCheck:
                        virtualMem = psutil.virtual_memory().available
                        if virtualMem < 134217728:
                            print('\n!!! Memory capacity reached !!! Set count:', len(intHashSet))
                            memOver = True
                            break
                    else:
                        if len(intHashSet) >= maxSet:
                            print('\n--- Stated limit reached --- Set count:', len(intHashSet))
                            memOver = True
                            break

                    intHashSet.add(newHashPart)
                    strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                    newHash = hashlib.sha256(strHashPart).hexdigest()
                    newHash = newHash[0:hashPartLength]
                    newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)

                stop = timeit.default_timer()
                totalTime = round(stop - start, 10)
                totalMemory = round(sys.getsizeof(intHashSet) / 1048576, 3)
                indexOfCollision = len(intHashSet)

                if not memOver:
                    print('\n##### Collision found process succeeded! #####')
                    print('Input string:', rndStr)
                    print('Input hash:', firstHash)
                    print('Input hash part:', firstHashPart)
                    print("Collision found after %s seconds" % (totalTime))
                    if (totalTime < bestTime): bestTime = totalTime
                    print('Index of collision:', indexOfCollision)
                    print('Collision hash:', newHash)
                    print('Set int structure used', totalMemory, 'MB')
                    print('\nThe best time yet:', bestTime)
                else:
                    memOver = False

                del intHashSet
                print('SET was emptied successfully')

        except Exception as e:
            print(str(e))


    def findCollisionFirst(self, hashPart=None):
        """
        Function to be thread by individually calling - looking for a collision with first hashPart

        :param hashPart: the input hash loaded from a file
        :return: inputString, inputHash, totalTime, indexOfFirst, indexOfLast,
        newHashPart, indexOfLast-indexOfFirst, firstTemp, lastTemp, totalMemory

        """

        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            if '.txt' not in str(self.inputFile):
                inputString = self.inputFile
            else:
                inputString = ''

            status = 0
            indexOfLast = 0
            lastTemp = ''

            newHashPart = hashlib.sha256(hashPart.encode('utf-8')).hexdigest()[0:hashPartLength]

            start = timeit.default_timer()
            while hashPart != newHashPart:
                lastTemp = newHashPart
                newHashPart = hashlib.sha256(newHashPart.encode('utf-8')).hexdigest()[0:hashPartLength]
                indexOfLast += 1
                status += 1
                if status == 100000000:
                    print(indexOfLast)
                    status = 0

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            print('\n##### findCollisionFirst - Collision found process succeeded! #####')
            print("Collision found after %s seconds" % (totalTime))
            print('Index of last collision:', indexOfLast)
            print('Collision hash:', newHashPart)
            print('Hash before collision:', lastTemp)

            return {"inputString": inputString, "inputHash": hashPart, "time": totalTime, "indexOfFirst": 0,
                    "indexOfLast": indexOfLast, "collisionHash": newHashPart, "cyclesBetCol": 0,
                    "firstTemp": '', "lastTemp": lastTemp, "dataStructConsum": 0}

        except Exception as e:
            print(str(e))


    def findCollisionWithDBSet(self, hashPart=None):
        """
        Function is looking for a collision with hashPart

        :param hashPart: the input hash loaded from a file
        :return: inputString, inputHash, totalTime, indexOfFirst, indexOfLast,
        newHashPart, indexOfLast-indexOfFirst, firstTemp, lastTemp, totalMemory

        """

        try:
            pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
            r = redis.Redis(connection_pool=pool)
            r.flushdb()

            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            if '.txt' not in str(self.inputFile):
                inputString = self.inputFile
            else:
                inputString = ''

            status = 0
            newHashPart = hashPart

            start = timeit.default_timer()
            while not r.sismember('hset', newHashPart):
                r.sadd('hset', newHashPart)
                status += 1
                if status == 10000000:
                    status = 0
                    print('\n' * 100)
                    print('Count of the cycles:', r.scard('hset'))
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')
                lastTemp = newHashPart
                newHashPart = hashlib.sha256(newHashPart.encode('utf-8')).hexdigest()[0:hashPartLength]

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            indexOfFirst = 0
            firstTemp = ''
            indexOfLast = r.scard('hset')
            lastCollision = newHashPart
            newHashPart = hashPart

            print('\n##### DBSet method - Collision found process succeeded! #####')
            print("Collision found after %s seconds" % (totalTime))
            print('Count of the cycles:', r.scard('hset'))
            print('Collision hash:', lastCollision)

            while newHashPart != lastCollision:
                indexOfFirst += 1
                firstTemp = newHashPart
                newHash = hashlib.sha256(newHashPart.encode('utf-8')).hexdigest()
                newHashPart = newHash[0:hashPartLength]

            print('Index of first collision:', indexOfFirst)
            print('Index of last collision:', indexOfLast)
            print('Cycles between collision hashes:', indexOfLast - indexOfFirst)
            print('Hash 1 before collision:', firstTemp)
            print('Hash 2 before collision:', lastTemp)

            return {"inputString": inputString, "inputHash": hashPart, "time": totalTime, "indexOfFirst": indexOfFirst,
                    "indexOfLast": indexOfLast, "collisionHash": lastCollision,
                    "cyclesBetCol": indexOfLast - indexOfFirst,
                    "firstTemp": firstTemp, "lastTemp": lastTemp, "dataStructConsum": 0}

        except Exception as e:
            print(str(e))


    def findCollisionBloom(self, hashPart=None, filterCapacity=1000000000):
        """
        The test method using performance Bloom filter.

        :param hashPart: the input hash loaded from a file
        :filterCapacity: the capacity of Bloom filter
        :return: inputString, inputHash, totalTime, indexOfFirst, indexOfLast,
        newHashPart, indexOfLast-indexOfFirst, firstTemp, lastTemp, totalMemory

        """
        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            if '.txt' not in str(self.inputFile):
                inputString = self.inputFile
            else:
                inputString = ''

            status = 0
            indexOfFirst = 0
            firstTemp = ''
            indexOfLast = 0
            lastTemp = ''

            newHashPart = bytes(hashPart, 'utf-8')
            bloomFilter = pybloof.StringBloomFilter(size=filterCapacity, hashes=9)
            start = timeit.default_timer()

            while True:
                if newHashPart not in bloomFilter:
                    bloomFilter.add(newHashPart)
                    indexOfLast += 1
                    status += 1
                    if status == 10000000:
                        print('\n' * 100)
                        print('Count of cycles:', indexOfLast)
                        print('Run time:', round((timeit.default_timer() - start), 3), 's')
                        status = 0
                    lastTemp = newHashPart.decode('utf-8')
                    newHash = hashlib.sha256(newHashPart).hexdigest()
                    newHash = newHash[0:hashPartLength]
                    newHashPart = bytes(newHash, 'utf-8')
                else:
                    if indexOfLast >= filterCapacity:
                        print("!!! filterCapacity reached !!!")
                        break
                    print("### Potencional collision successfully passed! ###")
                    print("Suspicious hash: ", newHash)
                    print('Count of cycles:', indexOfLast)
                    print('Time:', round((timeit.default_timer() - start), 3), 's')

                    indexOfFirst = 0
                    collisionHash = newHashPart
                    newHashPart = bytes(hashPart, 'utf-8')
                    while newHashPart != collisionHash:
                        indexOfFirst += 1
                        status += 1
                        if status == 10000000:
                            print('\n' * 100)
                            print('Suspicious hash found! :) Searching for collision index...')
                            print('Count of cycles:', indexOfFirst)
                            print('Run time:', round((timeit.default_timer() - start), 3), 's')
                            status = 0
                        firstTemp = newHashPart.decode('utf-8')
                        newHash = hashlib.sha256(newHashPart).hexdigest()
                        newHash = newHash[0:hashPartLength]
                        newHashPart = bytes(newHash, 'utf-8')

                    if indexOfFirst != indexOfLast:
                        break
                    else:
                        print('False positive hash detected :(')
                        indexOfLast += 1
                        status += 1
                        bloomFilter.add(newHashPart)
                        newHash = hashlib.sha256(newHashPart).hexdigest()
                        newHash = newHash[0:hashPartLength]
                        newHashPart = bytes(newHash, 'utf-8')

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            totalMemory = round(sys.getsizeof(bloomFilter) / 1048576, 3)

            if indexOfFirst != indexOfLast and filterCapacity > indexOfLast:
                print('\n\n##### findCollisionBloom - Collision found process succeeded! \o/ #####\n')
                print("Collision found after %s seconds" % (totalTime), '\n')
                if inputString:
                    print('Input string:', inputString)
                print('Input hashPart:', hashPart)
                print('\nCollision hash:', newHash)
                print('Hash 1 leading to collision:', firstTemp)
                print('Hash 2 leading to collision:', lastTemp)
                print('\nIndex of first collision:', indexOfFirst)
                print('Index of last collision:', indexOfLast)
                print('Cycles between collision hashes:', indexOfLast - indexOfFirst)
                print('\nBloom filter used', round(sys.getsizeof(bloomFilter) / 1024 / 1024, 3), 'MB')

                return {"inputString": inputString, "inputHash": hashPart, "time": totalTime,
                        "indexOfFirst": indexOfFirst,
                        "indexOfLast": indexOfLast, "collisionHash": newHashPart,
                        "cyclesBetCol": indexOfLast - indexOfFirst,
                        "firstTemp": firstTemp, "lastTemp": lastTemp, "dataStructConsum": totalMemory}
            else:
                print('\n##### findCollisionBloom - Collision found process failed! /o\ #####')

        except Exception as e:
            print(str(e))


    def findCollisionBloomStore(self, hashPart=None, filterCapacity=1000000000, storeCount=100000, hashCount=12):
        """
        The test method using performance Bloom filter.

        :param hashPart: the input hash loaded from a file
        :param filterCapacity: the capacity of Bloom filter
        :param storeCount: the count of set with stored suspicious hashes
        :param hashCount: number of hash cycles
        :return: inputString, inputHash, totalTime, indexOfFirst, indexOfLast,
        newHashPart, indexOfLast-indexOfFirst, firstTemp, lastTemp, totalMemory

        """
        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            if '.txt' not in str(self.inputFile):
                inputString = self.inputFile
            else:
                inputString = ''

            status = 0
            indexOfFirst = 0
            firstTemp = ''
            indexOfLast = 0
            lastTemp = ''
            byteIntHashDict = {bytes(): int()}  # structure using bytes (hash) + int (index)
            storeLimit = False

            newHashPart = bytes(hashPart, 'utf-8')
            bloomFilter = pybloof.StringBloomFilter(size=filterCapacity, hashes=hashCount)
            start = timeit.default_timer()

            while True:
                if newHashPart not in bloomFilter:
                    bloomFilter.add(newHashPart)
                    indexOfLast += 1
                    status += 1
                    if status == 10000000:
                        print('\n' * 100)
                        print('Count of cycles:', indexOfLast)
                        print('Run time:', round((timeit.default_timer() - start), 3), 's')
                        status = 0
                    lastTemp = newHashPart.decode('utf-8')
                    newHash = hashlib.sha256(newHashPart).hexdigest()
                    newHash = newHash[0:hashPartLength]
                    newHashPart = bytes(newHash, 'utf-8')
                else:
                    if indexOfLast >= filterCapacity:
                        print("!!! filterCapacity reached !!!")
                        storeLimit = True
                    print("### Potencional collision successfully stored! ###")
                    print("Suspicious hash: ", newHash)
                    print('Count of cycles:', indexOfLast)
                    print('Time:', round((timeit.default_timer() - start), 3), 's')

                    if storeLimit:
                        newHashPart = bytes(hashPart, 'utf-8')
                        while not byteIntHashDict.get(newHashPart):
                            indexOfFirst += 1
                            status += 1
                            if status == 10000000:
                                print('\n' * 100)
                                print('Checking suspicious hashes! :) Searching for collision index...')
                                print('Reached count:', indexOfLast)
                                print('Current count:', indexOfFirst)
                                print('Run time:', round((timeit.default_timer() - start), 3), 's')
                                status = 0
                            firstTemp = newHashPart.decode('utf-8')
                            newHash = hashlib.sha256(newHashPart).hexdigest()
                            newHash = newHash[0:hashPartLength]
                            newHashPart = bytes(newHash, 'utf-8')

                        indexOfLast = byteIntHashDict.get(newHashPart)
                        if indexOfFirst != indexOfLast:
                            break
                        else:
                            print('Just false positives have been detected :(')
                            indexOfFirst == indexOfLast
                            break
                    else:
                        byteIntHashDict[newHashPart] = indexOfLast
                        if len(byteIntHashDict) >= storeCount:
                            storeLimit = True
                        bloomFilter.add(newHashPart)
                        indexOfLast += 1
                        status += 1
                        newHash = hashlib.sha256(newHashPart).hexdigest()
                        newHash = newHash[0:hashPartLength]
                        newHashPart = bytes(newHash, 'utf-8')

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            totalMemory = round(sys.getsizeof(bloomFilter) / 1048576, 3)

            if indexOfFirst != indexOfLast and filterCapacity > indexOfLast:
                print('\n\n##### findCollisionBloomStore - Collision found process succeeded! \o/ #####\n')
                print("Collision found after %s seconds" % (totalTime), '\n')
                if inputString:
                    print('Input string:', inputString)
                print('Input hashPart:', hashPart)
                print('\nCollision hash:', newHash)
                print('Hash 1 leading to collision:', firstTemp)
                print('Hash 2 leading to collision:', lastTemp)
                print('\nIndex of first collision:', indexOfFirst)
                print('Index of last collision:', indexOfLast)
                print('Cycles between collision hashes:', indexOfLast - indexOfFirst)
                print('\nBloom filter used', round(sys.getsizeof(bloomFilter) / 1024 / 1024, 3), 'MB')

                return {"inputString": inputString, "inputHash": hashPart, "time": totalTime,
                        "indexOfFirst": indexOfFirst,
                        "indexOfLast": indexOfLast, "collisionHash": newHashPart,
                        "cyclesBetCol": indexOfLast - indexOfFirst,
                        "firstTemp": firstTemp, "lastTemp": lastTemp, "dataStructConsum": totalMemory}
            else:
                print('\n##### findCollisionBloom - Collision found process failed! /o\ #####')

        except Exception as e:
            print(str(e))

    def findCollisionCuckoo(self, hashPart=None, filterCapacity=10000000):
        """
        Using Cuckoo filter, large

        :param hashPart: the input hash loaded from a file
        :param filterCapacity: the capacity of Bloom filter
        :return: inputString, inputHash, totalTime, indexOfFirst, indexOfLast,
        newHashPart, indexOfLast-indexOfFirst, firstTemp, lastTemp, totalMemory

        """
        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            if '.txt' not in str(self.inputFile):
                inputString = self.inputFile
            else:
                inputString = ''

            status = 0
            indexOfFirst = 0
            firstTemp = ''
            indexOfLast = 0
            lastTemp = ''

            newHashPart = bytes(hashPart, 'utf-8')
            cf = cuckoofilter.CuckooFilter(capacity=filterCapacity, fingerprint_size=1)
            start = timeit.default_timer()

            while True:
                if newHashPart not in cf:
                    cf.insert(newHashPart)
                    indexOfLast += 1
                    status += 1
                    if status == 10000000:
                        print('\n' * 100)
                        print('Count of cycles:', indexOfLast)
                        print('Run time:', round((timeit.default_timer() - start), 3), 's')
                        status = 0
                    lastTemp = newHashPart.decode('utf-8')
                    newHash = hashlib.sha256(newHashPart).hexdigest()
                    newHash = newHash[0:hashPartLength]
                    newHashPart = bytes(newHash, 'utf-8')
                else:
                    if indexOfLast >= filterCapacity:
                        print("!!! filterCapacity reached !!!")
                        break
                    print("### Potencional collision successfully passed! ###")
                    print("Suspicious hash: ", newHash)
                    print('Count of cycles:', indexOfLast)
                    print('Time:', round((timeit.default_timer() - start), 3), 's')

                    indexOfFirst = 0
                    collisionHash = newHashPart
                    newHashPart = bytes(hashPart, 'utf-8')
                    while newHashPart != collisionHash:
                        indexOfFirst += 1
                        status += 1
                        if status == 10000000:
                            print('\n' * 100)
                            print('Suspicious hash found! :) Searching for collision index...')
                            print('Count of cycles:', indexOfFirst)
                            print('Run time:', round((timeit.default_timer() - start), 3), 's')
                            status = 0
                        firstTemp = newHashPart.decode('utf-8')
                        newHash = hashlib.sha256(newHashPart).hexdigest()
                        newHash = newHash[0:hashPartLength]
                        newHashPart = bytes(newHash, 'utf-8')

                    if indexOfFirst != indexOfLast:
                        break
                    else:
                        print('False positive hash detected :(')
                        indexOfLast += 1
                        status += 1
                        cf.insert(newHashPart)
                        newHash = hashlib.sha256(newHashPart).hexdigest()
                        newHash = newHash[0:hashPartLength]
                        newHashPart = bytes(newHash, 'utf-8')

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            totalMemory = round(sys.getsizeof(cf) / 1048576, 3)

            if indexOfFirst != indexOfLast and filterCapacity > indexOfLast:
                print('\n\n##### findCollisionCuckoo - Collision found process succeeded! \o/ #####\n')
                print("Collision found after %s seconds" % (totalTime), '\n')
                if inputString:
                    print('Input string:', inputString)
                print('Input hashPart:', hashPart)
                print('\nCollision hash:', newHash)
                print('Hash 1 leading to collision:', firstTemp)
                print('Hash 2 leading to collision:', lastTemp)
                print('\nIndex of first collision:', indexOfFirst)
                print('Index of last collision:', indexOfLast)
                print('Cycles between collision hashes:', indexOfLast - indexOfFirst)
                print('\nCuckoo filter used', round(sys.getsizeof(cf) / 1024 / 1024, 3), 'MB')

                return {"inputString": inputString, "inputHash": hashPart, "time": totalTime,
                        "indexOfFirst": indexOfFirst,
                        "indexOfLast": indexOfLast, "collisionHash": newHashPart,
                        "cyclesBetCol": indexOfLast - indexOfFirst,
                        "firstTemp": firstTemp, "lastTemp": lastTemp, "dataStructConsum": totalMemory}
            else:
                print('\n##### findCollisionCuckoo - Collision found process failed! /o\ #####')

        except Exception as e:
            print(str(e))


def main():
    # Optional arguments

    parser = argparse.ArgumentParser(usage='$prog [options] -b 32 -i hash.txt',
                                     description='SHA2 collision finder', add_help=True,
                                     epilog='SHA2 collision finder. Written by Jan Stangler, Ondrej\
                                      Gajdusek, Sarka Chwastkova, VUT FEEC, ICT1 project, 2017')
    parser.add_argument('-b', '--bits', action='store', dest='bits',
                        help='-b 32 (Number of hash bits to find collision)', required=True)
    parser.add_argument('-i', '--input', action='store', dest='inputFile',
                        help='-i input.txt The input file with hashes', required=False)
    parser.add_argument('-hg', '--hashgroup', action='store_true', dest='hashGroup',
                        help='-h The input file has hashes per line', required=False)
    parser.add_argument('-t', '--text', action='store_true', dest='text',
                        help='-t The input file of random text', required=False)
    parser.add_argument('-f', '--first', action='store_true', dest='first',
                        help='-f Collision with the first one hash', required=False)
    parser.add_argument('--bloom', action='store_true', dest='bloom',
                        help='--bloom Bloom filter is used.', required=False)
    parser.add_argument('--cuckoo', action='store_true', dest='cuckoo',
                        help='--cuckoo Cuckoo filter is used.', required=False)
    parser.add_argument('-m', '--memory', action='store_true', dest='memory',
                        help='-m Memory check during a process.', required=False)
    parser.add_argument('-c', '--capacity', action='store', dest='capacity',
                        help='-c Set a length of default storage - SET.', required=False)
    parser.add_argument('-r', '--redis', action='store_true', dest='redis',
                        help='-r Store hashes in redis database.', required=False)
    args = parser.parse_args()

    # Instance of the class Shacol
    shacol = Shacol(args.bits, args.inputFile, args.hashGroup, args.text, args.first)
    shacol.getInfo()

    print("Do you want to proceed?")
    input('\nPress Enter to continue...')

    # Inteligent tree of function calling
    if args.inputFile:
        if args.hashGroup:
            for hashes in shacol.shaList:
                if args.first:
                    shacol.findCollisionFirst(hashes)
                else:
                    shacol.findCollisionInt(hashes)
        else:
            if args.first:
                shacol.findCollisionFirst()
            else:
                if args.memory:
                    if args.redis:
                        shacol.findCollisionWithDBSet(memoryCheck=True)
                else:
                    if args.cuckoo:
                        if args.capacity:
                            shacol.findCollisionCuckoo(filterCapacity=int(args.capacity))
                        else:
                            shacol.findCollisionCuckoo()
                    elif args.bloom:
                        if args.capacity:
                            shacol.findCollisionBloom(filterCapacity=int(args.capacity))
                        else:
                            shacol.findCollisionBloom()
                    elif args.redis:
                        shacol.findCollisionWithDBSet()
                    else: # Default action without any additional arguments except input file (python3 shacol.py -b 32 -h hash.txt)
                        # shacol.findCollisionStr()
                        # shacol.findCollisionInt()
                        shacol.findCollisionBloomStore(filterCapacity=1000000000, storeCount=100000, hashCount=12)
    else:
        if args.bloom:
            if args.memory:
                if args.capacity:
                    shacol.findBestHashBloom(maxSet=int(args.capacity), memoryCheck=True)
                else:
                    shacol.findBestHashBloom(memoryCheck=True)
            else:
                if args.capacity:
                    shacol.findBestHashBloom(maxSet=int(args.capacity))
                else:
                    shacol.findBestHashBloom()
        else:
            if args.memory:
                if args.capacity:
                    shacol.findBestHash(maxSet=int(args.capacity), memoryCheck=True)
                else:
                    shacol.findBestHash(memoryCheck=True)
            else:
                if args.capacity:
                    shacol.findBestHash(maxSet=int(args.capacity))
                else: # Default action without any additional arguments (python3 shacol.py -b 32)
                    shacol.findBestHash()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted... Terminating')
        sys.exit()
