#!/usr/bin/env python
from pg import getbook




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
    


def handle_form():
    form = cgi.FieldStorage()
    bookid = form.getvalue("id")
    start = int(form.getvalue("start"))
    end = int(form.getvalue("end"))
    f = getbook.getBook(bookid)
    print getbook.getlines(f, start, end)


print_cont()
print_title()
handle_form()