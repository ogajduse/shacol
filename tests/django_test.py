import sys, os, sqlite3, subprocess, git
print(os.path.dirname(os.path.abspath(__file__))+"/../app/aplikace")
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")

import shacol
db_location = os.path.dirname(os.path.abspath(__file__))+"/../app/aplikace/db.sqlite3"
git_repo = r = git.repo.Repo(os.path.dirname(os.path.abspath(__file__))+"/../")
sha256 = True
BITS = 32
inputFile = "hash.txt"

shacol = shacol.Shacol(sha256, BITS, inputFile)
db_conn = sqlite3.connect(db_location)
print(db_conn)
for i in range(4, 57, 4):
    shacol.changeBitLength(16)
    shacol.getInfo()

    results = shacol.findCollisionStr()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(results)
    results["index"] = i
    results["bits"] = i


    print("INT METODA:::")
    #shacol.findCollisionInt()
    #shacol.findCollisionWithDBSet()
    db_conn.execute("INSERT INTO website_collision (hash_order, input_hash, total_time, cycles, coll_hash, test_method, bits, git_revision) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (results["index"], results["inputHash"], results["time"], results["cycles"], results["collisionHash"], "String method", results["bits"], git_repo.git.describe()))
    db_conn.commit()
    print("Pridano do databaze")
    break

db_conn.close()


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
#db_conn = sqlite3.connect('db.sqlite3')
#db_conn.execute("INSERT INTO WEBSITE_COLLISION (INDEX, INPUT_HASH, TOTAL_TIME, CYCLES, COLL_HASH, TEST_METHOD, BITS, GIT_REVISION) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (promenne!!!))
#db_conn.commit()
#db_conn.close()
