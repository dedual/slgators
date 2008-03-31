#!/usr/bin/python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
from user_db import user_info
def print_cont():
    print "Content-type: text/html"
    print

def print_title():
    print """
    <html>

    <head><title>SecondLife DB</title></head>

    <body>

    """

    
  
def handle_form():
    form = cgi.FieldStorage()
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    bookid = form.getvalue("bookid")
    page = form.getvalue("page")
    name = form.getvalue("name")
    result = user_info.add_bookmark(fname, lname, name, bookid, str(page))
        
        


print_cont()
#print_title()
handle_form()

        
        

