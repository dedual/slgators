#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
from amazon import amazon_review
from pyaws import ecs
import linecache

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

def add_new_lines(string, nchars = 92):
    f = string.split(" ")
    line = ""
    temp_line = ""
    for word in f:
        if (word[-1] == "\n" or word[-1] == unicode("\n")):
            temp_line += word
            line += temp_line
            temp_line = ""
        elif (len(temp_line) + len(word) + 1 > nchars):
            line += temp_line + "\n"
            temp_line = ""
        temp_line += " " + word
    return line
    #lenght = len(string)
    #insertion_point = []
    #j = 0
    #for i in xrange(1, len(string)):
        #if i % nchars == 0:
            #k = j
            #j = i
            #while (string[j] != unicode(" ") and string[j] != unicode("\n") and string[j] != "\n" and string[j] != " "):
                #a = string[j]
                #j -= 1
            #insertion_point.append([k,j])
    #result = "\n".join([string[point[0]:point[1]] for point  in insertion_point])       
    #result += string[j:]
    #return result
            
def getlines(f, start, end, nchars=92):
    string = add_new_lines(f)
    f = string.split("\n")
    lines = ""
    pad = ''
    if end > len(f):
        end = len(f) -1
    if start > len(f):
        end = len(f) - 1
    for i in range(start, end+1):
        pad = ''
        line = f[i].strip()
        line_len = len(line)
        if line_len < nchars:
            pad = ' ' * (nchars - line_len)
        pad = pad + '|\n'
        lines = lines + line + pad
    return lines            
            
def handle_form():
    form = cgi.FieldStorage()
    db = connect_to_database("amazon", "root", "gitkotwg0")    #replace with password
    cursor = db.cursor()
    
    ASIN = form.getvalue("ASIN") 
    bookid = form.getvalue('bookid')
    start = form.getvalue("start")
    end = form.getvalue("end")
    page = form.getvalue("page")
    images = form.getvalue("images")
    if(start and end):
        start = int(start) - 1
        end = int(end)
    elif(page):
        page = int(page)
        start = (page - 1)* 58
        end = ((page - 1) * 58 +1) + 57
        
    
    if ASIN:
        pass
    elif bookid:
        ASIN = get_ASIN(bookid)        
        
    try:
        editorial = int(form.getvalue('editorial'))
    except TypeError:
        editorial = None
    try:
        customer = int(form.getvalue('customer'))
    except TypeError:
        customer = None
    try:
        similarities = int(form.getvalue('similar'))
    except TypeError:
        similarities = None
    try:
        images = int(form.getvalue('images'))
    except TypeError:
        images = None
    if editorial:
        result = ""
        for review in amazon_review.amazon_editorial_review(ASIN):
            source, content = review
            result += "Source: " + source + "\n"
            result += content + "\n"
    elif customer:
        result = ""
        for review in amazon_review.amazon_customer_review(ASIN):
            rating, summary, content = review
            result += "Rating: " + rating + "\n"
            result += "Summary: " + summary + "\n"
            result += "Content<\n>" + content + "\n"
        result = result.replace("<", "")
        result = result.replace(">", "")
        print getlines(result, start, end)
    elif similarities:
        for similar in amazon_review.amazon_similarities(ASIN):
            title, id = similar
            print title + "|" + id + "<p>"
    elif images:
        for image in amazon_review.amazon_get_image(ASIN):
            print image + "<p>"

print_cont()            
handle_form()