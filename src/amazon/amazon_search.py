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
        sqlsearch = """SELECT DISTINCT `id`, contributor FROM `book` WHERE `title` LIKE CONVERT( _utf8 '%""" + MySQLdb.escape_string(book.Title) + """%' USING latin1 ) COLLATE latin1_swedish_ci LIMIT 0 , 30;"""
        db = connect_to_database("amazon", "root", "gitkotwg0")
        cursor = db.cursor()
        assert(isinstance(cursor, MySQLdb.cursors.Cursor))
        cursor.execute(sqlsearch)
        result = cursor.fetchone()
        if result:
            pg_books.append((book.Title, result, book.ASIN))
            cursor.execute("UPDATE `amazon`.`book` SET `ASIN` = '" + MySQLdb.escape_string(book.ASIN)+"' WHERE CONVERT( `book`.`id` USING utf8 ) = '"+ MySQLdb.escape_string(result[0]) +"'")
        else:
            pg_books.append((book.Title, None, None))            
    return pg_books


def group_searches(title, page):
    books = amazon_search(title)
    pg_books = get_pg_books(books, page)
    return pg_books


#print group_searches("asdadasd", 1)
               


#amazon_search("Divine Comedy")
