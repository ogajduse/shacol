import sys, os, sqlite3, subprocess, git
print(os.path.dirname(os.path.abspath(__file__))+"/../app/aplikace")
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")

import shacol
db_location = os.path.dirname(os.path.abspath(__file__))+"/../app/aplikace/db.sqlite3"
git_repo = r = git.repo.Repo(os.path.dirname(os.path.abspath(__file__))+"/../")

def main():
    sha256 = True
    BITS = 32
    inputFile = "hash.txt"
    shacolInstance = shacol.Shacol(sha256, BITS, inputFile)

    for i in range(4, 33, 4):
        shacolInstance.changeBitLength(i)
        shacolInstance.getInfo()
        results = shacolInstance.findCollisionStr()
        method = "String method"
        dbInsert(results, method, i)

        results = shacolInstance.findCollisionInt()
        method = "Int method"
        dbInsert(results, method, i)

        #results = shacolInstance.findCollisionWithDBSet()
        #method = "Method with DB Set"
        #dbInsert(results, method, i)

        results = shacolInstance.findCollisionIntBF()
        method = "Int BF"
        # dbInsert(results, method, i)


            #print("INT METODA:::")
            #shacol.findCollisionInt()
            #shacol.findCollisionWithDBSet()

def dbInsert(results, method, bits):
    db_conn = sqlite3.connect(db_location)
    db_conn.execute("INSERT INTO website_collision (hash_order, input_hash, total_time, cycles, coll_hash, test_method, bits, git_revision) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (results["indexOfCollision"], results["inputHash"], results["time"], results["cycles"], results["collisionHash"], method, bits, git_repo.git.describe()))
    db_conn.commit()
    print("Pridano do databaze")
    db_conn.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted... Terminating')
        sys.exit()

#db_conn.close()


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
