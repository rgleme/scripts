from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import sqlite3
import requests

class TestFlask(unittest.TestCase):

    def test_web_app_running(self):
        try:
             r = requests.get("http://127.0.0.1:5000/")
        except:
            self.fail("Could not open web app. Not running, or crashed. Test Failed")


    def test_home(self):

        r = requests.get("http://127.0.0.1:5000/")
        page_src = r.text

        if page_src.find("TWITTER API") < 0:
            self.fail("Home not working")


    def test_top_users(self):
        r = requests.get("http://127.0.0.1:5000/top_users")
        page_src = r.text

        if page_src.find('Most Popular Users and Followers Count') < 0:
            self.fail("Top Users failed")

    def test_lang(self):
        r = requests.get("http://127.0.0.1:5000/search_tweets")
        page_src = r.text

        if page_src.find('Top Tweets by Languages and Tags') < 0:
            self.fail("Search Twitters by Languages failed")

    def test_hour(self):
        r = requests.get("http://127.0.0.1:5000/tweets_by_hour")
        page_src = r.text

        if page_src.find('All tweets grouped by hour') < 0:
            self.fail("Search Twitters by Hour failed")        

if __name__ == "__main__":
    unittest.main()