#!/usr/bin/env python
import MySQLdb
import re
from pyaws import ecs

def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db

def reverse_contrib(contributor):
    contributor = contributor.split(",")
    contributor[2] = contributor[2].split()[-1]
    contributor.reverse()
    return [x.strip() for x in contributor]

def correct_contributor(contributor):
    contributor = reverse_contrib(contributor)
    contributor[0] += ' '
    contributor = "".join(contributor)
    return contributor


def truncate_brackets(title):
    pattern = '(.*)(\(.*\))(.*)'
    r = re.compile(pattern)
    m = r.match(title)
    if m:
        title = (m.group(1) + m.group(3)).strip()
    else:
        title =  title.strip()
    pattern = '(.*)(:.*)'
    r = re.compile(pattern)
    m = r.match(title)
    if m:
        return m.group(1).strip()
    else:
        return title

def amazon_search(title):
    ecs.setLicenseKey('0ZW74MMABE2VX9H26182')
    try:
        books = ecs.ItemSearch(title, SearchIndex='Books', Sort='relevancerank')
    except KeyError:
        return []
    return books


def get_pg_books(books, page):
    pg_books = []
    start = (page - 1)* 25
    end = page * 25
    if end > len(books):
        end = len(books)
    for i in range(start, end):
        book = books[i]
        title = book.Title
        contributor = None
        try:
            contributor = book.Creator
            if isinstance(contributor, list):
                pass
            else:
                contributor = [contributor]
        except AttributeError:
            try:
                contrib = book.Author
            except AttributeError:
                contrib = 'None'
            if isinstance(contributor, list):
                pass
            else:
                contributor = [contributor]

        out_result = None
        for contrib in contributor:
            if not contrib:
                contrib = "NONE"
            
            book_author = "NULL"
            try:
                book_author = book.Author[0]
            except AttributeError:
                book_author = "NULL"
            
            sqlquery_for_null = """ SELECT DISTINCT id, contributor
            FROM book
            WHERE title LIKE '%""" + MySQLdb.escape_string(truncate_brackets(title)) + """%' AND MATCH(creator) AGAINST (' """ + MySQLdb.escape_string(book_author) +"""');"""
            db = connect_to_database("amazon", "root", "gitkotwg0")
            cursor = db.cursor()
            cursor.execute(sqlquery_for_null)
            result = cursor.fetchone()
            if result:
                if result[1] == 'NULL':
                    out_result = result
                    break


            sqlsearch = """ SELECT DISTINCT id 
            FROM book
            WHERE title LIKE '%""" + MySQLdb.escape_string(truncate_brackets(title)) + """%'
            AND MATCH (
            creator, contributor
            )
            AGAINST (
            '""" + MySQLdb.escape_string(contrib)+ """'
            );"""
            
            print "00000000000000000000000000000000000"
            print sqlsearch
            print book.Title
            print contrib
            print "00000000000000000000000000000000000"
            db = connect_to_database("amazon", "root", "gitkotwg0")
            cursor = db.cursor()
            cursor.execute(sqlsearch)
            result = cursor.fetchone()
            if result:
                out_result = result
                break
        if out_result:
            pg_books.append((book.Title, result, book.ASIN))
            cursor.execute("UPDATE `amazon`.`book` SET `ASIN` = '" + MySQLdb.escape_string(book.ASIN)+"' WHERE CONVERT( `book`.`id` USING utf8 ) = '"+ MySQLdb.escape_string(out_result[0]) +"'")
        else:
            pg_books.append((book.Title, None, None))            
    return pg_books


def pg_search(title):
    sqlquery = """SELECT DISTINCT `id`, `title` , `creator` , `contributor`
    FROM `book`
    WHERE MATCH (
    title, friendly_title
    )
    AGAINST (
    '""" + MySQLdb.escape_string(title) + """'
    )
    """
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
        else:
            books[id] = {'title': title, 'creator' : [], 'contributor' : []}
            if creator:
                books[id]['creator'].append(creator)
            if contributor:
                books[id]['contributor'].append(contributor)
    
    return books

def group_searches(title, page):
    books = amazon_search(title)
    pg_books = get_pg_books(books, page)
    return pg_books

for k,v in pg_search("beowulf").iteritems():
    print k + ": " + str(v)