import urllib2
import re
import MySQLdb

from amazon import amazon_search

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


def __pg_search(page):
    etextids = get_top_books()
    if 0 > page:
        return {}
    start = (page - 1) * 10 
    end =  page * 10
    
    db = connect_to_database("amazon", "root", "gitkotwg0")     #replace with password
    cursor = db.cursor()
    books = {}
    
    for i in xrange(start, end):
        etextid = etextids[i]
        sqlquery = """SELECT DISTINCT `id`, `title` , `creator` , `contributor`
                      FROM `book`
                      WHERE id = '""" + MySQLdb.escape_string(etextid) + """'
                      GROUP BY id """
        cursor.execute(sqlquery)
        result = cursor.fetchall()
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
    db.close()
        
    return books


def get_top_100_books(page):
    books = __pg_search(page)
    return books


    
    
        
