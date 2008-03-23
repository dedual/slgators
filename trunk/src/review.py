#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
from amazon import amazon_review

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


def handle_form():
    form = cgi.FieldStorage()
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    
    ASIN = form.getvalue("ASIN") 
    bookid = form.getvalue('bookid')
    
    if ASIN:
        pass
    elif bookid:
        sqlQuery = """ SELECT DISTINCT `ASIN`
        FROM `book`
        WHERE `id` = CONVERT( _utf8 '""" + bookid +"""'
        USING latin1 )
        COLLATE latin1_swedish_ci
        LIMIT 0 , 30 
        """
        cursor.execute(sqlQuery)
        ASIN = cursor.fetchone()[0]
        
    try:
        editorial = int(form.getvalue('editorial'))
    except TypeError:
       editorial = 0
    try:
        customer = int(form.getvalue('customer'))
    except TypeError:
        customer = 0
    try:
        similarities = int(form.getvalue('similar'))
    except TypeError:
        similarities = 0
    try:
        images = int(form.getvalue('images'))
    except TypeError:
        images = 0
    
    if editorial:
        for review in amazon_review.amazon_editorial_review(ASIN):
            source, content = review
            print source + "<p>"
            print content + "<p>"
    elif customer:
        for review in amazon_review.amazon_customer_review(ASIN):
            rating, summary, content = review
            print rating + "<p>"
            print summary + "<p>"
            print content + "<p>"
    elif similarities:
        for similar in amazon_review.amazon_similarities(ASIN):
            title, id = similar
            print title + "|" + id + "<p>"
    elif images:
        for image in amazon_review.amazon_get_image(ASIN):
            print image + "<p>"
                    
                    

print_cont()
print_title()
handle_form()