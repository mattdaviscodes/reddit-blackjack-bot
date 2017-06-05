import sqlite3

from config import DB_FILENAME
from models import Player

def db_connect():
    conn = sqlite3.connect(DB_FILENAME)

class PlayerRepository(object):

    def __init__(self, db_connection):
        self.conn = db_connection

    def player_get(self, name):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM players WHERE name = ?""", (name,))
        data = cursor.fetchall()
        cursor.close()
        player = None
        if data:    # Will either be empty list (no user) or one-item list
            player = self.fill_player_object(data[0])
        return player

    def new_player(self, name):
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO players (name) VALUES (?)""", (name,))
        cursor.close()
        self.conn.commit()

    def fill_player_object(self, row):
        player = Player()
        player.player_id = row[0]
        player.name = row[1]
        player.credits = row[2]
        player.is_blocked = row[3]
        player.created_date = row[4]
        return player
