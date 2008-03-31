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
    page = int(form.getvalue("page")) 
    if page:
        result = ""
        for row in user_info.fetch_all_bookmarks(fname, lname, page):
            str_row = [str(x) for x in row]
            print "|".join(str_row)
            """
            for item in row:
                result += str(item) + ","
            result.strip()
            result = result.replace(",", "|")
            print result
            """
            print "<P>"      
    else:
        for row in user_info.fetch_all_bookmarks("Ghais", "Ireton"):
            str_row = [str(x) for x in row]
            print "|".join(str_row)
            """
            result = ""
            for item in row:
                result += str(item) + ","
            result.strip()
            result = result.replace(",", "|")
            print result
            """
            print "<P>"

        


print_cont()
#print_title()
handle_form()

