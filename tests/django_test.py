import sys, os, sqlite3, git, pybloomfilter
import pymysql as mariadb

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

import shacol
db_location = '85.255.0.154'
git_repo = git.repo.Repo(root_dir)

def main():
    sha256 = True
    BITS = 32
    inputFile = root_dir + "/hash.txt"
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

        # results = shacolInstance.findCollisionIntBF()
        # method = "Int BF"
        # dbInsert(results, method, i)


            #print("INT METODA:::")
            #shacol.findCollisionInt()
            #shacol.findCollisionWithDBSet()

def dbInsert(results, method, bits):
    db_conn = mariadb.connect(host = db_location, user='shacol_django_u', password='Aim4Uusoom9ea8', database='shacol_django')
    cursor = db_conn.cursor()
    add_collision = ("INSERT INTO website_collision"
                    "(hash_order, input_hash, total_time, cycles, coll_hash, test_method, bits, git_revision)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    
    data_collision = (int(results["indexOfCollision"]), results["inputHash"], results["time"], int(results["cycles"]), results["collisionHash"], method, int(bits), git_repo.git.describe())
    cursor.execute(add_collision, data_collision)

    db_conn.commit()
    cursor.close()
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
