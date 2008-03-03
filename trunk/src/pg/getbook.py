import re
import urllib2
import StringIO
import os
def geturl(textid):
    r = re.compile('(\d+)')
    match = r.search(textid)
    url = "http://www.gutenberg.org/files/" + match.group() + "/" + match.group() + ".txt"
    return url


def getBook(textid):
    url = geturl(textid)
    if os.path.isfile('books/' + textid):
        f = open('books/' + textid)
    else:
        os.system('wget -c ' + url + ' -O books/' + textid)
        f = open('books/' + textid)
    return f



def getpage(pagen, f, nchars=75, nlines=10):
    r = re.compile('\s')
    if pagen == 1:
        lines = f.read(nchars * nlines)
        if r.match(lines[-1]):
            return lines
        else:
            for i in range(nchars):
                if r.match(lines[i * -1]):
                    return lines[: i * -1]
    else:
        f.seek(nchars * nlines * (pagen - 1))
        c = f.read(1)
        if r.match(c):
            lines  = f.read(nchars * nlines)
            if r.match(lines[-1]):
                return lines
            else:
                for i in range(1, nchars):
                    if r.match(lines[i * -1]):
                        return lines[: i * -1]
        else:
            current = f.tell()
            for i in range(nchars):
                f.seek(current - i)
                if r.match(f.read(1)):
                    lines  = f.read(nchars * nlines)
                    if r.match(lines[-1]):
                        return lines
                    else:
                        for i in range(nchars):
                            if r.match(lines[i * -1]):
                                return lines[: i * -1]

f = getBook('etext76')                            
print getpage(2, f)
            




