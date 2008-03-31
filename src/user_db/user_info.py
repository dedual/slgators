import MySQLdb

def connect_to_database(databasename, usr, password):
    """ Connects to a database using usr and password"""
    db = MySQLdb.connect(host="localhost", user=usr, passwd=password, db=databasename)
    return db

def check_usr(fname, lname):
    """Given a first name and a last name, it checks weather the user exists in the database
    If not it returns Null otherwise it returns (fname, lname) as fetche from the database"""
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



def fetch_user_bookmarks(fname, lname):
    """Given a first name, and a last name it returns the tupple containing bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page from the database"""
    db = connect_to_database("amazon", "root", "gitkotwg0")
    cursor = db.cursor()

    sql_query = ("""SELECT DISTINCT bookmark.id, bookmark.name, book.title, book.UUID, bookmark.page
    FROM book, bookmark
    WHERE bookmark.fname = '""" + fname + """'
    AND bookmark.lname = '"""   + lname + """'
    AND bookmark.bookid = book.id;""")
    
    cursor.execute(sql_query)
    result = cursor.fetchall()
    db.close()
    return result

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
        VALUES ('""" + fname + "', '" + lname + """', 'en'
        );""")
        db.close()
    
