#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
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
    title = form.getvalue("title")
    page = int(form.getvalue('page'))
    result = amazon_search.group_searches(title, page)
    if(result):
        for title, id, ASIN in result:
            if id:
                print "<p>" + title + "|" + str(id[0]) + "|" +str(ASIN)
                
            else:
                print "<p>" + title + '|None' + '|None'
    else:
        print("Error")

        
        
print_cont()
handle_form()
