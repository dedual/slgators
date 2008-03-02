#!/usr/bin/env python

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

def check_usr(fname, lname):
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    assert(isinstance(cursor, MySQLdb.cursors.Cursor))
    cursor.execute("SELECT fname, lname FROM user WHERE(fname = '" + fname + "'AND lname= '" + lname + "');");
    result = cursor.fetchone()
    db.close()
    return result



def fetch_user_info(fname, lname):
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    assert(isinstance(cursor, MySQLdb.cursors.Cursor))
    cursor.execute("select bookmark.id, bookmark.name, book.title, bookmark.page from book,bookmark, user where (user.fname = '" + fname + "' and user.lname = '" + lname + "' and user.bookmark_id = bookmark.id and bookmark.bookid=book.id) GROUP BY book.title;")
    result = cursor.fetchall()
    db.close()
    return result

def add_user(fname, lname):
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    assert(isinstance(cursor, MySQLdb.cursors.Cursor))
    cursor.execute("""INSERT INTO `amazon`.`user` (
    `fname` ,
    `lname` ,
    `bookmark_id` ,
    `languag`
    ) 
    VALUES ('""" + fname + "', '" + lname + """', NULL , 'en'
    );""")
    db.close()

def handle_form():
    #Corrected Functionality
    #If the user is registered but has no bookmarks then we return None
    #If the user is not registerd the we register him and we return New
    #In either case the user always has a bookmark however this bookmark might have no reference to a book
    #This case should be considered as a reference to the default page.
    #In summary every person has a bookmark to the default starting page. This will make it easier later on to access it directly
    #any bookmarks the user has. To be discussed with nicolas
    form = cgi.FieldStorage()
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    result = check_usr(fname, lname)
    if(result):
        #Exact Details to be discussed with nicolas
        info = fetch_user_info(fname, lname)
        if info:
            for row in info:
                print str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "|" + str(row[3])
        else:
            print "None"
    else:
        add_user(fname, lname)
        print "New"
        
        


print_cont()
print_title()
handle_form()
