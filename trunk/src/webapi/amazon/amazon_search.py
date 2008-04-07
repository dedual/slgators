#!/usr/bin/env python
import MySQLdb
import re
from pyaws import ecs
import string

def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db


def reverse_contrib(contributor):
    contributor = contributor.split(",")
    try:
        contributor[2] = contributor[2].split()[-1]
    except IndexError:
        contributor[1] = contributor[1].split()[-1]
    contributor.reverse()
    return [x.strip() for x in contributor]

def correct_contrib(contributor):
    contributor = reverse_contrib(contributor)
    contributor[1] += ' '
    contributor = "".join(contributor[1:])
    return  contributor

def get_ASIN(etextid):
    sql_query = """SELECT DISTINCT title, creator, contributor
     FROM book
     WHERE id = CONVERT( _utf8 '""" + etextid + "'USING latin1) COLLATE latin1_swedish_ci;"

    db = connect_to_database("amazon", "root", "gitkotwg0")
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
                return "None"
        else:
            try:
                ecs.setLicenseKey('0ZW74MMABE2VX9H26182')
                books = ecs.ItemSearch(Keywords = title, SearchIndex='Books', Sort='relevancerank')
                return books[0].ASIN
            except KeyError:
                return "None"
            except ecs.AWSException:
                return "None"
            except TypeError:
                return "None"
            


