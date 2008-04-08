from parserdf import *
import MySQLdb
import re

def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db


def correct_title(title):
    pattern = ", Illustrated"
    p = re.compile(pattern)
    return p.sub("", title)


def convert_illustrated():
    db = connect_to_database("amazon", "root", "password-here")    #replace with password
    cursor = db.cursor()
    cursor.execute("select id,title, friendly_title from amazon.book where title like '%The Divine Comedy by Dante, Illustrated, %';")
    result = cursor.fetchall()
    for id, title, ftitle in result:
        print id
        cursor.execute("UPDATE `amazon`.`book` SET `title` = '" + 
                       MySQLdb.escape_string(correct_title(title)) + 
                       "',`friendly_title` = '" + 
                       MySQLdb.escape_string(correct_title(ftitle)) + 
                       "' WHERE  `book`.`id` = '" + id + "'; " )

def insert(statement):
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    cursor.execute(statement)
    db.close
    

def populatedb(xml_filename):
    root  = getRoot(xml_filename)
    for etext in root.getiterator(pgterms + "etext"):
        b = Book()
        setID(etext, b)
        for node in etext.getchildren():
            if node.tag == dc + 'type':
                b.switch = False
            if node.tag == dc + 'publisher':
                setPublisher(node, b)
            elif node.tag == dc + 'title':
                setTitle(node, b)
            elif node.tag == dc + 'creator':
                setCreator(node, b)
            elif node.tag == pgterms + 'friendlytitle':
                setFriendlyTitle(node, b)
            elif node.tag == dc + 'contributor':
                setContributor(node, b)
            elif node.tag == dc + 'language':
                setLanguage(node, b)
            elif node.tag == dc + 'subject':
                setSubject(node, b)
        for sql in b.sqliterator():
            insert(sql)
populatedb("/home/ghais/Documents/workspace/SLGators/data/cata.rdf")

        
        