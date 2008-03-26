from pyaws import ecs
from _xmlplus.dom import html
import re

license_key = '0ZW74MMABE2VX9H26182'

p = re.compile('(<p.*?>)|(<tr.*?>)', re.I)
t = re.compile('<td.*?>', re.I)
comm = re.compile('<!--.*?-->', re.M)
tags = re.compile('<.*?>', re.M)

def html2txt(s, hint = 'entity', code = 'ISO-8859-1'):
    """Convert the html to raw txt
    - suppress all return
    - <p>, <tr> to return
    - <td> to tab
    Need the foolwing regex:
    p = re.compile('(<p.*?>)|(<tr.*?>)', re.I)
    t = re.compile('<td.*?>', re.I)
    comm = re.compile('<!--.*?-->', re.M)
    tags = re.compile('<.*?>', re.M)
    version 0.0.1 20020930
    """
    s = s.replace('\n', '') # remove returns time this compare to split filter join
    s = p.sub('\n', s) # replace p and tr by \n
    s = t.sub('\t', s) # replace td by \t
    s = comm.sub('', s) # remove comments
    s = tags.sub('', s) # remove all remaining tags
    s = re.sub(' +', ' ', s) # remove running spaces this remove the \n and \t
    # handling of entities
    result = s
    pass
    return result



def amazon_editorial_review(ASIN):
    editorials = []
    ecs.setLicenseKey(license_key)
    result = ecs.ItemLookup(ASIN, ResponseGroup = "EditorialReview")
    for review in result:
        try:
            for editorial_review in review.EditorialReviews:
                editorials.append((editorial_review.Rating, html2txt(editorial_review.Summary), html2txt(editorial_review.Content)))
        except TypeError:
            editorials.append(html2txt(review.EditorialReviews.EditorialReview.Content))
    return editorials
        

def amazon_customer_review(ASIN):
    reviews = []
    ecs.setLicenseKey(license_key)
    result = ecs.ItemLookup(ASIN, ResponseGroup = "Reviews")
    for review in result[0].CustomerReviews.Review:
        reviews.append((review.Rating, html2txt(review.Summary), html2txt(review.Content)))
    return reviews

def amazon_get_image(ASIN, size="LargeImage"):
    images = []
    ecs.setLicenseKey(license_key)
    result = ecs.ItemLookup(ASIN, ResponseGroup = "Images")
    for item in result:
        images.append(item.LargeImage.URL)
    return images
        
        

def amazon_similarities(ASIN):
    similarities = []
    ecs.setLicenseKey(license_key)
    result = ecs.ItemLookup(ASIN, ResponseGroup = "Similarities")
    for item in result:
        for product in item.SimilarProducts.SimilarProduct:
            similarities.append((product.Title, product.ASIN))
    return similarities


a = amazon_similarities("0307266931")
#for item in a:
#    print item 
    