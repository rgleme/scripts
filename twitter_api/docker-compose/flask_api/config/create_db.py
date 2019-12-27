import sqlite3

db = "twitter.db"

conn = sqlite3.connect(db)
c = conn.cursor()

try:
    c.execute("drop table twit_data")
except:
    pass

cmd = "CREATE TABLE twit_data (user TEXT, followers NUMBER, lang TEXT, location TEXT, datetime DATETIME, hashtag TEXT)"
c.execute(cmd)

conn.commit()

conn.close()