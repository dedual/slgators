#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
from amazon import amazon_review
from pyaws import ecs

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


def reverse_contrib(contributor):
    contributor = contributor.split(",")
    contributor[2] = contributor[2].split()[-1]
    contributor.reverse()
    return [x.strip() for x in contributor]

def correct_contrib(contributor):
    contributor = reverse_contrib(contributor)
    contributor[1] += ' '
    contributor = "".join(contributor[1:])
    return contributor

def get_ASIN(etextid):
    sql_query = """SELECT DISTINCT title, creator, contributor
     FROM book
     WHERE id = '""" + etextid + "';"
    db = connect_to_database("amazon", "root", "gitkotwg0")    #repace with password
    cursor = db.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    db.close()
    for title, creator, contributor in results:
        if contributor != 'NULL':
            ecs.setLicenseKey('0ZW74MMABE2VX9H26182')
            try:
                books = ecs.ItemSearch(Keywords = correct_contrib(contributor) + ' ' + title,SearchIndex='Books', Sort='relevancerank')
                return books[0].ASIN
            except KeyError:
                print "KEYERROR"
        else:
            try:
                books = ecs.ItemSearch(title,SearchIndex='Books', Sort='relevancerank')
                return books[0].ASIN
            except KeyError:
                return "KeyError"
            
def handle_form():
    form = cgi.FieldStorage()
    db = connect_to_database("amazon", "root", "gitkotwg0")    #replace with password
    cursor = db.cursor()
    
    ASIN = form.getvalue("ASIN") 
    bookid = form.getvalue('bookid')
    
    if ASIN:
        pass
    elif bookid:
        ASIN = get_ASIN(bookid)
        
    print ASIN
        
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
                    
 
#print get_ASIN("etext2600")
                    
print_cont()
handle_form()