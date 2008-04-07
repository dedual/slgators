from xml.etree import ElementTree as ET
from book import *
import string


#########################
#Defining standard namespaces
#########################
rdf="{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
rdfs="{http://www.w3.org/2000/01/rdf-schema#}"
xsi="{http://www.w3.org/2001/XMLSchema-instance}"
dc="{http://purl.org/dc/elements/1.1/}"
dcterms="{http://purl.org/dc/terms/}"
dcmitype="{http://purl.org/dc/dcmitype/}"
cc="{http://web.resource.org/cc/}"
pgterms="{http://www.gutenberg.org/rdfterms/}"
base="{http://www.gutenberg.org/feeds/catalog.rdf}"





def getRoot(filename):
    parser = ET.parse(open(filename, 'r'))
    root  = parser.getroot()
    return root

def setID(etext, b):
    b.setID(etext.get(rdf + 'ID'))

def setPublisher(node, b):
    b.setPublisher(node.text.encode('latin-1', 'replace'))


def setTitle(node, b):
    if node.getchildren():
        for title in node.getiterator(rdf + 'li'):
            if title.text:
                b.addTitle(title.text.encode('latin-1', 'replace'))
    elif node.text:
        b.addTitle(node.text.encode('latin-1', 'replace'))


def setCreator(node, b):
    if node.getchildren():
        for creator in node.getiterator(rdf + 'li'):
            if creator.text:
                b.addCreator(creator.text.encode('latin-1', 'replace'))
    elif node.text:
        b.addCreator(node.text.encode('latin-1', 'replace'))
        
        
def setFriendlyTitle(node, b):
    if node.getchildren():
        for ftitle in node.getiterator(rdf + 'li'):
            if ftitle.text:
                b.addFriendlyTitl(ftitle.text.encode('latin-1', 'replace'))
    elif node.text:
        b.addFriendlyTitle(node.text.encode('latin-1', 'replace'))
    
    

def setContributor(node, b):
    if node.getchildren():
        for contributor in node.getiterator(rdf + 'li'):
            if contributor.text:
                b.addContributor(contributor.text.encode('latin-1', 'replace'))
    elif node.text:
        b.addContributor(node.text.encode('latin-1', 'replace'))
        
def setLanguage(node, b):
    if node.getiterator(rdf + 'li'):
        for language in node.getiterator(rdf + 'li'):
            for value in language.getiterator(rdf + 'value'):
                if value.text:
                    b.addLanguage(value.text.encode('latin-1', 'replace'))
    else:
        for value in node.getiterator(rdf + 'value'):
            if value.text:
                b.addLanguage(value.text.encode('latin-1', 'replace'))

def setSubject(node, b):
    if node.getiterator(rdf + 'li'):
        for subject in node.getiterator(rdf + 'li'):
            for value in subject.getiterator(rdf + 'value'):
                if value.text:
                    b.addSubject(value.text.encode('latin-1', 'replace'))
    else:
        for value in node.getiterator(rdf + 'value'):
            if value.text:
                b.addSubject(value.text.encode('latin-1', 'replace'))
                
def has_type(node, b):
    for type in node.getiterator(rdf + "value"):
        if type.text:
            return False
    return True
    

