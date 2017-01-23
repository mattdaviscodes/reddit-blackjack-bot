import praw
import config
import sqlite3
import sys
import time
import traceback

from datetime import datetime

from blackjack import Game

try:
    import config
except ImportError:
    # Handle error if no config.py file found
    pass


class Bot(object):
    def __init__(self, reddit, sql):
        self.reddit = reddit
        self.sql = sql
        self.cur = sql.cursor()

    def parse_mentions(self):
        mentions = list(self.reddit.inbox.unread())
        for mention in mentions:
            self.cur.execute('INSERT INTO users (reddit_name, reddit_fullname, created_date) VALUES (?,?,?)',
                             (mention.author.name, mention.author.fullname, datetime.now().isoformat()))
            self.sql.commit()
            author_id = self.cur.lastrowid
            game = None
            if 'deal me in' in mention.body:
                game = self.run_deal()
            if game:
                self.send_reply(mention, game)
                self.store_hand_state(game)
            mention.mark_read()

    def run_deal(self):
        game = Game()
        game.deal()
        return game

    def send_reply(self, mention, game):
        reply = self.generate_reply(game)
        #mention.reply(reply)
        print reply

    def store_hand_state(self, game):
        self.cur.execute('INSERT INTO games (dealer_hand, player_hand, created_date) VALUES (?,?,?)',
                         (game.dealer_hand.encode_hand_for_db(), game.player_hand.encode_hand_for_db(),
                         datetime.now().isoformat()))
        self.sql.commit()

    def generate_reply(self, game):
        reply = '''Dealer: {}\n\n{}\n\nPlayer: {}\n\n{}\n\nPlease reply: {}\n\n---\nOther commands:\n\n* /u/blackjack_bot help\n* /u/blackjack_bot history\n* /u/blackjack_bot highscores\n\n^^Made ^^by ^^/u/Davism72. ^^Send ^^feedback!\n^^Source: ^^https://github.com/mattdavis1121/reddit-blackjack-bot'''.format(
            game.dealer_hand.get_hand_value(), game.dealer_hand.get_hand_ascii_art(), game.player_hand.get_hand_value(),
            game.player_hand.get_hand_ascii_art(), None)  # TODO: Implement reply prompts
        return reply

if __name__ == '__main__':
    # Connect to or create database
    print('Opening SQL Database')
    sql = sqlite3.connect('sql.db')
    cur = sql.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, reddit_name TEXT, reddit_fullname TEXT, created_date TEXT)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS games(game_id INTEGER PRIMARY KEY, dealer_hand TEXT, player_hand TEXT, created_date TEXT, completed_date TEXT)')

    # Connect to reddit
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME,
                         password=config.PASSWORD)
    bot = Bot(reddit, sql)

    loops = 0
    while True:
        loops += 1
        print("Loop {}".format(loops))
        try:
            bot.parse_mentions()
        except KeyboardInterrupt:
            sys.exit()
        except praw.exceptions.APIException as e:
            # TODO: Investigate if this catches only rate limit exceptions, or more
            print(e)
            print("Rate limit exceeded. Sleeping for 1 minute.")
            time.sleep(60)
        except Exception as e:
            print(traceback.format_exc())