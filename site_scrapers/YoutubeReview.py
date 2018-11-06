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
from selenium.webdriver import FirefoxOptions
from random import randint

class YoutubeSearch():
    """This class takes a phrase, and find a relvent youtube video link"""

    def __init__(self):
        # Object used in loops so wait
        self.wait = randint(2, 6)

    def search(self, keyword):
        # wait before search
        time.sleep(self.wait)

        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=opts)

        # Creates url from keyword
        url = "https://www.youtube.com/results?search_query=" + keyword.replace(' ', "%20")

        # Adds url to searchbar
        driver.get(url)

        # Pure html from loaded page
        html = driver.page_source

        # Parses html
        parsed = soup(html, 'lxml')

        driver.close()


        # Searches all videos on page
        review_link = parsed.findAll('a', {"class": "yt-simple-endpoint style-scope ytd-video-renderer"})

        vid_id = ""

        # Returns first valid vidoe ulr found
        for i in review_link:
            link = i.get("href")
            if link is not None:
                vid_id = link
                break

        # Forms valid link
        review_link = "https://www.youtube.com" + vid_id

        # changes wait time for next inter
        self.wait = randint(2, 6)

        return review_link
