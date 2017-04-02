from __future__ import division
from __future__ import print_function
# !/usr/bin/env python
# requirements - redis, python3-psutil, future

from future import standard_library

standard_library.install_aliases()
from builtins import input
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import os
import sys
import random
import timeit
import psutil
import hashlib
import argparse
from io import StringIO
import redis
import binascii


class Shacol(object):
    def __init__(self, sha256, bits, inputFile, hashGroup=False, text=False, first=False):
        self.sha256 = sha256
        self.bits = int(bits)
        self.inputFile = inputFile
        self.hashGroup = hashGroup
        self.text = text
        self.first = first

        self.hashPartLength = old_div(int(self.bits), 4)
        self.shaList = []
        self.hashPart = str()

        if inputFile:
            with open(self.inputFile, 'r', encoding='utf-8') as dataFromFile:
                if self.hashGroup:
                    if self.sha256:
                        if self.text:
                            for textInFile in dataFromFile:
                                self.shaList.append(
                                    hashlib.sha256(textInFile.encode('utf-8').hexdigest()[0:self.hashPartLength]))
                        else:
                            for hashInFile in dataFromFile:
                                self.shaList.append(hashInFile[0:self.hashPartLength])
                else:
                    if sha256:
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
        self.hashPartLength = old_div(self.bits, 4)

    def hashToBits(self, hashPart):
        bits = bin(int(binascii.hexlify(hashPart.encode('utf-8', 'surrogatepass')), 16))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    def hashFromBits(self, bitHash):
        n = int(bitHash, 2)
        return self.intToBytes(n).decode('utf-8', 'surrogatepass')

    def intToBytes(self, i):
        hex_string = '%x' % i
        n = len(hex_string)
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

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

            return {"inputHash": hashPart, "time": (totalTime, 's'), "cycles": cycles, "collisionHash": newHashPart,
                    "indexOfCollision": index, "cyclesBetCol": cycles-index,
                    "dataStructConsum": (totalMemory, 'MB')}

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

            return {"inputHash": hashPart, "time": totalTime, "cycles": cycles, "collisionHash": newHash,
                    "indexOfCollision": index, "cyclesBetCol": cycles-index,
                    "dataStructConsum": (totalMemory,'MB')}

        except Exception as e:
            print(str(e))

    def findBestHash(self):
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
                    if len(intHashSet) >= 1000000000:
                        print('\n--- Stated limit reached --- Set count:', len(intHashSet))
                        memOver = True
                        break
                    """ #Memory based control
                    if len(intHashSet) : 10000000 == 0:
                        virtualMem = psutil.virtual_memory().available
                        if virtualMem < 134217728:
                            print('\n!!! Memory capacity reached !!! Set count:', len(intHashSet))
                            memOver = True
                            break
                    """
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

    def findExperimental(self, hashPart=None):
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

            counter = 0
            intHashSet = {int()}
            hashPartLength = len(hashPart)
            newHashPart = int(binascii.hexlify(bytes(hashPart, 'utf-8')), 16)
            print('\nExperimental method started...')

            start = timeit.default_timer()

            while True:
                previousLength = len(intHashSet)
                intHashSet.add(newHashPart)
                if len(intHashSet) == previousLength:
                    break
                counter += 1
                if counter == 1000000:
                    print('!!! State limit reached !!! Cycles:', counter)
                    break

                strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                newHash = hashlib.sha256(strHashPart).hexdigest()
                newHash = newHash[0:hashPartLength]
                newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)
            print('Hashing without store started...')

            while newHashPart not in intHashSet:
                strHashPart = binascii.unhexlify(hex(newHashPart)[2:])
                newHash = hashlib.sha256(strHashPart).hexdigest()
                newHash = newHash[0:hashPartLength]
                newHashPart = int(binascii.hexlify(bytes(newHash, 'utf-8')), 16)
                counter += 1
                status += 1
                if status == 100000000:
                    print(counter)
                    status = 0

            stop = timeit.default_timer()
            totalTime = round(stop - start, 12)
            totalMemory = round(sys.getsizeof(intHashSet) / 1024 / 1024, 3)

            print('\n##### findExperimental - found process succeeded! #####')
            print('\nInput hashPart:', hashPart)
            print("Collision found after %s seconds" % (totalTime))
            print('Count of the cycles:', len(intHashSet)+1)
            print('Collision hash:', newHash)
            index = 0
            for intHash in intHashSet:
                index += 1
                if intHash == newHashPart:
                    print('Index of collision hash:', index)
                    break
            print('Cycles between collision hashes:', cycles-index)
            print('\nSet int structure used', totalMemory, 'MB')
            del intHashSet

            return {"inputHash": hashPart, "time": totalTime, "cycles": counter, "collisionHash": newHash,
            "indexOfCollision:": index, "cyclesBetCol": cycles-index,
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

            start = timeit.default_timer()
            while not r.sismember('hset', hashPart):
                r.sadd('hset', hashPart)
                count += 1
                if count % 10000000 == 0:
                    print(count)
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


def main():
    # Input parameters

    parser = argparse.ArgumentParser(usage='$prog [options] -sha2 -b 32 -i hash.txt',
                                     description='SHA collision finder', add_help=True,
                                     epilog='SHA collision finder. Written by Jan Stangler, Ondrej\
                                      Gajdusek, Sarka Chwastova, VUT FEKT, ICT1 project, 2017')
    parser.add_argument('-sha2', '--sha256', action='store_true', dest='sha256',
                        help='-sha2 (hash algorithm)', required=True)
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
    args = parser.parse_args()

    # Instance of the class Shacol
    shacol = Shacol(args.sha256, args.bits, args.inputFile, args.hashGroup, args.text, args.first)
    shacol.getInfo()

    print("Do you want to proceed?")
    input('\nPress Enter to continue...')

    if args.inputFile:
        if (args.hashGroup):
            for hashes in shacol.shaList:
                if (args.first):
                    shacol.findCollisionFirst(hashes)
                else:
                    shacol.findCollisionInt(hashes)
        else:
            if (args.first):
                shacol.findCollisionFirst()
            else:
                # shacol.findCollisionStr()
                shacol.findCollisionInt()
                # shacol.findExperimental()
    else:
        shacol.findBestHash()

    # shacol.findCollisionWithDBset()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted... Terminating')
        sys.exit()
