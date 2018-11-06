from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time
from selenium.webdriver import FirefoxOptions
from random import randint
import os




class Review():
    """This class takes a game name and returns the metacritic reviews"""

    def __init__(self):
        # Object used in loops so wait
        self.wait = randint(2, 6)
        self.rev_arr = []

    def make_req(self, url):
        # wait before search
        time.sleep(self.wait)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

        # Pure html from loaded page
        html = requests.get(url, headers=headers)

        html = html.content

        # Parses html
        parsed = soup(html, 'lxml')

        # changes wait time for next inter
        self.wait = randint(2, 6)

        return parsed

    def parse_page(self, parsed, deepname, u):
        user_reviews = parsed.findAll('div', {"class": "review_body"})

        self.rev_arr = []
        self.rev_arr.append(deepname)
        self.rev_arr.append(u)

        for rev in user_reviews:
            if len(self.rev_arr) > 5:
                break
            try:
                rev_text = rev.find("span", {"class": "blurb blurb_collapsed"}).text
            except Exception:
                try:
                    rev_text = rev.find("span").text
                except Exception:
                    rev_text = ""
                    pass

            rev_text = rev_text.replace("\r", "")
            rev_text = rev_text.replace("Expand", "")


            self.rev_arr.append(rev_text)

        if len(self.rev_arr) > 2:
            return self.rev_arr
        else:
            return False

    def search(self, keyword):
        deepname = keyword

        keyword = keyword.lower()
        keyword = keyword.replace(":", "")
        keyword = keyword.replace("'", "")
        keyword = keyword.replace("-", " ")
        keyword = keyword.replace("&", "")
        keyword = keyword.replace("~", "")
        keyword = keyword.replace(".", "")
        keyword = keyword.replace("  ", "-")
        keyword = keyword.replace("   ", "-")
        keyword = keyword.replace(" ", "-")

        # Creates url from keyword
        url_ps4 = "http://www.metacritic.com/game/playstation-4/{}/user-reviews".format(keyword)
        url_pc = "http://www.metacritic.com/game/pc/{}/user-reviews".format(keyword)
        url_one = "http://www.metacritic.com/game/xbox-one/{}/user-reviews".format(keyword)
        url_switch = "http://www.metacritic.com/game/switch/{}/user-reviews".format(keyword)

        all_urls = [url_pc, url_ps4, url_switch, url_one]

        for u in all_urls:
            parsed = self.make_req(u)

            content = self.parse_page(parsed, deepname, u)

            if content:
                print("REVIEW FOUND {}".format(u))
                break

        if len(self.rev_arr) > 2:
            print("GOT VALID REVIEW")
            return self.rev_arr
        else:
            return False
