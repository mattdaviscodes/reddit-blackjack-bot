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
            self.cur.execute('SELECT user_id from users where reddit_name=?', (mention.author.name,))
            try:
                author_id = self.cur.next()[0]
            except StopIteration:
                self.cur.execute('INSERT INTO users (reddit_name, reddit_fullname, created_date) VALUES (?,?,?)',
                                 (mention.author.name, mention.author.fullname, datetime.now().isoformat()))
                self.sql.commit()
                author_id = self.cur.lastrowid
            game = None
            if 'deal me in' in mention.body.lower():
                game = self.run_deal()
            if 'hit' in mention.body.lower():
                game = self.run_hit(author_id)
            if game:
                self.send_reply(mention, game)
                self.store_hand_state(game, author_id)
            mention.mark_read()

    def run_deal(self):
        game = Game()
        game.deal()
        return game

    def run_hit(self, author_id):
        self.cur.execute(
            'SELECT game_id, dealer_hand, player_hand FROM games WHERE user_id = ? and completed_date is null',
            (author_id,))
        game_id, dealer_hand, player_hand = self.cur.next()
        game = Game()
        game.game_id = game_id
        game.populate_game_from_db(dealer_hand, player_hand)
        game.player_hit()
        return game

    def send_reply(self, mention, game):
        reply = self.generate_reply(game)
        # mention.reply(reply)
        print reply

    def store_hand_state(self, game, author_id):
        if game.game_id:
            self.cur.execute('UPDATE games SET dealer_hand=?, player_hand=? where game_id=?',
                             (game.dealer_hand.encode_hand_for_db(), game.player_hand.encode_hand_for_db(),
                              game.game_id))
        else:
            self.cur.execute('INSERT INTO games (user_id, dealer_hand, player_hand, created_date) VALUES (?,?,?,?)',
                             (author_id, game.dealer_hand.encode_hand_for_db(), game.player_hand.encode_hand_for_db(),
                              datetime.now().isoformat()))
        self.sql.commit()

    def generate_reply(self, game):
        dealer_value = 'Dealer: {}'.format('?' if not game.player_stays else game.dealer_hand.get_hand_value())
        dealer_ascii = self.generate_hand_ascii_art(game.dealer_hand, dealer=True, player_stays=game.player_stays)
        player_value = 'Player: {}'.format(game.player_hand.get_hand_value())
        player_ascii = self.generate_hand_ascii_art(game.player_hand)
        reply_prompt = 'HIT or STAY'  # TODO
        footer = 'Other commands:\n\n* /u/blackjack_bot help\n* /u/blackjack_bot history\n* /u/blackjack_bot highscores\n\n^^Made ^^by ^^/u/Davism72. ^^Send ^^feedback!\n^^Source: ^^https://github.com/mattdavis1121/reddit-blackjack-bot'
        return '\n\n'.join([dealer_value, dealer_ascii, player_value, player_ascii, reply_prompt, footer])

    def generate_hand_ascii_art(self, hand, dealer=False, player_stays=False):
        line1 = '    '
        line2 = '    '
        line3 = '    '
        line4 = '    '
        for i, card in enumerate(hand.cards):
            line1 += ' __ '
            line2 += '|  |'
            if dealer and not player_stays and i == 0:
                line3 += '|  |'
            else:
                line3 += '|{}{}|'.format(card.symbol, card.suit)
            line4 += '|__|'
        return '\n'.join([line1, line2, line3, line4])


if __name__ == '__main__':
    # Connect to or create database
    print('Opening SQL Database')
    sql = sqlite3.connect('sql.db')
    cur = sql.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, reddit_name TEXT, reddit_fullname TEXT, created_date TEXT)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS games(game_id INTEGER PRIMARY KEY, user_id INTEGER, dealer_hand TEXT, player_hand TEXT, created_date TEXT, completed_date TEXT, FOREIGN KEY(user_id) REFERENCES users(user_id));')
    cur.execute('PRAGMA foreign_keys = ON;')

    # Connect to reddit
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME,
                         password=config.PASSWORD)
    bot = Bot(reddit, sql)

    loops = 0
    print('Begin main loop')
    while True:
        loops += 1
        if loops % 50 == 0:
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
