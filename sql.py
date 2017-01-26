import sqlite3
import pickle
from datetime import datetime

import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class BlackjackSQL(object):
    def __init__(self, filename):
        self.sql = sqlite3.connect(filename)
        self.cursor = self.sql.cursor()
        self.build_db()

    def build_db(self):
        """
        Run all commands necessary to build database from scratch
        :return: None
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    user_id INTEGER PRIMARY KEY,
                                    reddit_name TEXT,
                                    bankroll INTEGER DEFAULT 500,
                                    created_date TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                                    game_id INTEGER PRIMARY KEY,
                                    user_id INTEGER,
                                    bet INTEGER,
                                    pickled_game TEXT,
                                    created_date TEXT,
                                    completed_date TEXT,
                                    FOREIGN KEY(user_id) REFERENCES users(user_id));''')
        self.cursor.execute('''PRAGMA foreign_keys = ON;''')

    def get_user(self, name):
        self.try_insert_new_user(name)
        query = '''SELECT user_id, reddit_name, bankroll FROM users WHERE reddit_name = ?'''
        self.cursor.execute(query, (name,))
        user_id, name, bankroll = self.cursor.fetchone()
        game = self.get_current_game(user_id)
        return User(user_id, name, bankroll, game)

    def try_insert_new_user(self, name):
        query = '''SELECT EXISTS (SELECT 1 FROM users WHERE reddit_name = ? LIMIT 1);'''
        self.cursor.execute(query, (name,))  # Returns 1 or 0
        user_exists = self.cursor.fetchone()[0]
        if not user_exists:
            logging.info('Creating new user: %s', name)
            self.cursor.execute('INSERT INTO users (reddit_name, created_date) VALUES (?,?)',
                                (name, datetime.now().isoformat()))
            self.sql.commit()

    def get_current_game(self, user_id):
        query = '''SELECT pickled_game FROM games WHERE user_id = ? and completed_date is null'''
        self.cursor.execute(query, (user_id,))
        try:
            return pickle.loads(self.cursor.fetchone()[0])
        except TypeError:
            return None

    def insert_new_game(self, user):
        self.cursor.execute('INSERT INTO games (user_id, created_date) VALUES (?,?)',
                            (user.user_id, datetime.now().isoformat()))
        self.sql.commit()
        return self.cursor.lastrowid

    def store_hand_state(self, user):
        if user.game.game_complete:
            self.cursor.execute('UPDATE games SET pickled_game=?, completed_date=? where game_id=?',
                                (pickle.dumps(user.game), datetime.now().isoformat(), user.game.game_id))
        else:
            self.cursor.execute('UPDATE games SET pickled_game=? where game_id=?',
                                (pickle.dumps(user.game), user.game.game_id))
        self.sql.commit()

    def pay_user(self, user):
        self.cursor.execute('UPDATE users SET bankroll=? where user_id=?',
                            (user.bankroll + user.game.payout, user.user_id))
        self.sql.commit()

    def charge_user(self, user):
        self.cursor.execute('UPDATE users SET bankroll=? where user_id=?',
                            (user.bankroll - user.game.bet, user.user_id))
        self.sql.commit()


class User(object):
    def __init__(self, user_id, name, bankroll, game=None):
        self.user_id = user_id
        self.name = name
        self.bankroll = bankroll
        self.game = game
        self.history = None
