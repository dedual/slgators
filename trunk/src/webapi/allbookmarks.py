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



def getAll(fname, lname, start='0', end='10'):
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    assert(isinstance(cursor, MySQLdb.cursors.Cursor))
    cursor.execute(""" SELECT DISTINCT `bookmark`.`name`, `bookmark`.`id`, `book`.`title`, `book`.`UUID`, `bookmark`.`page` FROM bookmark, book, user WHERE ((`bookmark`.`id` =user.bookmark_id) AND (`user`.`fname` ='""" + MySQLdb.escape_string(fname) + """') AND (`user`.`lname` ='""" + MySQLdb.escape_string(lname) +"""') AND (`book`.`id` =bookmark.bookid)) ORDER BY `book`.`title` ASC LIMIT """ + start +"," + end + """;""")
    return cursor.fetchall()


def handle_form():
    form = cgi.FieldStorage()
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    start = form.getvalue("start")
    end = form.getvalue("end")
    if start and end:
        result = ""
        for row in getAll(fname, lname, start, end):
            for item in row:
                result += str(item) + ","
            result.strip()
            result = result.replace(",", "|")
            print result[:-1]       
    else:
        for row in getAll("Ghais", "Ireton"):
            result = ""
            for item in row:
                result += str(item) + ","
            result.strip()
            result = result.replace(",", "|")
            print result[:-1]
            

        


print_cont()
print_title()
handle_form()

