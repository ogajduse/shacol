# !/usr/bin/env python

import sys
import redis
import random
import timeit
import psutil
import hashlib
import argparse
import binascii
import pybloomfilter


class Shacol(object):
    def __init__(self, bits, inputFile, hashGroup=False, text=False, first=False, bloom=False, memory=False):
        self.bits = int(bits)
        self.inputFile = inputFile
        self.hashGroup = hashGroup
        self.text = text
        self.first = first
        self.bloom = bloom
        self.memory = memory

        self.bestTime = sys.maxsize
        self.hashPartLength = int(int(self.bits) / 4)
        self.shaList = []
        self.hashPart = str()

        if inputFile:
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

    def getInfo(self):
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
        self.bits = newBitLength
        self.hashPartLength = int(int(self.bits) / 4)


    def findCollisionStr(self, hashPart=None):
        """
        Function with the best performance - storing hashes in SET by STRING

        :param hashPart: the input hash loaded from a file
        """
        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            status = 1
            strHashSet = {str()}
            newHashPart = hashPart

            start = timeit.default_timer()

            while newHashPart not in strHashSet:
                strHashSet.add(newHashPart)
                status += 1
                if status == 10000000:
                    print('\n' * 100)
                    print('SET length:', len(strHashSet))
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')
                    status = 0
                newHash = hashlib.sha256(newHashPart.encode('utf-8')).hexdigest()
                newHashPart = newHash[0:hashPartLength]

            stop = timeit.default_timer()

            totalTime = round(stop - start, 12)
            totalMemory = round(sys.getsizeof(strHashSet) / 1024 / 1024, 3)
            cycles = len(strHashSet) + 1

            print('\n##### findCollisionStr - Collision found process succeeded! #####')
            print('\nInput hashPart:', hashPart)
            print("Collision found after %s seconds" % (totalTime))
            print('Count of the cycles:', cycles)
            print('Collision hash:', newHashPart)
            index = 0
            for strHash in strHashSet:
                index += 1
                if strHash == newHashPart:
                    print('Index of collision hash:', index)
                    break
            print('Cycles between collision hashes:', cycles-index)
            print('\nSet string structure used', round(sys.getsizeof(strHashSet) / 1024 / 1024, 3), 'MB')
            del strHashSet

            #time in sec, dataStructConsum in MB
            return {"inputHash": hashPart, "time": totalTime, "cycles": cycles, "collisionHash": newHashPart,
                    "indexOfCollision": index, "cyclesBetCol": cycles-index,
                    "dataStructConsum": totalMemory}

        except Exception as e:
            print(str(e))

    def findCollisionInt(self, hashPart=None):
        """
        The most effective versions of storing hash - INT in SET

        :param hashPart: the input hash loaded from a file
        """
        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            status = 1
            intHashSet = {int()}
            newHashPart = int(binascii.hexlify(bytes(hashPart, 'utf-8')), 16)

            start = timeit.default_timer()

            while newHashPart not in intHashSet:
                intHashSet.add(newHashPart)
                status += 1
                if status == 10000000:
                    print('\n' * 100)
                    print('Set length:', len(intHashSet))
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')
                    status = 0
                strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                newHash = hashlib.sha256(strHashPart).hexdigest()
                newHash = newHash[0:hashPartLength]
                newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            totalMemory = round(sys.getsizeof(intHashSet) / 1024 / 1024, 3)
            cycles = len(intHashSet) + 1

            print('\n##### findCollisionInt - Collision found process succeeded! #####')
            print('\nInput hashPart:', hashPart)
            print("Collision found after %s seconds" % (totalTime))
            print('Count of the cycles:', len(intHashSet) + 1)
            print('Collision hash:', newHash)
            index = 0
            for intHash in intHashSet:
                index += 1
                if intHash == newHashPart:
                    print('Index of collision hash:', index)
                    break
            print('Cycles between collision hashes:', cycles-index)
            print('\nSet int structure used', round(sys.getsizeof(intHashSet) / 1024 / 1024, 3), 'MB')
            del intHashSet

            #totalMemory in MB
            return {"inputHash": hashPart, "time": totalTime, "cycles": cycles, "collisionHash": newHash,
                    "indexOfCollision": index, "cyclesBetCol": cycles-index,
                    "dataStructConsum": totalMemory}

        except Exception as e:
            print(str(e))

    def findBestHash(self, maxSet=100000000, memoryCheck=False):
        """
        Function provides the best possible input string with the least time consumption.
        Offers memory check in intervals.
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
                cycles = len(intHashSet) + 1

                if not memOver:
                    print('\n##### Collision found process succeeded! #####')
                    print('Input string:', rndStr)
                    print('Input hash:', firstHash)
                    print('Input hash part:', firstHashPart)
                    print("Collision found after %s seconds" % (totalTime))
                    if (totalTime < bestTime): bestTime = totalTime
                    print('Count of the cycles:', cycles)
                    print('Collision hash:', newHash)
                    index = 0
                    for intHash in intHashSet:
                        index += 1
                        if intHash == newHashPart:
                            print('Index of collision hash:', index)
                            break
                    print('Cycles between collision hashes:', cycles-index)
                    print('Set int structure used', totalMemory, 'MB')
                    print('\nThe best time yet:', bestTime)
                else:
                    memOver = False

                del intHashSet
                print('SET was emptied successfully')

        except Exception as e:
            print(str(e))

    def findBestHashBloom(self, maxSet=100000000, memoryCheck=False):
        """
        Function provides the best possible input string.
        Offers memory check in intervals.

        Using bloom filter, after the success return collision value
        BloomFilter(countOfSet, probability, tmpFile)
        """
        try:
            globalStart = timeit.default_timer()
            memOver = False
            status = 1
            countOfCycles = 0
            bloomFound = True
            hashPartLength = self.hashPartLength
            charStr = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/!@#$%&?'
            bestTime = self.bestTime
            random.seed()

            while True:
                rndStr = ''
                intHashSet = {int()}
                bloomFilter = pybloomfilter.BloomFilter(maxSet, 0.1)
                charLen = random.randint(1, 64)
                for number in range(charLen):
                    rndStr += ''.join(random.sample(charStr, 1))
                print('\nGenerate new string input: ', rndStr, '\n')

                firstHash = hashlib.sha256(rndStr.encode('utf-8')).hexdigest()
                firstHashPart = firstHash[0:hashPartLength]
                newHashPart = int(binascii.hexlify(bytes(firstHashPart, 'utf-8')), 16)

                print('Finding collision started')
                start = timeit.default_timer()
                if not memoryCheck:
                    while True:
                        if newHashPart.to_bytes((newHashPart.bit_length() + 7) // 8, 'big') not in bloomFilter:
                            status += 1
                            if status == 10000000:
                                status = 0
                                print('\n' * 100)
                                print('Set length:', len(intHashSet))
                                print("Count of tested randomness:", countOfCycles)
                                print('Run time:', round((timeit.default_timer() - globalStart) / 60, 3), 'minutes')
                                if len(intHashSet) >= maxSet:
                                    print('\n--- Stated limit reached --- Set count:', len(intHashSet))
                                    memOver = True
                                    break

                            previousLength = len(intHashSet)
                            intHashSet.add(newHashPart)
                            if len(intHashSet) == previousLength:
                                bloomFound = False
                                break
                            bloomFilter.update(newHashPart.to_bytes((newHashPart.bit_length() + 7) // 8, 'big'))

                            strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                            newHash = hashlib.sha256(strHashPart).hexdigest()
                            newHash = newHash[0:hashPartLength]
                            newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)
                        else:
                            break

                else:
                    while True:
                        if newHashPart.to_bytes((newHashPart.bit_length() + 7) // 8, 'big') not in bloomFilter:
                            status += 1
                            if status == 10000000:
                                status = 0
                                print('\n' * 100)
                                print('Set length:', len(intHashSet))
                                print("Count of tested randomness:", countOfCycles)
                                print('Run time:', round((timeit.default_timer() - globalStart) / 60, 3), 'minutes')
                                virtualMem = psutil.virtual_memory().available
                                if virtualMem < 536870912:
                                    print('\n!!! Memory capacity reached !!! Set count:', len(intHashSet))
                                    memOver = True
                                    break

                            previousLength = len(intHashSet)
                            intHashSet.add(newHashPart)
                            if len(intHashSet) == previousLength:
                                bloomFound = False
                                break
                            bloomFilter.update(newHashPart.to_bytes((newHashPart.bit_length() + 7) // 8, 'big'))

                            strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                            newHash = hashlib.sha256(strHashPart).hexdigest()
                            newHash = newHash[0:hashPartLength]
                            newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)
                        else:
                            break

                stop = timeit.default_timer()
                countOfCycles += 1

                if not memOver:
                    totalTime = round(stop - start, 10)
                    totalMemory = round(sys.getsizeof(intHashSet) / 1048576, 3)
                    cycles = len(intHashSet) + 1

                    print('\n##### Collision found process succeeded! #####')
                    print('Input string:', rndStr)
                    print('Input hash:', firstHash)
                    print('Input hash part:', firstHashPart)
                    print("Collision found after %s seconds" % (totalTime))
                    if (totalTime < self.bestTime): self.bestTime = totalTime
                    print('Count of the cycles:', cycles)
                    print('Collision hash:', newHash)
                    index = 0
                    for intHash in intHashSet:
                        index += 1
                        if intHash == newHashPart:
                            print('Index of collision hash:', index)
                            break
                    print('Cycles between collision hashes:', cycles-index)
                    print('Set int structure used', totalMemory, 'MB')
                    print('Bloom filter succeeded?',bloomFound)
                    print('\nThe best time yet:', self.bestTime,'s')

                    return {"inputString": rndStr, "inputHash": firstHashPart, "time": totalTime, "cycles": cycles, "collisionHash": newHash,
                    "indexOfCollision:": index, "cyclesBetCol": cycles-index,
                    "dataStructConsum": (totalMemory, 'MB')}
                else:
                    memOver = False

                del intHashSet
                print('SET was emptied successfully')

        except Exception as e:
            print(str(e))


    def findExperimental(self, hashPart=None, memoryCheck=False, maxSet=10000000):
        """
        Experimental method based on generating bilion of hashes. After that
        the memory is exceeded and it will continue without saving previous hashes.
        """
        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            status = 1
            intHashSet = {int()}
            hashPartLength = len(hashPart)
            newHashPart = int(binascii.hexlify(bytes(hashPart, 'utf-8')), 16)
            print('\nExperimental method started...')

            start = timeit.default_timer()

            while True:
                status += 1
                previousLength = len(intHashSet)
                intHashSet.add(newHashPart)

                if len(intHashSet) == previousLength:
                    break
                if status == 1000000:
                    status = 0
                    print('\n' * 100)
                    print('Set length:', len(intHashSet))
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')

                    if memoryCheck:
                        virtualMem = psutil.virtual_memory().available
                        if virtualMem < 536870912:
                            print('\n!!! Memory capacity reached !!! Set count:', len(intHashSet))
                            break
                    else:
                        if len(intHashSet) >= maxSet:
                            print('\n--- Stated limit reached --- Set count:', len(intHashSet))
                            break

                strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                newHash = hashlib.sha256(strHashPart).hexdigest()
                newHash = newHash[0:hashPartLength]
                newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)
            print('Hashing without store started...')

            strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
            newHash = hashlib.sha256(strHashPart).hexdigest()
            newHash = newHash[0:hashPartLength]
            newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)

            counter = len(intHashSet)+1

            while newHashPart not in intHashSet:
                strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                newHash = hashlib.sha256(strHashPart).hexdigest()
                newHash = newHash[0:hashPartLength]
                newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)
                counter += 1
                status += 1
                if status == 100000000:
                    status = 0
                    print('\n' * 100)
                    print('Set length:', len(intHashSet))
                    print('Count of cycles:', len(intHashSet) + counter)
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            totalMemory = round(sys.getsizeof(intHashSet) / 1024 / 1024, 3)

            print('\n##### findExperimental - found process succeeded! #####')
            print('\nInput hashPart:', hashPart)
            print("Collision found after %s seconds" % (totalTime))
            print('Count of the cycles:', counter)
            print('Collision hash:', newHash)
            index = 0
            for intHash in intHashSet:
                index += 1
                if intHash == newHashPart:
                    print('Index of collision hash:', index)
                    break
            print('Cycles between collision hashes:', counter-index)
            print('\nSet int structure used', totalMemory, 'MB')
            del intHashSet

            return {"inputHash": hashPart, "time": totalTime, "cycles": counter, "collisionHash": newHash,
            "indexOfCollision:": index, "cyclesBetCol": counter-index,
            "dataStructConsum": (totalMemory, 'MB')}

        except Exception as e:
            print(str(e))

    def findCollisionFirst(self, hashPart=None):
        """
        Function to be thread by individually calling - looking for a collision with first hashPart
        """
        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            count = 0
            status = 0

            newHashPart = hashlib.sha256(hashPart.encode('utf-8')).hexdigest()[0:hashPartLength]

            start = timeit.default_timer()
            while hashPart != newHashPart:
                newHashPart = hashlib.sha256(newHashPart.encode('utf-8')).hexdigest()[0:hashPartLength]
                count += 1
                status += 1
                if status == 100000000:
                    print(count)
                    status = 0

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            print('\n##### findCollisionFirst - Collision found process succeeded! #####')
            print("Collision found after %s seconds" % (totalTime))
            print(('Count of the cycles:', count))
            print(('Collision hash:', newHashPart))

            return {"inputHash": hashPart, "time": totalTime, "cycles": count, "collisionHash": newHashPart}

        except Exception as e:
            print(str(e))

    def findCollisionWithDBSet(self, hashPart=None):
        """
        Function is looking for a collision with hashPart
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

            count = 0
            status = 0

            start = timeit.default_timer()
            while not r.sismember('hset', hashPart):
                r.sadd('hset', hashPart)
                count += 1
                status += 1
                if status == 10000000:
                    status = 0
                    print('\n' * 100)
                    print('Count of cycles:', count)
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')

                hashPart = hashlib.sha256(hashPart.encode('utf-8')).hexdigest()[0:hashPartLength]

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            print('\n##### DBSet method - Collision found process succeeded! #####')
            print("Collision found after %s seconds" % (totalTime))
            print(('Count of the cycles:', r.scard('hset')))
            print(('Collision hash:', hashPart))
            # print 'Index of collision hash:'
            return {"inputHash": hashPart, "time": totalTime, "cycles": count, "collisionHash": hashPart}

        except Exception as e:
            print(str(e))

    def findCollisionIntensity(self, hashPart=None):
        """
        The test method saving hashes in cycles.

        :param hashPart: the input hash loaded from a file
        """
        try:
            if not hashPart:
                hashPart = self.hashPart
                hashPartLength = self.hashPartLength
            else:
                hashPartLength = len(hashPart)

            status = 0
            count = 0
            newHashPart = bytes(hashPart, 'utf-8')
            bloomFilter = pybloomfilter.BloomFilter(10000000000, 0.01) #up to 10 bilions
            start = timeit.default_timer()

            while True:
                if newHashPart not in bloomFilter:
                    bloomFilter.update(newHashPart)
                    count += 1
                    status += 1
                    if status == 10000000:
                        print('\n' * 100)
                        print('Count of cycles:', count)
                        print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')
                        status = 0

                    strHashPart = binascii.unhexlify(newHashPart)
                    newHash = hashlib.sha256(strHashPart).hexdigest()
                    newHash = newHash[0:hashPartLength]
                    newHashPart = bytes(newHash, 'utf-8')
                else:
                    print("Potencional collision successfully passed!")
                    print("Suspicious hash: ", newHash)
                    break

            print("Second part started... ")
            collisionHash = newHashPart
            index = count
            newHashPart = bytes(hashPart, 'utf-8')
            status = 0
            count = 0

            while newHashPart != collisionHash:
                count += 1
                status += 1
                if status == 10000000:
                    print('\n' * 100)
                    print('Collision found! Searching for collision index...')
                    print('Count of cycles:', count)
                    print('Run time:', round((timeit.default_timer() - start) / 60, 3), 'minutes')
                    status = 0
                strHashPart = binascii.unhexlify(newHashPart)
                newHash = hashlib.sha256(strHashPart).hexdigest()
                newHash = newHash[0:hashPartLength]
                newHashPart = bytes(newHash, 'utf-8')

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)

            print('\n##### findCollisionIntensity - Collision found process succeeded! #####')
            print('\nInput hashPart:', hashPart)
            print("Collision found after %s seconds" % (totalTime))
            print('Count of the cycles:', index-count)
            print('Collision hash:', newHash)
            print('Cycles between collision hashes:', cycles-index)

            return {"inputHash": hashPart, "time": totalTime, "cycles": cycles, "collisionHash": newHash,
                    "indexOfCollision": index, "cyclesBetCol": cycles-index}

        except Exception as e:
            print(str(e))


def main():
    # Input parameters

    parser = argparse.ArgumentParser(usage='$prog [options] -b 32 -i hash.txt',
                                     description='SHA collision finder', add_help=True,
                                     epilog='SHA collision finder. Written by Jan Stangler, Ondrej\
                                      Gajdusek, Sarka Chwastkova, VUT FEKT, ICT1 project, 2017')
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
    parser.add_argument('-m', '--memory', action='store_true', dest='memory',
                        help='-m Memory check during a process.', required=False)
    parser.add_argument('-c', '--capacity', action='store', dest='capacity',
                        help='-c Set a length of default storage - SET.', required=False)
    parser.add_argument('-r', '--redis', action='store_true', dest='redis',
                        help='-r Store hashes in redis database.', required=False)
    args = parser.parse_args()

    # Instance of the class Shacol
    shacol = Shacol(args.bits, args.inputFile, args.hashGroup, args.text, args.first, args.bloom, args.memory)
    shacol.getInfo()

    print("Do you want to proceed?")
    input('\nPress Enter to continue...')

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
                    if args.capacity:
                        shacol.findExperimental(maxSet=args.capacity,memoryCheck=True)
                    else:
                        if args.redis:
                            shacol.findCollisionWithDBSet(memoryCheck=True)
                        else:
                            shacol.findExperimental(memoryCheck=True)
                else:
                    if args.capacity:
                        shacol.findExperimental(maxSet=args.capacity)
                    else:
                        if args.redis:
                            shacol.findCollisionWithDBSet()
                        else:
                            # shacol.findCollisionIntensity()
                            shacol.findExperimental()
                            # shacol.findCollisionStr()
                            # shacol.findCollisionInt()
    else:
        if args.bloom:
            if args.memory:
                if args.capacity:
                    shacol.findBestHashBloom(maxSet=args.capacity,memoryCheck=True)
                else:
                    shacol.findBestHashBloom(memoryCheck=True)
            else:
                if args.capacity:
                    shacol.findBestHashBloom(maxSet=args.capacity)
                else:
                    shacol.findBestHashBloom()
        else:
            if args.memory:
                if args.capacity:
                    shacol.findBestHash(maxSet=args.capacity,memoryCheck=True)
                else:
                    shacol.findBestHash(memoryCheck=True)
            else:
                if args.capacity:
                    shacol.findBestHash(maxSet=args.capacity)
                else:
                    shacol.findBestHash()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted... Terminating')
        sys.exit()
