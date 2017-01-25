import sqlite3
from datetime import datetime


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
                                    dealer_hand TEXT,
                                    player_hand TEXT,
                                    bet INTEGER,
                                    created_date TEXT,
                                    completed_date TEXT,
                                    FOREIGN KEY(user_id) REFERENCES users(user_id));''')
        self.cursor.execute('''PRAGMA foreign_keys = ON;''')

    def get_user(self, name):
        self.try_insert_new_user(name)
        query = '''SELECT user_id, reddit_name, bankroll FROM users WHERE reddit_user_name = ?'''
        self.cursor.execute(query, (name,))
        id, name, bankroll = self.cursor.fetchone()
        return User(id, name, bankroll)

    def try_insert_new_user(self, name):
        query = '''SELECT EXISTS (SELECT 1 FROM users WHERE reddit_name = ? LIMIT 1);'''
        self.cursor.execute(query, (name,))  # Returns 1 or 0
        if not self.cursor.fetchone():
            self.cursor.execute('INSERT INTO users (reddit_name, created_date) VALUES (?,?)',
                                (name, datetime.now().isoformat()))
            self.sql.commit()

    def get_current_game(self, user):
        pass


class User(object):
    def __init__(self, id, name, bankroll):
        self.id = None
        self.name = None
        self.game = None
        self.bankroll = None
        self.history = None
