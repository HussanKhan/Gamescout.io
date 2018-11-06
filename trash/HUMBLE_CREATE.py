from HumbleDeals import HumbleBundle
import json

def HUMBLEJSON():

    instance = HumbleBundle()
    array = instance.humble_parse()

    with open("HumbleBundle_DEALS.json", "w") as newfile:
        json.dump({"HumbleBundle": array}, newfile)
