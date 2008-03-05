import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb

def print_cont():
    print "Content-type: text/html"
    print

def print_title():
    print """
    <html>

    <head><title>SecondLife DB</title></head>

    <body>

    """

    
def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db

def insertBookmark(fname, lname, bookmarkname, bookid, page):
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    assert(isinstance(cursor, MySQLdb.cursors.Cursor))
    cursor.execut("""SELECT `bookid`
    FROM `bookmark`
    WHERE bookid = '""" + bookid +"""'
    AND page =""" + str(page) +";")
    result = cursor.fetchone()
    if not result:        
        cursor.execute("""INSERT INTO `amazon`.`bookmark` (
        `id` ,
        `name` ,
        `bookid` ,
        `page` ,
        `misc`
        )
        VALUES (
        NULL ,'""" + MySQLdb.escape_string(bookmarkname) + "','" + bookid +"', '" + page +"""', NULL
        );""")
        cursor.execut("""SELECT `id`
        FROM `bookmark`
        WHERE bookid = '""" + bookid +"""'
        AND page =""" + str(page) +";")

