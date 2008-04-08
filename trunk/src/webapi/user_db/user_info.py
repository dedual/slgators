from _mysql_exceptions import MySQLError
import MySQLdb

def connect_to_database(databasename, usr, password):
    """ Connects to a database using usr and password"""
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db

def check_usr(fname, lname):
    """Given a first name and a last name, it checks weather the user exists in the database"""
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()
    assert(isinstance(cursor, MySQLdb.cursors.Cursor))
    cursor.execute("SELECT fname, lname FROM user WHERE(fname = '" + fname + "'AND lname= '" + lname + "');");
    result = cursor.fetchone()
    db.close()
    if result:
        return True
    else:
        return False

def fetch_user_bookmarks(fname, lname, bookid = None):
    """Given a first name, and a last name it returns the tupple containing bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page from the database"""
    db = connect_to_database("amazon", "root", "password-here")    #replace with password
    cursor = db.cursor()
    sql_query = ""
    if bookid:
        sql_query = ("""SELECT DISTINCT bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page
        FROM book, bookmark
        WHERE bookmark.fname = '""" + MySQLdb.escape_string(fname) + """'
        AND bookmark.lname = '"""   + MySQLdb.escape_string(lname) + """'
        AND bookmark.bookid = '""" + MySQLdb.escape_string(bookid) + """'
        AND bookmark.bookid = book.id;""")
    else:
        sql_query = ("""SELECT DISTINCT bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page
        FROM book, bookmark
        WHERE bookmark.fname = '""" + MySQLdb.escape_string(fname) + """'
        AND bookmark.lname = '"""   + MySQLdb.escape_string(lname) + """'
        AND bookmark.bookid = book.id;""")
        
    cursor.execute(sql_query)
    result = cursor.fetchall()
    db.close()
    return result

def fetch_all_bookmarks(fname, lname, bookid = None, page = None):
    if page:
        start = (page - 1) * 25
        end = 25
        db = connect_to_database("amazon", "root", "gitkotwg0")
        cursor = db.cursor()
        sql_query = ""
        if bookid:
            sql_query = ("""SELECT DISTINCT bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page
            FROM book, bookmark
            WHERE bookmark.fname = '""" + MySQLdb.escape_string(fname) + """'
            AND bookmark.lname = '"""   + MySQLdb.escape_string(lname) + """'
            AND bookmark.bookid = '""" + MySQLdb.escape_string(bookid) + """' 
            AND bookmark.bookid = book.id LIMIT """ + MySQLdb.escape_string(str(start)) + """,""" + MySQLdb.escape_string(str(end)) + """ ;""")
        else:
            sql_query = ("""SELECT DISTINCT bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page
            FROM book, bookmark
            WHERE bookmark.fname = '""" + fname + """'
            AND bookmark.lname = '"""   + lname + """'
            AND bookmark.bookid = book.id LIMIT """ + str(start) + """,""" + str(end) + """ ;""")
            
        cursor.execute(sql_query)
        result = cursor.fetchall()
        db.close()
        return result
    else:
        return fetch_user_bookmarks(fname, lname, bookid)


def add_user(fname, lname):
    """Given a first name and a last name, this functions inserts a new user into the database and associates him with the empty bookmark"""
    if check_usr(fname, lname):         #User already in database
        pass
    else:                               #Insert user
        db = connect_to_database("amazon", "root", "gitkotwg0")
        cursor = db.cursor()
        assert(isinstance(cursor, MySQLdb.cursors.Cursor))
        cursor.execute("""INSERT INTO `amazon`.`user` (
        `fname` ,
        `lname` ,
        `languag`
        ) 
        VALUES ('""" + MySQLdb.escape_string(fname) + "', '" + MySQLdb.escape_string(lname) + """', 'en'
        );""")
        db.close()
        
        
def add_bookmark(fname, lname,  bookmarkname, bookid, page):
    
    if check_usr(fname, lname):
        sql_query = """INSERT INTO `amazon`.`bookmark` (
        `id` ,
        `fname` ,
        `lname` ,
        `name` ,
        `bookid` ,
        `page` ,
        `misc`
        )
        VALUES (
                NULL , '""" + MySQLdb.escape_string(fname) + """', '""" + MySQLdb.escape_string(lname) + """', '""" + MySQLdb.escape_string(bookmarkname) + """', '""" + MySQLdb.escape_string(bookid) +"""', '""" + MySQLdb.escape_string(page) + """', NULL
                );"""
        db = connect_to_database("amazon", "root", "gitkotwg0")
        cursor = db.cursor()
        assert(isinstance(cursor, MySQLdb.cursors.Cursor))
        try:
            cursor.execute(sql_query)
            db.close()
            print 1
        except MySQLError:
            print "MySQL error"        #indicates mysql error
    else:
        print "User doesn't exist"     #indicates user doesn't exist



