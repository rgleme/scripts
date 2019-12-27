import unittest
import sqlite3
from twit import GetTwit

class TestTwit(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        c = self.conn.cursor()
        cmd = "CREATE TABLE twit_data (user TEXT, followers NUMBER, lang TEXT, location TEXT, datetime TEXT, hashtag TEXT)"
        c.execute(cmd)
        self.conn.commit()
        self.twit_numbers = 1
        self.hashtags ="devops"
        self.teste = GetTwit(self.hashtags,self.twit_numbers,self.conn)

    def test_db(self):
        self.teste.config() 
    
if __name__ == "__main__":
    unittest.main()