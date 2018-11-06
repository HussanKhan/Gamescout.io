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


class HumbleBundle():

    def __init__ (self):
        self.page = 0

    def grab_page(self, request_url):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)
        driver.get(request_url)
        print("HB: Request Sent")

        WebDriverWait(driver, 40)
        html = driver.page_source
        driver.close()

        parsed_content = soup(html, 'lxml')

        return parsed_content

    def get_pagecount(self):
        request_url = "https://www.humblebundle.com/store/search?sort=bestselling&filter=onsale"

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)

        driver.get(request_url)
        WebDriverWait(driver, 40)

        html = driver.page_source

        driver.close()

        parsed_content = soup(html, 'lxml')

        # Find how many pages
        number_pages = parsed_content.findAll("a", {"class": "js-grid-page grid-page"})
        number_pages = int(number_pages.pop().text)

        return number_pages


    def humble_parse(self):
        game_list = []

        # page_total = self.get_pagecount()
        #
        # if page_total > 50:
        #     page_total = 50

        for i in range(1, 11):
            print("HB: Page {}".format(self.page))
            if self.page == 0:
                request_url = "https://www.humblebundle.com/store/search?sort=bestselling&filter=onsale"
            else:
                request_url = "https://www.humblebundle.com/store/search?sort=bestselling&filter=onsale" + "&page=" + str(self.page)

            parsed_content = self.grab_page(request_url)

            # Find Every game
            item_container = parsed_content.findAll("li", {"class": "entity-block-container js-entity-container"})

            for game in item_container:
                try:
                    title = game.find("span", {"class": "entity-title "}).text
                    price = game.find("span", {"class": "price"}).text

                    url = "https://www.humblebundle.com" + game.find("a", {"class": "entity-link js-entity-link"}).get("href") + "?partner=xxxxxxxxxxxxxxxxx&charity=1379"

                    attr = Games(title=title, price=price, genre="Other", image="NONE", source="Humble Bundle", buy_link=url)
                    session.add(attr)
                    session.commit()

                    print("HB: FILLING DATABASE...")

                except Exception:
                    print("HB: Error getting game")

            print("HB: Request Cooldown - 30s")
            time.sleep(10)
            self.page = self.page + 1
        return game_list
