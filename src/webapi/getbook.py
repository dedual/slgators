from pg import getbook


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
    


def handle_form():
    form = cgi.FieldStorage()
    bookid = form.getvalue("id")
    page = form.getvalue("pagen")
    f = getbook.getBook(bookid)
    print getbook.getpage(page, f)


print_cont()
print_title()
handle_form()