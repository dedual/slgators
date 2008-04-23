#from pg import top100
from amazon import amazon_review
from amazon import amazon_search
from pyaws import ecs
import os
import urllib2 
import re 

license_key = '0ZW74MMABE2VX9H26182'

def amazon_get_image(ASIN, size="LargeImage"):
    images = []
    ecs.setLicenseKey(license_key)
    result = ecs.ItemLookup(ASIN, ResponseGroup = "Images")
    for item in result:
        try:
            images.append(item.LargeImage.URL)
        except AttributeError:
            images.append("None")
    return images

def get_images():
    etextids = get_book_ids()
    for etextid in etextids.iterkeys():
        asin = amazon_search.get_ASIN(etextid)
        if (asin != "None") and (asin != None):
            #print asin
            url = amazon_get_image(asin)[0]
            if url != 'None':
                os.system("wget -c " + url + " -O " + etextid + ".jpg")



def get_book_ids():
    url = "http://www.gutenberg.org/browse/scores/top/"
    f = urllib2.urlopen(url)
    pattern = '(<li><a href="/etext/)(.*)(">.*</li>)'
    r = re.compile(pattern)
    etextids = {}
    for line in f:
        m = r.match(line)
        if m:
            etextids[m.group(2)] = True
    return etextids

get_images()