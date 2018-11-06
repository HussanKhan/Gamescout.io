#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/VgApp/vgdeals_production/")

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.request
from urllib.request import Request, urlopen
import time
from shutil import copyfileobj
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

class CDKEYSDEALS():

    def __init__(self):
        self.page = ""

        self.request_url = "https://www.cdkeys.com/pc/games/l/worldwide"

    def parse_page(self):
        for i in range(1, 17):
            print("CD: Browser Opened")
            time.sleep(10)

            opts = FirefoxOptions()
            opts.add_argument("--headless")
            driver = webdriver.Firefox(firefox_options=opts)
            driver.get(self.request_url)

            WebDriverWait(driver, 60).until(EC.title_is("Origin Keys, Steam Keys, uPlay Keys, Battle.net Keys, Worldwide"))
            time.sleep(2)

            html = driver.page_source
            driver.close()

            parsed_content = soup(html, 'lxml')

            everygame = parsed_content.findAll("div", {"class": "col-6 col-sm-4 col-md-4 col-lg-4"})
            print("games found {}".format(len(everygame)))
            for game in everygame:
                try:
                    url1 = game.find("a")

                    title = url1.get("title")

                    url = url1.get("href") + "?mw_aref=vgdealsio"

                    price = game.find("span", {"class": "price"}).text

                    attr = Games(title=title, price=price, genre="Other", image="NONE", source="CDKeys", buy_link=url)
                    session.add(attr)
                    session.commit()

                    print("CD: {} {}".format(title, price))

                except Exception:
                    print("CD: FAILED TO GET GAME DATA")

            count = i + 1
            self.request_url = "https://www.cdkeys.com/pc/games/l/worldwide" + "/" + str(count)
