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
    etextid = form.getvalue("bookid")
    try:
        page = int(form.getvalue("page"))
        if page < 0:
            page = None
    except TypeError:
        page = None
    
    if page != None:
        result = ""
        for row in user_info.fetch_all_bookmarks(fname, lname, etextid, int(page)):
            str_row = [str(x).strip() for x in row]
            print "|".join(str_row)
            print "<P>"      
    else:
        for row in user_info.fetch_all_bookmarks(fname, lname, etextid):
            str_row = [str(x).strip() for x in row]
            print "|".join(str_row)
            print "<P>"

print_cont()
handle_form()

