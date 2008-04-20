import MySQLdb
import random
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


def __random_w_cover(start, end):
    db = connect_to_database("amazon", "root", "gitkotwg0")     #replace with password
    cursor = db.cursor()
    sql_query = """ SELECT DISTINCT `id`
FROM `book`
WHERE `UUID` != CONVERT( _utf8 '1f62ad03-0350-452f-f1e8-80c4889e57ce '
USING latin1 )
COLLATE latin1_swedish_ci;"""
    cursor.execute(sql_query)
    result = cursor.fetchall()
    result = [item[0] for item in result]
    etextids = list(result)
        
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
            UUID = UUID.strip()
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


def get_random_book(start, end):
    books = __random_w_cover(start, end)
    return books

print get_random_book(1,10)