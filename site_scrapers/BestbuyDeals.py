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


class BestBuy():

    def __init__ (self):
        self.page = 1

    def grab_page(self, request_url):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)
        driver.get(request_url)
        print("BB: Request Sent")

        WebDriverWait(driver, 40)
        html = driver.page_source
        driver.close()

        parsed_content = soup(html, 'lxml')

        return parsed_content

    def get_pagecount(self):
        request_url = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=pcmcat1487698928729&cp=1&id=pcat17071&iht=n&ks=960&list=y&qp=currentoffers_facet%3DCurrent%20Deals~On%20Sale&sc=Global&st=categoryid%24pcmcat1487698928729&type=page&usc=All%20Categories"

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)

        driver.get(request_url)
        WebDriverWait(driver, 40)

        html = driver.page_source

        driver.close()

        parsed_content = soup(html, 'lxml')

        # Find how many pages
        number_pages = parsed_content.findAll("li", {"class": "page-item"})
        number_pages = int(number_pages.pop().text)

        return number_pages


    def best_parse(self):
        game_list = []

        page_total = 4

        for i in range(1, (page_total+1)):
            print("BB: Page {}".format(self.page))

            request_url = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=pcmcat1487698928729&cp={}&id=pcat17071&iht=n&ks=960&list=y&qp=currentoffers_facet%3DCurrent%20Deals~On%20Sale&sc=Global&st=categoryid%24pcmcat1487698928729&type=page&usc=All%20Categories".format(self.page)

            parsed_content = self.grab_page(request_url)

            # Find Every game
            item_container = parsed_content.findAll("li", {"class": "sku-item"})

            for game in item_container:
                try:
                    title = game.find("h4", {"class": "sku-header"})

                    game_url = title.find("a").get("href")

                    title = title.find("a").text

                    price = game.find("div", {"class": "priceView-hero-price priceView-purchase-price"})
                    price = price.find("span").text

                    url = "https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&murl={}".format(game_url)

                    attr = Games(title=title, price=price, genre="Other", image="none", source="Best Buy", buy_link=url)
                    session.add(attr)
                    session.commit()

                    print("BB: FILLING DATABASE...")

                except Exception:
                    print("BB: Error getting game")

            print("BB: Request Cooldown - 10s")
            time.sleep(10)
            self.page = self.page + 1
        return game_list
