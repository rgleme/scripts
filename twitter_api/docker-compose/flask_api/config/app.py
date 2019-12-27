from flask import Flask, render_template, request
from collections import Counter
import sqlite3
import subprocess

db = "twitter.db"
langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)', 'und': 'N/A', 'in': 'N/A'}

app = Flask(__name__)

def get_top_tweets():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("select followers,user from twit_data ORDER by 1 DESC")
    result = c.fetchall()
    tweets = []
    inc = 1

    for tweet in result:
        if inc < 6:
            if tweet not in tweets: 
                tweets.append(tweet)
                inc += 1
    
    conn.close()
    return tweets

def top_tweets_tag_lang(hashtag):
    languages = []
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("select lang, count(lang) from twit_data where hashtag = '{0}' group by lang".format(hashtag))
    result = c.fetchall()
    for tweet in result:
        languages.append(langs[tweet[0]])
        languages.append(tweet[1])

    conn.close()
    print (languages)
    print (tweet)
    return languages        

def top_tweets_tag_location(hashtag):
    locations = []
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("select location, count(location) from twit_data where hashtag = '{0}' group by location".format(hashtag))
    result = c.fetchall()
    for tweet in result:
        locations.append(tweet)
    conn.close()
    return locations

def top_tweets_hour():
    hours = []
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("select strftime('%Y-%m-%d %H', datetime), count (datetime) from twit_data group by strftime('%Y-%m-%d %H', datetime);")
    result = c.fetchall()
    for tweet in result:
        hours.append(tweet[0])
        hours.append(tweet[1])
    conn.close()
    return hours 

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/top_users")
def top_users():
    tweets = get_top_tweets()
    return render_template('top_users.html', tweets = tweets)

@app.route("/populate_list")
def populate_list():
    subprocess.check_call(["python create_db.py"], shell=True)
    subprocess.check_call(["python twit.py"], shell=True)
    return render_template('populate_list.html')

@app.route("/search_tweets")
def search_tweets():
    return render_template('search_tweets.html')

@app.route("/tweets_by_tag",methods = ['POST', 'GET'])
def tweets_by_tag():
    if request.method == 'POST':
        result = request.form
        for key,value in result.items():
            tweets = top_tweets_tag_lang(value)
            locations = top_tweets_tag_location(value)
            return render_template('tweets_by_tag.html', tweets = tweets, hashtag = value, locations = locations)

@app.route("/tweets_by_hour")
def tweets_by_hour():
    tweets = top_tweets_hour()
    return render_template('tweets_by_hour.html', tweets = tweets)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)