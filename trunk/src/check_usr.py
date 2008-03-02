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
    cursor.execute("select bookmark.name, book.title, bookmark.page from book,bookmark, user where (user.fname = '" + fname + "' and user.lname = '" + lname + "' and user.bookmark_id = bookmark.id and bookmark.bookid=book.id);")
    result = cursor.fetchone()
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
    VALUES (""" + fname + ", " + lname + """, NULL , 'en'
    );""")
    db.close()

def handle_form():
    form = cgi.FieldStorage()
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    result = check_usr(fname, lname)
    if(result):
        #Exact Details to be discussed with nicolas
        print (result[0] + "|" + result[1] + "|" + str(result[2]))
    else:
        add_user(fname, lname)
        print "1"
        
        


print_cont()
print_title()
handle_form()
