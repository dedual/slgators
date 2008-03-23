#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb


def print_cont():
    """ Prints the Content-type"""
    print "Content-type: text/html"
    print

def print_title():
    """Prints the title of the page"""
    print """
    <html>

    <head><title>SecondLife DB</title></head>

    <body>

    """

    
def connect_to_database(databasename, usr, password):
    """ Connects to a database using usr and password"""
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db

def check_usr(fname, lname):
    """Given a first name and a last name, it checks weather the user exists in the database
    If not it returns Null otherwise it returns (fname, lname) as fetche from the database"""
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    assert(isinstance(cursor, MySQLdb.cursors.Cursor))
    cursor.execute("SELECT fname, lname FROM user WHERE(fname = '" + fname + "'AND lname= '" + lname + "');");
    result = cursor.fetchone()
    db.close()
    return result



def fetch_user_info(fname, lname):
    """Given a first name, and a last name it returns the tupple containing bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page from the database"""
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    assert(isinstance(cursor, MySQLdb.cursors.Cursor))
    cursor.execute("select bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page from book,bookmark, user where (user.fname = '" + fname + "' and user.lname = '" + lname + "' and user.bookmark_id = bookmark.id and bookmark.bookid=book.id) GROUP BY book.title;")
    result = cursor.fetchall()
    db.close()
    return result

def add_user(fname, lname):
    """Given a first name and a last name, this functions inserts a new user into the database and associates him with the empty bookmark"""
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
    """ called by invoking 'check_user.py?fname=firstname&lname=lastname'
    If the user is already in the database and has some personalized bookmarks then the return is the string bookmark.id|bookmark.name|book.title|bookmark.page
    If the user is already in the database but has no bookarks then we return None
    If the user is not in the database, then we insert the user into the database and return New
    """
    
    form = cgi.FieldStorage()
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    result = check_usr(fname, lname)
    if(result):
        #Exact Details to be discussed with nicolas
        info = fetch_user_info(fname, lname)
        if info:
            for row in info:
                print str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "|" + str(row[3]) + "|" + str(row[4])
        else:
            print "None"
    else:
        add_user(fname, lname)
        print "New"
        
        


print_cont()
#print_title()
handle_form()
