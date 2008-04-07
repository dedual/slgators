from pg import top100
from amazon import amazon_review
from amazon import amazon_search
from pyaws import ecs
import os


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
    etextids = top100.get_top_books()
    for etextid in etextids:
        asin = amazon_search.get_ASIN(etextid)
        if (asin != "None") and (asin != None):
            #print asin
            url = amazon_get_image(asin)[0]
            if url != 'None':
                os.system("wget -c " + url + " -O " + etextid + ".jpg")



