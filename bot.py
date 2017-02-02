import praw
import config
import sqlite3
import sys
import time
import traceback
from datetime import datetime

from blackjack import Game
from sql import BlackjackSQL
from parsers import meta_args, cmd_parser


try:
    import config
except ImportError:
    # Handle error if no config.py file found
    pass

import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Should create a custom logger and substitute it with all praw replies
# Doesn't work, and I don't know why. Leaving it for now,
# but will likely delete later
if meta_args.test:
    # Create custom logger to overwrite external communications
    testmode = logging.getLogger('TestMode')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(asctime)s\n%(message)s')
    handler.setFormatter(formatter)
    testmode.addHandler(handler)

    # Replace all reddit responses with logs to new custom logger
    praw.models.Submission.reply = testmode.warn


class Bot(object):
    def __init__(self, reddit, sql):
        self.reddit = reddit
        self.sql = sql

    def parse_mentions(self):
        mentions = list(self.reddit.inbox.unread())
        for mention in mentions:

            # Only allow actions on posts by me in test mode
            if meta_args.test and mention.author.name != 'Davism72':
                continue

            user = sql.get_user(mention.author.name)
            if 'deal me in' in mention.body.lower():
                if not user.game:
                    logging.info('Dealing new hand to %s', user.name)
                    user.game = Game()
                    user.game.game_id = self.sql.insert_new_game(user)
                    self.sql.charge_user(user)
                    user.game.deal()
                else:
                    self.generate_error_message(mention, "Invalid action - user already has game active")
            # Write logic for variable bets here
            # Need to find "bet" in string, then parse out the following int
            if 'hit' in mention.body.lower():
                if user.game and user.game.can_hit():
                    logging.info('%s hits', user.name)
                    user.game.player_hit()
                else:
                    logging.info('%s invalid hit', user.name)
                    self.generate_error_message(mention, "Invalid action - Hit not allowed in game state")
            if 'stay' in mention.body.lower():
                logging.info('%s stays', user.name)
                if user.game:
                    user.game.player_stay()
                else:
                    logging.info('%s invalid stay', user.name)
                    self.generate_error_message(mention, "Invalid action - Stay not allowed without active game")
            if 'double down' in mention.body.lower():
                logging.info('%s doubles down', user.name)
                if user.game and user.game.can_double_down():
                    self.sql.charge_user(user)
                    user.game.player_double_down()
                else:
                    logging.info('%s invalid double down', user.name)
                    self.generate_error_message(mention, "Invalid action - Double down not allowed in game state")
            if user.game:
                mention.reply(self.generate_reply(user.game))
                self.sql.store_hand_state(user)
                if user.game.game_complete:
                    logging.info('Game complete. User: %s - Game ID: %s', user.name, user.game.game_id)
                    self.sql.pay_user(user)
                mention.mark_read()

    def generate_reply(self, game):
        outcome = game.outcome.upper() if game.game_complete else None
        bet = 'Bet: {}'.format(game.original_bet)
        if game.double_down:
            bet += ' (+{})'.format(game.original_bet)
        # payout = "Payout: {}".format(game.payout - game.bet) if game.payout - game.bet > 0 else None
        payout = None
        dealer_value = 'Dealer: {}'.format('?' if not game.game_complete else game.dealer_hand.get_hand_value())
        dealer_ascii = self.generate_hand_ascii_art(game.dealer_hand, dealer=True, game_complete=game.game_complete)
        player_value = 'Player: {}'.format(game.player_hand.get_hand_value())
        player_ascii = self.generate_hand_ascii_art(game.player_hand)
        reply_prompt = 'HIT or STAY' if not game.game_complete else None
        footer = '^^Send ^^feedback!\n^^Source: ^^https://github.com/mattdavis1121/reddit-blackjack-bot'
        return '\n\n'.join(filter(None, [outcome, bet, payout, dealer_value, dealer_ascii, player_value, player_ascii,
                                         reply_prompt, footer]))

    def generate_error_message(self, mention, msg):
        mention.reply(msg)
        mention.mark_read()

    def generate_hand_ascii_art(self, hand, dealer=False, game_complete=False):
        line1 = '    '
        line2 = '    '
        line3 = '    '
        line4 = '    '
        for i, card in enumerate(hand.cards):
            line1 += ' __ '
            line2 += '|  |'
            if dealer and not game_complete and i == 0:
                line3 += '|  |'
            else:
                line3 += '|{}{}|'.format(card.symbol, card.suit)
            line4 += '|__|'
        return '\n'.join([line1, line2, line3, line4])


if __name__ == '__main__':
    # Connect to or create database
    logging.info('Opening SQL Database')
    sql = BlackjackSQL('sql.db')
    sql.build_db()

    # Connect to reddit
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME,
                         password=config.PASSWORD)
    bot = Bot(reddit, sql)

    loops = 0
    logging.info('Begin main loop')
    while True:
        loops += 1
        if loops % 100 == 0:
            logging.info("Loop {}".format(loops))
        try:
            bot.parse_mentions()
        except KeyboardInterrupt:
            sys.exit()
        except praw.exceptions.APIException as e:
            # TODO: Investigate if this catches only rate limit exceptions, or more
            logging.warn(e)
            logging.warn("Rate limit exceeded. Sleeping for 1 minute.")
            time.sleep(60)
        except Exception as e:
            logging.error(traceback.format_exc())
