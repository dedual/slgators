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
    cursor.execute("SELECT current_book, current_page FROM usr WHERE fname='" + fname + "' AND lname='" + lname + "';")
    result = cursor.fetchone()
    db.close()
    return result

    
def handle_form():
    form = cgi.FieldStorage()
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    result = check_usr(fname, lname)
    if(result):
        print(result[0] + "|" + str(result[1]))
    else:
        print("user note in data base")


print_cont()
print_title()
handle_form()
