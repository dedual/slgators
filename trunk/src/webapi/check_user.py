#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
from user_db import user_info

def print_cont():
    """ Prints the Content-type"""
    print "Content-type: text/html"
    print

def print_title():
    """Prints the title of the page"""
    print """
    <html>

    <head><title>SecondLife DB</title></head>

    <body>

    """

    

def handle_form():
    """ called by invoking 'check_user.py?fname=firstname&lname=lastname'
    If the user is already in the database and has some personalized bookmarks then the return is the string bookmark.id|bookmark.name|book.title|bookmark.page
    If the user is already in the database but has no bookarks then we return None
    If the user is not in the database, then we insert the user into the database and return New
    """
    
    form = cgi.FieldStorage()
    fname = form.getvalue("fname")
    lname = form.getvalue("lname")
    if fname and lname:
        if(user_info.check_usr(fname, lname)):
            #Exact Details to be discussed with nicolas
            info = user_info.fetch_user_bookmarks(fname, lname)
            if info:
                for row in info:
                    print str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "|" + str(row[3]) + "|" + str(row[4]) + "<p>"
            else:
                print "None"
        else:
            user_info.add_user(fname, lname)
            print "New"
    else:
        print "fname and lname required"
        
        


print_cont()
handle_form()
