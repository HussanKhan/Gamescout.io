from CDKeysDeals import CDKEYSDEALS
import json
# import urllib.request
# from urllib.request import Request, urlopen
# from shutil import copyfileobj
def CDJSON():

    array = CDKEYSDEALS()

    with open("CDKeys_DEALS.json", "w") as newfile:
        json.dump({"CDKeys": array}, newfile)
#
# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
#
# url = "https://www.cdkeys.com/media/catalog/product/cache/1/small_image/295x395/9df78eab33525d08d6e5fb8d27136e95/b/a/battlefield_1_cover.jpg"
#
# req = Request(url, headers=header)
#
# with urlopen(req) as in_stream, open("static/images/CDKEYS/" + "test" + ".jpg", 'wb') as out_file:
#     copyfileobj(in_stream, out_file)
