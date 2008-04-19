#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
from pg import top100
from amazon import amazon_search




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
    try:
        start = int(form.getvalue('start'))
        end = int(form.getvalue("end"))
    except TypeError, e:
        print e
    books = top100.get_top_100_books(start, end)
    output = ""
    for book_id in  books.keys():
        asin = amazon_search.get_ASIN(book_id)
        if asin == None:
            asin = "None"
        
        print books[book_id]['title'] + "|" + book_id + "|" +  books[book_id]["UUID"] + "|" + asin + "<p>"

        
print_cont()
handle_form()
