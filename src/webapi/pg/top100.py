import urllib2
import re
import MySQLdb


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

def get_top_books():
    """Returns a list containing the ids of the top 100 books in the last 30 days as reported by PG"""
    url = "http://www.gutenberg.org/browse/scores/top"
    etextid = []
    try:
        f = urllib2.urlopen(url)

        begin = False
        end = False
        
        for line in f:
            if __match_begin(line):        #matches where the top 100 books in the last 30 days start
                begin = True
            elif begin:
                if line == '</ol>':         #We have reached the end of the list
                    break        
                id = __get_etextid(line)
                if id:
                    etextid.append(id)
        return etextid                 
    except urllib2.HTTPError, e:
        return etextid

def __match_begin(string):
    """checks for the string that marks the begining of the 100 most read books in the last 30 days"""
    pattern = '<h2 id="books-last30">Top 100 EBooks last 30 days</h2>'
    r = re.compile(pattern)
    return r.search(string)


def __get_etextid(string):
    """The following is a sample for what we are matching against
    We try to extract the 20417
    <li><a href="/etext/20417">The Outline of Science, Vol. 1 (of 4) by J. Arthur Thomson (34196)</a></li>"""

    pattern = '(<li><a href="/etext/)(.*)(">.*</li>)'
    r = re.compile(pattern)
    m = r.match(string)
    if m:
        return 'etext' + m.group(2)
    else:
        return None

def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db


def __pg_search(start, end):
    etextids = get_top_books()
    if 0 > page:
        return {}
        
    if len(etextids) < end:
        end = len(etextids)
    if len(etextids) < start:
        start = len(etextids)
        
    db = connect_to_database("amazon", "root", "gitkotwg0")     #replace with password
    cursor = db.cursor()
    books = {}
    
    for i in xrange(start, end):
        etextid = etextids[i]
        sqlquery = """SELECT DISTINCT `id`, `title` , `creator` , `contributor`, `UUID`
                      FROM `book`
                      WHERE id = '""" + MySQLdb.escape_string(etextid) + "';"
        cursor.execute(sqlquery)
        result = cursor.fetchall()
        books[etextid] = {'title': "Book not available", 'creator' : [], 'contributor' : [], "UUID" : "1f62ad03-0350-452f-f1e8-80c4889e57ce"}
        for id, title, creator, contributor, UUID in result:            
            uuid = uuid.strip()
            if books[id]:
                if creator != 'NULL':
                    books[id]['creator'].append(creator)
                else:
                    books[id]['creator'].append("None")
                if contributor != 'NULL':
                    books[id]['contributor'].append(contributor)
                else:
                    books[id]['contributor'].append("None")                    
                books[id]['creator'] = unique(books[id]['creator'])
                books[id]['contributor'] = unique(books[id]['contributor'])
                books[id]["title"] = title
                books[id]["UUID"] = UUID
            else:
                books[id] = {'title': title, 'creator' : [], 'contributor' : [], "UUID" : UUID}
                if creator:
                    books[id]['creator'].append(creator)
                if contributor:
                    books[id]['contributor'].append(contributor)

    db.close()
        
    return books


def get_top_100_books(start, end):
    books = __pg_search(start, end)
    return books

    
        
