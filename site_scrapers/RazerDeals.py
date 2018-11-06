#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/VgApp/vgdeals_production/")

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import urllib
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_create.database_generation import Games
from sqlalchemy.ext.declarative import declarative_base
from selenium.webdriver import FirefoxOptions

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

class Razer():

    def __init__ (self):
        self.page = 0

    # Retrieves formatted html to scrape
    def grab_page(self, request_url):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)

        driver.get(request_url)
        print("RZ: Request Sent")

        WebDriverWait(driver, 40)
        html = driver.page_source
        driver.close()

        parsed_content = soup(html, 'lxml')

        return parsed_content

    def razer_parse(self):
        print("RZ: Page {}".format(self.page))

        request_url =  "https://gamestore.razer.com/home.html"

        parsed_content = self.grab_page(request_url)

        # Find Every game
        item_container = parsed_content.findAll("li")

        for game in item_container:
            try:
                if game.find("div", {"class": "price-old"}) is None:
                    print("RZ: Not on sale")
                else:
                    title = game.find("h5", {"class": "title"}).text
                    price = game.find("div", {"class": "price-current"}).text
                    price = str(price.replace(u"\u00AD", ""))

                    game_url = game.find("a").get("href")

                    url = "http://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx{}".format(game_url)

                    attr = Games(title=title + " " + "PC", price=price, genre="Other", image="none", source="Razer Gamestore", buy_link=url)
                    session.add(attr)
                    session.commit()

                print("RZ: FILLING DATABASE...")
            except Exception:
                print("RZ: Error getting game")

        return 0
