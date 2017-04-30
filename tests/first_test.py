"""
shacol_instance = shacol.Shacol(BITS_TARGET, inputFile)
for i in range(4, 21):
    shacol.changeBitLength(i)
    shacol.getInfo()
    vysledky = shacol.findCollisionFast()
    print
    "pro pocet bitu ", i, vysledky
    print
    "#####################################################" 
"""

import unittest
import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import shacol

BITS_TARGET = 28
INPUT_FILE = root_dir + "/hash.txt"
TEST_HASH = "fe1e4492c12bb3204d6745394b7512e3f6d617927aa1baa977dc3c3ec6c321ef"


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_int_method(self):
        shacol_instance = shacol.Shacol(BITS_TARGET, INPUT_FILE)

        expectation = {'lastTemp': 'f8848ee',
                       'cyclesBetCol': 4436,
                       'inputHash': 'fe1e449',
                       'indexOfLast': 34290,
                       'dataStructConsum': 2.0,
                       'indexOfFirst': 29854,
                       'collisionHash': '5b7fe78',
                       'inputString': '',
                       'firstTemp': '5f5a679'}

        result = shacol_instance.findCollisionInt()
        result.pop('time')

        self.assertEqual(result, expectation)

    def test_str_method(self):
        shacol_instance = shacol.Shacol(BITS_TARGET, INPUT_FILE)

        expectation = {'lastTemp': 'f8848ee',
                       'cyclesBetCol': 4436,
                       'inputHash': 'fe1e449',
                       'indexOfLast': 34290,
                       'dataStructConsum': 2.0,
                       'indexOfFirst': 29854,
                       'collisionHash': '5b7fe78',
                       'inputString': '',
                       'firstTemp': '5f5a679'}

        result = shacol_instance.findCollisionStr()
        result.pop('time')

        self.assertEqual(result, expectation)

    def test_DB_method(self):
        shacol_instance = shacol.Shacol(BITS_TARGET, INPUT_FILE)

        expectation = {'lastTemp': 'f8848ee',
                       'cyclesBetCol': 4436,
                       'inputHash': 'fe1e449',
                       'indexOfLast': 34290,
                       'indexOfFirst': 29854,
                       'collisionHash': '5b7fe78',
                       'inputString': '',
                       'firstTemp': '5f5a679'}

        result = shacol_instance.findCollisionWithDBSet()
        result.pop('time')
        result.pop('dataStructConsum')

        self.assertEqual(result, expectation)


if __name__ == '__main__':
    unittest.main()
