import linecache

nlines = 20
nchars = 60
current_line = 0
f = open("http://www.gutenberg.org/files/20417/20417.txt")

linecache.getline(
