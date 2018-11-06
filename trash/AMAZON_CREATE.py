from AmazonDeals import AmazonGames
import json

def AMAZONJSON():
    #
    amazon = AmazonGames()
    # amazon.database(1)
    array = []

    amazon.parse_data(array)

    with open("Amazon_DEALS.json", "w") as newfile:
        json.dump({"Amazon": array}, newfile)
