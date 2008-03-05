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
    start = form.getvalue("start")
    end = form.getvalue("end")
    page = form.getvalue("page")
    if not bookid:
        print 0
    else:
        if start and end:
            continue
        elif page:
            start = (page - 1)* 58 + 1
            end = ((page - 1) * 58 +1) + 57
        f = getbook.getBook(bookid)
        print getbook.getlines(f, start, end)


print_cont()
print_title()
handle_form()