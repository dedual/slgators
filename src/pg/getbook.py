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
    f = urllib2.urlopen(url)
    return StringIO.StringIO(f.read())



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





