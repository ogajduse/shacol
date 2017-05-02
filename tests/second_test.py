import sys, os, git
import pymysql as mariadb
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import shacol

db_location = '85.255.0.154'
git_repo = git.repo.Repo(root_dir)

def dbInsert(results, method, bits):
    db_conn = mariadb.connect(host=db_location, user='shacol_django_u', password='Aim4Uusoom9ea8',
                              database='shacol_django')
    cursor = db_conn.cursor()
    add_collision = ("INSERT INTO website_collision"
                    "(hash_order, input_hash, total_time, cycles, coll_hash, firstTemp, lastTemp, total_memory, test_method, bits, git_revision)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data_collision = (int(results["indexOfLast"]), results["inputHash"], results["time"], int(results["cyclesBetCol"]), results["collisionHash"], results["firstTemp"], results["lastTemp"], results["dataStructConsum"], method, int(bits), git_repo.git.describe())
    cursor.execute(add_collision, data_collision)

    db_conn.commit()
    cursor.close()
    db_conn.close()

def main():
    inputValue = root_dir + "/hash.txt"
    shacolInstance = shacol.Shacol(56, inputValue, hashGroup=True)

    for i in range(4, 57, 4):
        shacolInstance.changeBitLength(i)
        shacolInstance.getInfo()
        for input_hash in shacolInstance.shaList:
            results = shacolInstance.findCollisionStr()
            method = "String method"
            dbInsert(results, method, i)

            results = shacolInstance.findCollisionInt()
            method = "Int method"
            dbInsert(results, method, i)
    print("inserting data DONE")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted... Terminating')
        sys.exit()