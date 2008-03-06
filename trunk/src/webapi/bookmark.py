#!/usr/bin/python
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
    cursor.execute("""SELECT `bookmark`.`id`
    FROM bookmark, user
    WHERE (
    (
    `bookmark`.`id` = user.bookmark_id
    )
    AND (
    `user`.`fname` = '""" + fname + """'
    )
    AND (
    `user`.`lname` = '""" + lname +"""'
    )
    AND (
    `bookmark`.`page` = """ + page + """
    )
    ); """)

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
        cursor.execute("""SELECT MAX(`id`)
        FROM `bookmark`
        WHERE bookid = '""" + MySQLdb.escape_string(bookid) +"""'
        AND page =""" + str(page) +";")
        id = str(cursor.fetchone()[0])
        cursor.execute("""INSERT INTO `amazon`.`user` (
        `fname` ,
        `lname` ,
        `bookmark_id` ,
        `languag`
        )
        VALUES (
        '""" + fname +"""', '""" + lname + """', '""" + id + """', NULL
        );""")
        print 1
    else:
        print 0
        
        
def handle_form():
    form = cgi.FieldStorage()
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    bookid = form.getvalue("bookid")
    page = form.getvalue("page")
    name = form.getvalue("name")
    result = insertBookmark(fname, lname, name, bookid, str(page))
        
        


print_cont()
print_title()
handle_form()

        
        

