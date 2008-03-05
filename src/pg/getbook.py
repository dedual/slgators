import re
import urllib2
import cStringIO
import os
import linecache 

def geturl(textid):
    r = re.compile('(\d+)')
    match = r.search(textid)
    url = "http://www.gutenberg.org/files/" + match.group() + "/" + match.group() + ".txt"
    return url


def getBook(textid, path='/tmp/'):
    if os.path.isfile(path + textid + ".txt"):
        return (path + textid + ".txt")
    url = geturl(textid)
    o = urllib2.urlopen(url)
    f = open(path + textid + ".txt", 'w')
    f.write(o.read())
    f.close()
    
    return (path + textid + ".txt")



def getlines(f, start, end, nchars=92):
    lines = ""
    pad = ''
    for i in range(start, end+1):
        line = linecache.getline(f, i).rstrip()
        line_len = len(line)
        if line_len < nchars:
            pad = '&nbsp' * (nchars - line_len)
        pad += '|'
        lines += line + pad
    #linecache.clearcache()
    return lines









