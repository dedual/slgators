from parserdf import *
import MySQLdb

def connect_to_database(databasename, usr, password):
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db


def insert(statement):
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    cursor.execute(statement)
    db.close
    


root  = getRoot("/home/ghais/public_html/cgi-bin/cata.rdf")
for etext in root.getiterator(pgterms + "etext"):
    b = Book()
    setID(etext, b)
    for node in etext.getchildren():
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

    
