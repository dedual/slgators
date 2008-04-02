#!/usr/bin/env python

import cgi
#import cgitb; cgitb.enable()  # for troubleshooting
import MySQLdb
from amazon import amazon_search


def unique(s):
    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].

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
    start = str((page - 1) * 10) 
    end =  str(page * 10)
    sqlquery = """SELECT DISTINCT `id`, `title` , `creator` , `contributor`
    FROM `book`
    WHERE MATCH (
    title, friendly_title
    )
    AGAINST (
    '""" + MySQLdb.escape_string(title) + """'
    ) LIMIT """ + start + ',' + end + ';'
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    cursor.execute(sqlquery)
    result = cursor.fetchall()
    books = {}
    for id, title, creator, contributor in result:
        if books.has_key(id):
            if creator:
                books[id]['creator'].append(creator)
            if contributor:
                books[id]['contributor'].append(contributor)
            books[id]['creator'] = unique(books[id]['creator'])
            books[id]['contributor'] = unique(books[id]['contributor'])
        else:
            books[id] = {'title': title, 'creator' : [], 'contributor' : []}
            if creator:
                books[id]['creator'].append(creator)
            if contributor:
                books[id]['contributor'].append(contributor)
        
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
    form = cgi.FieldStorage()
    title = "Alice in wonderland" #form.getvalue("title")
    page = 1 #int(form.getvalue('page'))
    books = pg_search(title, page)
    output = ""
    for book_id in  books.keys():
        asin = amazon_search.get_ASIN(book_id)
        
        print books[book_id]['title'] + "|" + book_id + "|" +  asin + "<p>"
#        for creator in books[book_id]['creator']:
#            output += creator + ","
#        output = output[:-1]
#        output += "|"
#        for contrib in books[book_id]['contributor']:
#            output += contrib + ","
#            output = output[:-1]
#        
#print_cont()
handle_form()
#print pg_search("Alice in wonderland", 1);