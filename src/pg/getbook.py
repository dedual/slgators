import re
import urllib2
import cStringIO
import os
import linecache
import random;
import sys;


def geturl(textid):
    r = re.compile('(\d+)')
    match = r.search(textid)
    url = ""
    if match:
        url = "http://www.gutenberg.org/files/" + match.group() + "/" + match.group() + ".txt"
    return url


def get_alternate_url(textid):
    r = re.compile('(\d+)')
    match = r.search(textid)
    url = ""
    if match: 
        url = "http://www.gutenberg.org/etext/" + match.group()
    return url

def getBook(textid, path='/tmp/'):
    if os.path.isfile(path + textid + ".txt"):
        return (path + textid + ".txt")
    url = geturl(textid)
    if url:
        try:
            o = urllib2.urlopen(url)
            f = open(path + textid + ".txt", 'w')
            f.write(o.read())
            f.close()
        except urllib2.HTTPError:
            url = get_alternate_url(textid)
            pattern = '<a href="/dirs/(.*)\.txt" title="Download from ibiblio.org.">'
            p = re.compile(pattern)
            href_pattern = '<a href="(.*)" (.*)'
            p2 = re.compile(href_pattern)
            
            u = urllib2.urlopen(url)
            string = u.read()
            m= p.search(string)
            if m:
                href =  m.group()
                print url + p2.search(href).group(1)
                o = urllib2.urlopen("http://www.gutenberg.org" + p2.search(href).group(1))
                f = open(path + textid + ".txt", 'w')
                f.write(o.read())
                f.close()
            else:
                return ""
        return (path + textid + ".txt")



def getlines(f, start, end, nchars=92):
    lines = ""
    pad = ''
    for i in range(start, end+1):
        line = linecache.getline(f, i).rstrip()
        line_len = len(line)
        if line_len < nchars:
            pad = ' ' * (nchars - line_len)
        pad = pad + '|'
        lines = lines + line + pad
    return lines


f = getBook("etext928")






