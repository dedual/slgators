#!/usr/bin/env python

import MySQLdb
from pyaws import ecs



    
def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db

def amazon_search(title):
    ecs.setLicenseKey('0ZW74MMABE2VX9H26182')
    books = ecs.ItemSearch(title, SearchIndex='Books',Sort='relevancerank')
    return books


def get_pg_books(books, page):
    pg_books = []
    for i in range((page - 1 )* 10, page * 10):
        book = books[i]
        sqlsearch= """SELECT DISTINCT `id` FROM `book` WHERE `title` LIKE CONVERT( _utf8 '""" + MySQLdb.escape_string(book.Title) + """' USING latin1 ) COLLATE latin1_swedish_ci LIMIT 0 , 30;"""
        db = connect_to_database("amazon", "root", "gitkotwg0")
        cursor = db.cursor()
        assert(isinstance(cursor, MySQLdb.cursors.Cursor))
        cursor.execute(sqlsearch)
        result = cursor.fetchone()
        if result:
            pg_books.append( (book.Title, result))
        else:
            pg_books.append( (book.Title, None))            
    return pg_books


def group_searches(title):
    books = amazon_search(title)
    pg_books = get_pg_books(books)
    return pg_books


