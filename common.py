import praw
import sqlite3

import config

def reddit_connect():
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME,
                         password=config.PASSWORD)
    return reddit

def db_connect():
    db = sqlite3.connect(config.DB_FILENAME)
    return db

def build_db():
    db = db_connect()
    with open('tables.sql') as f:
        db.executescript(f.read())
    with open('magic_numbers.sql') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
