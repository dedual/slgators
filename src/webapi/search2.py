#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
from amazon import amazon_search
from amazon import amazon_review


def unique(s):
    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].page

    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.

    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.

    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """

    n = len(s)
    if n == 0:
        return []

    # Try using a dict first, as that's the fastest and will usually
    # work.  If it doesn't work, it will usually fail quickly, so it
    # usually doesn't cost much to *try* it.  It requires that all the
    # sequence elements be hashable, and support equality comparison.
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

    # We can't hash all the elements.  Second fastest is to sort,
    # which brings the equal elements together; then duplicates are
    # easy to weed out in a single pass.
    # NOTE:  Python's list.sort() was designed to be efficient in the
    # presence of many duplicate elements.  This isn't true of all
    # sort functions in all languages or libraries, so this approach
    # is more effective in Python than it may be elsewhere.
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u





def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db


def pg_search(title, page):
    if page < 0:
        return {}
    start = (page - 1) * 10
    end =  10
    sqlquery = """SELECT DISTINCT `id`, `title` , `creator` , `contributor`, `UUID`, `subject`
    FROM `book`
    WHERE MATCH (
    title, friendly_title
    )
    AGAINST (
    '""" + MySQLdb.escape_string(title) + """'
    ) ;"""
    db = connect_to_database("amazon", "root", "gitkotwg0")    #replace with password
    cursor = db.cursor()
    cursor.execute(sqlquery)
    result = cursor.fetchall()
    db.close()
    books = {}
    if (start > len(result)):
        start = len(result)
    for i in xrange(start, len(result)):
        if (len(books) == end):
            break
        id, title, creator, contributor, uuid, subject = result[i]
        if books.has_key(id):
            if creator != 'NULL':
                books[id]['creator'].append(creator)
            else:
                books[id]['creator'].append("None")
                
            if contributor != 'NULL':
                books[id]['contributor'].append(contributor)
            else:
                books[id]['contributor'].append("None")                
                
            if uuid != 'NULL':
                books[id]['UUID'].append(uuid)
            else:
                books[id]['UUID'].append(uuid)
                
            if subject != 'NULL':
                books[id]['subject'].append(subject)
            else:
                books[id]['subject'].append("None")
            
            books[id]['creator'] = unique(books[id]['creator'])
            books[id]['contributor'] = unique(books[id]['contributor'])
            books[id]['UUID'] = unique(books[id]['UUID'])
            books[id]['subject'] = unique(books[id]['subject'])
        else:
            books[id] = {'title': title, 'creator' : [], 'contributor' : [], 'UUID' : [], 'subject' : [] }
            if creator != 'NULL':
                books[id]['creator'].append(creator)
            else:
                books[id]['creator'].append("None")
                
            if contributor != 'NULL':
                books[id]['contributor'].append(contributor)
            else:
                books[id]['contributor'].append("None")
                
            if uuid != 'NULL':
                books[id]['UUID'].append(uuid)
            else:
                books[id]['UUID'].append(uuid)
                
            if subject != 'NULL':
                books[id]['subject'].append(subject)
            else:
                books[id]['subject'].append("None")
        
    return books




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
    """etextid|title|author|contributor|UUID|subject|rankings|ASIN"""
    form = cgi.FieldStorage()
    title = form.getvalue("title")
    page = int(form.getvalue('page'))
    books = pg_search(title, page)
    output = ""
    for book_id in  books.keys():
        asin = amazon_search.get_ASIN(book_id)
        
        print book_id + "|" +  books[book_id]['title'] + "|" + "#".join(books[book_id]["UUID"]) + "|",
        print "#".join(books[book_id]["creator"]) + "|",
        print "#".join(books[book_id]["contributor"]) + "|",
        print "#".join(books[book_id]["subject"]) + "|" ,
        print amazon_review.avarage_rating(asin) + "|",
        if asin:
            print asin + "<p>"
        else:
            print "None <p>" 
print_cont()
handle_form()


