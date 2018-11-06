# Starting link
# https://www.gamestop.com/browse/pc?nav=2b6,28-xu0,13a-8c-162
# https://www.gamestop.com/browse/pc?nav=2b12,28-xu0,13a-8c-162
# https://www.gamestop.com/browse/pc?nav=2b24,28-xu0,13a-8c-162
# https://www.gamestop.com/browse/pc?nav=2b36,28-xu0,13a-8c-162

# USE 2b INCREMTN BY + 12 after first 6 increment

# Format for linkshare
# https://click.linksynergy.com/deeplink?id=Kkv1tcDJ/BU&mid=24348&murl=URLHERE
# https://click.linksynergy.com/deeplink?id=Kkv1tcDJ/BU&mid=24348&murl=URLHERE

# List of products
# List class="products"

# each product = class="product digital_product"
            # title = class="product_info grid_12"
              # a contains title and link class="ats-product-title-lnk"

            # contains price class="purchase_info grid_6 omega"
                # p tag class="pricing ats-product-price" contains price

# nUMBER OF PAGES INFO
# div class="pagination_controls"
# get second strong
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

class GameStop():

    def __init__ (self):
        self.page = 0

    # Retrieves formatted html to scrape
    def grab_page(self, request_url):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)

        driver.get(request_url)

        print("GS: Request Sent")

        WebDriverWait(driver, 40)
        html = driver.page_source
        driver.close()

        parsed_content = soup(html, 'lxml')

        return parsed_content

    # Need to know how many times to crawl site, and see how many pages
    def get_pagecount(self, page):
        request_url = page

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)

        driver.get(request_url)

        WebDriverWait(driver, 40)

        html = driver.page_source

        driver.close()

        parsed_content = soup(html, 'lxml')

        # Find how many pages
        number_pages = parsed_content.findAll("a", {"class": "next_page"})
        number_pages = number_pages[1].get("href")
        number_pages = number_pages.split('2b')[1]
        # [/browse/pc?nav=, 36,28-xu0,13a-8c-162]
        number_pages = number_pages[:2]
        number_pages = int((int(number_pages) / 12) + 1)

        return number_pages

    def gamestop_parse_teen(self):
        game_list = []

        page_total = self.get_pagecount("https://www.gamestop.com/browse?nav=2b6,28-xu0,13162-4f-34")

        for i in range(1, int(page_total + 1)):
            print("GS: Page {}".format(self.page))

            if self.page == 0:
                request_url = "https://www.gamestop.com/browse?nav=2b6,28-xu0,13162-4f-34"
            else:
                request_url = "https://www.gamestop.com/browse?nav=2b{},28-xu0,13162-4f-34".format(self.page)

            parsed_content = self.grab_page(request_url)

            # Find Every game
            item_container = parsed_content.findAll("div", {"class": "product new_product"})

            for game in item_container:
                try:
                    title = game.find("a", {"class": "ats-product-title-lnk"}).text
                    plat = game.find("h3", {"class": "ats-product-title"})
                    plat = plat.find("strong").text
                    price = game.find("p", {"class": "pricing ats-product-price"}).text
                    price = price.split('$')[2]
                    price = "$" + price

                    game_url = "https://www.gamestop.com" + game.find("a", {"class": "ats-product-title-lnk"}).get("href")

                    url = "https://click.linksynergy.com/deeplink?id=Kkv1tcDJ/BU&mid=24348&murl={}".format(game_url)

                    attr = Games(title=title + " " + plat, price=price, genre="Other", image="none", source="GameStop", buy_link=url)
                    session.add(attr)
                    session.commit()

                    print("GS: FILLING DATABASE...")
                except Exception:
                    print("GS: Error getting game")

            print("GS: Request Cooldown - 10s")
            time.sleep(10)

            self.page = self.page + 12

    def gamestop_parse(self):
        game_list = []

        page_total = self.get_pagecount("https://www.gamestop.com/browse?nav=2b6,28-xu0,13162-4f-35")

        for i in range(1, int(page_total + 1)):
            print("GS: Page {}".format(self.page))

            if self.page == 0:
                request_url = "https://www.gamestop.com/browse?nav=2b6,28-xu0,13162-4f-35"
            else:
                request_url = "https://www.gamestop.com/browse?nav=2b{},28-xu0,13162-4f-35".format(self.page)

            parsed_content = self.grab_page(request_url)

            # Find Every game
            item_container = parsed_content.findAll("div", {"class": "product new_product"})

            for game in item_container:
                try:
                    title = game.find("a", {"class": "ats-product-title-lnk"}).text
                    plat = game.find("h3", {"class": "ats-product-title"})
                    plat = plat.find("strong").text
                    price = game.find("p", {"class": "pricing ats-product-price"}).text
                    price = price.split('$')[2]
                    price = "$" + price

                    game_url = "https://www.gamestop.com" + game.find("a", {"class": "ats-product-title-lnk"}).get("href")

                    url = "https://click.linksynergy.com/deeplink?id=Kkv1tcDJ/BU&mid=24348&murl={}".format(game_url)

                    attr = Games(title=title + " " + plat, price=price, genre="Other", image="none", source="GameStop", buy_link=url)
                    session.add(attr)
                    session.commit()

                    print("GS: FILLING DATABASE...")
                except Exception:
                    print("GS: Error getting game")

            print("GS: Request Cooldown - 20s")
            time.sleep(10)

            self.page = self.page + 12
        self.page = 0
        self.gamestop_parse_teen()
