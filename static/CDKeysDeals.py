# Append links with ?mw_aref=vgdealsio
# for best deals
# https://www.cdkeys.com/deals
from bs4 import BeautifulSoup as soup
import urllib

def CDKeyDeals():
    request_url = "https://www.cdkeys.com/deals"

    data = urllib.request.urlopen(request_url)
    content = soup(data, "lxml")
    data.close()

    cats = content.findAll("div", {"class": "category-products"})

    print(cats)
