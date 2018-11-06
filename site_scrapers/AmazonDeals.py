#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/VgApp/vgdeals_production/")

import  base64, datetime, hashlib, hmac, urllib
import requests
import webbrowser
from bs4 import BeautifulSoup
import urllib.request
from flask import url_for
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_create.database_generation import Games
from sqlalchemy.ext.declarative import declarative_base
import json

# Creates handler
Base = declarative_base()
# creates engine
engine = create_engine('sqlite:///gamedeals.db')

# Combines handler and engine
Base.metadata.bind = engine

# Creates a unique session
DBSession = sessionmaker(bind=engine)

# Activating session
session = DBSession()

# Before starting delete all contents of database
class AmazonGames():

    def __init__(self):
        self.page = 1
        pass

    def database(self, page, term):
        # Creating timestamp
        timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()

        endparas = "AWSAccessKeyId=xxxxxxxxxxxxxxxxxxxxxxxxxxx&AssociateTag=xxxxxxxxxxxxx&ItemPage=" + str(page) +"&Keywords=" + term + "&MinPercentageOff=10&Operation=ItemSearch&ResponseGroup=Large%2COffers&SearchIndex=VideoGames&Service=AWSECommerceService&Timestamp={}Z".format(timestamp)

        # Removing colons
        endparas = endparas.replace(":", "%3A")

        # Making string that will be used to hash secret key
        string_to_sign = "GET\n"
        string_to_sign += "webservices.amazon.com\n"
        string_to_sign += "/onca/xml\n"
        string_to_sign += endparas

        # Hash slinging slasher
        hash = hmac.new(b"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", msg=string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()

        # Coding signature in proper format
        signature = base64.b64encode(hash).decode()

        # Encoding signature to url
        signature = urllib.parse.quote_plus(signature)

        # Appending signature to request
        endparas += '&Signature=' + signature

        # Creating URL
        request_url = "http://webservices.amazon.com" + "/onca/xml" + "?" + endparas

        # webbrowser.open(request_url)
        r = urllib.request.urlopen(request_url)
        print("AMZN: REQUEST SENT")
        return r

    def parse_data(self):
        searchterms = ["video%20game%20pc", "video%20game%20ps4", "video%20game%20xbox%20one", "video%20game%20switch"]
        for term in searchterms:
            for i in range(1,11):
                print("AMZN: PAGE {}".format(self.page))
                r = self.database(self.page, term)
                xml = BeautifulSoup(r, 'xml')
                thing = xml.findAll('Item')
                for i in thing:
                    try:
                        pgroup = i.find('ProductGroup').text
                        if pgroup == "Digital Video Games" or pgroup == "Video Games":
                            # Digging for price
                            price = i.find('Offers')
                            price = price.find('Offer')
                            price = price.find('OfferListing')

                            price = price.find('Price')
                            price = price.find('FormattedPrice').text # Final Price

                            if price == "Too low to display":
                                price = "10% Off"

                            url = i.find('DetailPageURL').text # Url to buy product

                            title = i.find('Title').text

                            print("AMZN: FILLING DATABASE...")
                            try:
                                attr = Games(title=title, price=price, genre="Other", image="NONE", source="Amazon", buy_link=url)
                                session.add(attr)
                                session.commit()
                            except Exception:
                                attr = Games(title=title, price=price, genre="Other", image="NONE", source="Amazon", buy_link=url)
                                session.add(attr)
                                session.commit()
                                print('AMZN: Error Downloading Image')
                        else:
                            print("AMZN: Not Digital Game")

                    except Exception:
                        print("AMZN: Error Parsing XML")
                time.sleep(1)
                self.page = self.page + 1
            print("AMZN: term rest")
            self.page = 0
            time.sleep(1)
