import MySQLdb

def remove_newline(s):
    return s.replace("\n", " ") 

class Book(object):
    def __init__(self):
        self._id = ""
        self._title = ['NULL']
        self._friendly_title = ['NULL']
        self._language = ['NULL']
        self._creator= ['NULL']
        self._contributor = ['NULL']
        self._subject = ['NULL']
        self._publisher = "NULL"
        self._translator = ['NULL']
        self._isbn = 000000000
        self.switch = True
    
    def getISBN(self):
        return self._isbn
    
    def setISBN(self, isbn):
        self._isbn = isbn
        
    
    def getTitle(self):
        return self._title
    
    def setTitle(self, title):
        self._title = title
    
    def addTitle(self, title):
        if self._title[0] == 'NULL':
            self._title[0] = title
        else:
            self._title.append(title)
    
    def getFriendlyTitle(self):
        return self._friendly_title
    
    def addFriendlyTitle(self, ftitle):
        if self._friendly_title[0] == 'NULL':
            self._friendly_title[0] = ftitle
        else:
            self._friendly_title.append(ftitle)
        
    def setFriendlyTitle(self, ftitle):
        self._friendly_title = ftitle
    
    def getLanguage(self):
        return self._language
    
    def setLanguage(self, language):
        self._language = language
    
    def addLanguage(self, language):
        if self._language[0] == 'NULL':
            self._language[0] = language
        else:
            self._language.append(language)
    
    def getCreator(self):
        return self._creator

    def setCreator(self, creator):
        self._creator = creator
    
    def addCreator(self, creator):
        if self._creator[0] == 'NULL':
            self._creator[0] = creator
        else:
            self._creator.append(creator)
    
    def getTranslator(self):
        return self._translator

    def setTranslator(self, translator):
        self._translator = translator
    
    def addTranslator(self, translator):
        if self._translator[0] == 'NULL':
            self._translator[0] = translator
        else:
            self._translator.append(translator)
    
    def getContributor(self):
        return self._contributor
    
    def setContributor(self, contributor):
        self._contributor = contributor
        
    def addContributor(self, contributor):
        if self._contributor[0] == 'NULL':
            self._contributor[0] = contributor
        else:
            self._contributor.append(contributor)

        
    def getSubject(self):
        return self._subject
    
    def setSubject(self, subject):
        self._subject = subject
        
    def addSubject(self, subject):
        if self._subject[0] == 'NULL':
            self._subject[0] = subject
        else:
            self._subject.append(subject)
    
    def getPublisher(self):
        return self._publisher
    
    def setPublisher(self, publisher):
        self._publisher = publisher
        
    def getID(self):
        return self._id
    
    def setID(self, id):
        self._id = id
    
    def __str__(self):
        header = """INSERT INTO `amazon`.`book` (
        `id` ,
        `isbn` ,
        `title` ,
        `friendly_title` ,
        `creator` ,
        `contributor` ,
        `language` ,
        `subject` ,
        `publisher`
        )
        VALUES ("""
        
        tail = ');\n'
        id = self.getID()
        isbn = self.getISBN()
        pub = self.getPublisher()
        result = ""
        for title in self.getTitle():
            for ftitle in self.getFriendlyTitle():
                for creator in self.getCreator():
                    for contrib in self.getContributor():
                        for lang in self.getLanguage():
                            for sub in self.getSubject():
                                result = result + header
                                result = result + "'" + id      + "'," + str(isbn)  + ","
                                result = result + "'" + title   + "'," + "'" + ftitle     + "'," 
                                result = result + "'" + creator + "'," + "'" + contrib    + "'," 
                                result = result + "'" + lang    + "'," + "'" + sub        + "'," + "'" + pub + "'" 
                                result = result + tail
        return result
        
    def sqliterator(self):
        header = """INSERT INTO `amazon`.`book` (
        `id` ,
        `isbn` ,
        `title` ,
        `friendly_title` ,
        `creator` ,
        `contributor` ,
        `language` ,
        `subject` ,
        `publisher`
        )
        VALUES ("""
        
        tail = ');\n'
        id = self.getID()
        isbn = self.getISBN()
        pub = self.getPublisher()
        result = ""
        if self.switch:
            for title in self.getTitle():
                for ftitle in self.getFriendlyTitle():
                    for creator in self.getCreator():
                        for contrib in self.getContributor():
                            for lang in self.getLanguage():
                                for sub in self.getSubject():
                                    result = result + header
                                    result = result + "'" + id                             + "'," + str(isbn)  + ","
                                    result = result + "'" + MySQLdb.escape_string(remove_newline(title))   + "'," + "'" + MySQLdb.escape_string(remove_newline(ftitle))     + "'," 
                                    result = result + "'" + MySQLdb.escape_string(remove_newline(creator)) + "'," + "'" + MySQLdb.escape_string(remove_newline(contrib))    + "'," 
                                    result = result + "'" + MySQLdb.escape_string(remove_newline(lang))    + "'," + "'" + MySQLdb.escape_string(remove_newline(sub))        + "'," + "'" + MySQLdb.escape_string(remove_newline(pub)) + "'" 
                                    result = result + tail
                                    yield result
