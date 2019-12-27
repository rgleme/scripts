import tweepy
from local_config import *
import sqlite3
from collections import Counter

db = "twitter.db"

class GetTwit():
    def __init__(self, hashtags, twit_numbers, conn):
        self.auth = tweepy.OAuthHandler(cons_tok, cons_sec)
        self.auth.set_access_token(app_tok, app_sec)
        self.twitter_api = tweepy.API(self.auth, wait_on_rate_limit=True)
        self.hashtags = hashtags
        self.twit_numbers = twit_numbers
        self.conn = conn
        self.c = self.conn.cursor()

    def config(self):        
        for var in self.hashtags:
            languages = []
            locations = []
            search_results = tweepy.Cursor(self.twitter_api.search, q = "#" + var, src = "typed_query", f = "live").items(self.twit_numbers)
            for result in search_results:
                print (result)       
                self.c.execute("insert into twit_data values('{0}','{1}','{2}','{3}','{4}','{5}')".format(result.user.screen_name, result.user.followers_count, result.lang, result.user.location, result.created_at, var))
                self.conn.commit()

if __name__ == "__main__":
    hashtags = ("openbanking","apifirst","devops","cloudfirst","microservices","apigateway","oauth","swagger","raml","openapis")
    twit_numbers = 100
    try:
        conn = sqlite3.connect(db)
        a = GetTwit(hashtags,twit_numbers,conn)
        a.config()
    except Exception as e:
        print(e)      
    finally:
        conn.close()
    