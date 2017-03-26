
import sys, os, sqlite3, subprocess
print(os.path.dirname(os.path.abspath(__file__))+"/../")
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")

import shacol
sha256 = True
#BITS = 32
inputFile = "hash.txt"
hashGroup = True

shacol = shacol.Shacol(sha256, 1, inputFile, hashGroup)
for i in range(4, 9, 4):
    shacol.changeBitLength(i)
    shacol.getInfo()

    results = shacol.findCollisionStr()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(results["time"])

    print("INT METODA:::")
    shacol.findCollisionInt()
    shacol.findCollisionWithDBSet()

"""
INDEX - print(results["index"])
INPUT_HASH - print(results["inputHash"])
TOTAL_TIME - print(results["time"])
CYCLES - print(results["cycles"])
COLL_HASH - print(results["collisionHash"])
TEST_METHOD - "INT", "STR", "DB"
BITS - print(results["bits"])
GIT_REVISION - subprocess.check_output(["git", "describe"])
"""

db_conn = sqlite3.connect('db.sqlite3')
db_conn.execute("INSERT INTO WEBSITE_COLLISION (INDEX, INPUT_HASH, TOTAL_TIME, CYCLES, COLL_HASH, TEST_METHOD, BITS, GIT_REVISION) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (promenne!!!))
db_conn.commit()
db_conn.close()
