from random import shuffle


class Dealer(object):
    ''' A stateless class to store all logic required for running a game of blackjack '''

    def __init__(self):
        self.deck = Deck().shuffle()
        self.dealer_hand = Hand()
        self.player_hand = Hand()
        self.player_stays = False
        self.dealer_stays = False

    def deal(self):
        for i in xrange(2):
            self.player_hand.cards.append(self.deck.pop())
            self.dealer_hand.cards.append(self.deck.pop())

    def player_hit(self):
        self.player_hand.cards.append(self.deck.pop())

    def player_stay(self):
        self.player_stays = True

    def player_double_down(self):
        pass

    def player_split(self):
        pass

    def dealer_hit(self):
        self.dealer_hand.cards.append(self.deck.pop())

    def dealer_play(self):
        if self.dealer_hand.get_hand_value() == 17 and self.dealer_hand.has_ace():
            self.dealer_hit()
        elif self.dealer_hand.get_hand_value() >= 17:
            self.dealer_stays = True
        else:
            self.dealer_hit()

    def display_hands(self):
        print("Dealer: {}\n{}\n\nPlayer: {}\n{}\n".format(self.dealer_hand.get_hand_value(),
                                                          self.dealer_hand.get_hand_ascii_art(),
                                                          self.player_hand.get_hand_value(),
                                                          self.player_hand.get_hand_ascii_art()))

    def get_reddit_reply(self):
        # TODO: Break into component parts -- e.g. Dealer, Player, Reply Prompt, Footer, etc
        reply = '''Dealer: {}\n\n{}\n\nPlayer: {}\n\n{}\n\nPlease reply: {}\n\n---\nOther commands:\n\n* /u/blackjack_bot help\n* /u/blackjack_bot history\n* /u/blackjack_bot highscores\n\n^^Made ^^by ^^/u/Davism72. ^^Send ^^feedback!\n^^Source: ^^https://github.com/mattdavis1121/reddit-blackjack-bot'''.format(
            self.dealer_hand.get_hand_value(), self.dealer_hand.get_hand_ascii_art(), self.player_hand.get_hand_value(),
            self.player_hand.get_hand_ascii_art(), None)
        return reply

    def hand_complete(self):
        if self.dealer_stays:
            if self.dealer_hand.get_hand_value() > self.player_hand.get_hand_value():
                print("Dealer wins.")
            elif self.dealer_hand.get_hand_value() < self.player_hand.get_hand_value():
                print("Player wins.")
            else:
                print("Push.")
            return True
        if self.dealer_hand.get_hand_value() > 21:
            if self.dealer_hand.devalue_ace():
                return False
            else:
                print("Dealer busts. Player wins.")
                return True
        elif self.player_hand.get_hand_value() > 21:
            if self.player_hand.devalue_ace():
                return False
            else:
                print("Player busts. Dealer wins.")
                return True
        return False


class Hand(object):
    def __init__(self):
        self.cards = []

    def get_hand_value(self):
        return sum([card.value for card in self.cards])

    def get_hand_ascii_art(self):
        line1 = '    '
        line2 = '    '
        line3 = '    '
        line4 = '    '
        for card in self.cards:
            line1 += ' __ '
            line2 += '|  |'
            line3 += '|{}{}|'.format(card.symbol, card.suit)
            line4 += '|__|'
        return '\n'.join([line1, line2, line3, line4])

    def has_ace(self):
        for card in self.cards:
            if card.symbol == 'A':
                return True
        return False

    def devalue_ace(self):
        for card in self.cards:
            if card.symbol == 'A':
                card.value = 1
                return True
        return False

    def encode_hand_for_db(self):
        return '|'.join([card.id for card in self.cards])

    def decode_hand_from_db(self):
        pass

    def __repr__(self):
        return "{} - {}".format(self.get_hand_value(), '|'.join([str(card) for card in self.cards]))


class Card(object):
    def __init__(self, suit, symbol, value, id):
        self.suit = suit  # [C,H,D,S]
        self.symbol = symbol  # [A,2,3,4,5,6,7,8,9,10,J,Q,K]
        self.value = value  # [1,2,3,4,5,6,7,8,9,10,11]
        self.id = id

    def get_ascii_art(self):
        pass

    def __repr__(self):
        return "{}{}".format(self.symbol, self.suit)

    def __str__(self):
        return "{}{}".format(self.symbol, self.suit)


class Deck(object):
    def __init__(self):
        self.deck = [Card('C', 'A', 11, 1),
                     Card('C', '2', 2, 2),
                     Card('C', '3', 3, 3),
                     Card('C', '4', 4, 4),
                     Card('C', '5', 5, 5),
                     Card('C', '6', 6, 6),
                     Card('C', '7', 7, 7),
                     Card('C', '8', 8, 8),
                     Card('C', '9', 9,9),
                     Card('C', 'T', 10, 10),
                     Card('C', 'J', 10, 11),
                     Card('C', 'Q', 10, 12),
                     Card('C', 'K', 10, 13),
                     Card('S', 'A', 11, 14),
                     Card('S', '2', 2, 15),
                     Card('S', '3', 3, 16),
                     Card('S', '4', 4, 17),
                     Card('S', '5', 5, 18),
                     Card('S', '6', 6, 19),
                     Card('S', '7', 7, 20),
                     Card('S', '8', 8, 21),
                     Card('S', '9', 9, 22),
                     Card('S', 'T', 10, 23),
                     Card('S', 'J', 10, 24),
                     Card('S', 'Q', 10, 25),
                     Card('S', 'K', 10, 26),
                     Card('H', 'A', 11, 27),
                     Card('H', '2', 2, 28),
                     Card('H', '3', 3, 29),
                     Card('H', '4', 4, 30),
                     Card('H', '5', 5, 31),
                     Card('H', '6', 6, 32),
                     Card('H', '7', 7, 33),
                     Card('H', '8', 8, 34),
                     Card('H', '9', 9, 35),
                     Card('H', 'T', 10, 36),
                     Card('H', 'J', 10, 37),
                     Card('H', 'Q', 10, 38),
                     Card('H', 'K', 10, 39),
                     Card('D', 'A', 11, 40),
                     Card('D', '2', 2, 41),
                     Card('D', '3', 3, 42),
                     Card('D', '4', 4, 43),
                     Card('D', '5', 5, 44),
                     Card('D', '6', 6, 45),
                     Card('D', '7', 7, 46),
                     Card('D', '8', 8, 47),
                     Card('D', '9', 9, 48),
                     Card('D', 'T', 10, 49),
                     Card('D', 'J', 10, 50),
                     Card('D', 'Q', 10, 51),
                     Card('D', 'K', 10, 52)]

    def shuffle(self):
        shuffle(self.deck)
        return self.deck
