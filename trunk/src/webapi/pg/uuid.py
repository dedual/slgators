import MySQLdb

def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db



def csv2List(filename):
    all_lst = []
    f = open(filename, "r")
    for line in f:
        assert(isinstance(line, str))
        line = line.strip()
        lst = line.split(",")
        all_lst.append([x[1:-1] for x in lst])
    return all_lst

uuid_lst = csv2List("uuids.csv")
for id, uuid in uuid_lst:
    sql_query = """UPDATE `amazon`.`book` SET `UUID` = '""" + uuid + """' WHERE book.id = '""" + id + """' ;"""
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    cursor.execute(sql_query)

    