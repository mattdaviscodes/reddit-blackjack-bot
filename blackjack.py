from random import shuffle


class Game(object):
    ''' A stateless class to store all logic required for running a game of blackjack '''

    def __init__(self, bet=50):
        self.deck = None
        self.dealer_hand = Hand()
        self.player_hand = Hand()
        self.player_stays = False
        self.dealer_stays = False
        self.game_id = None
        self.bet = bet
        self.payout = None
        self.game_complete = False
        self.outcome = None

    def deal(self):
        self.deck = Deck().shuffle()
        for i in xrange(2):
            self.player_hand.cards.append(self.deck.pop())
            self.dealer_hand.cards.append(self.deck.pop())
        if self.player_hand.get_hand_value() == 21:
            self.player_hand.blackjack = True
        if self.dealer_hand.get_hand_value() == 21:
            self.dealer_hand.blackjack = True
        self.check_game()

    def can_hit(self):
        if len(self.deck) > 0 and not self.player_stays:
            return True
        else:
            return False

    def player_hit(self):
        self.player_hand.cards.append(self.deck.pop())
        self.check_game()

    def player_stay(self):
        self.player_stays = True
        self.check_game()

    def can_double_down(self):
        if len(self.player_hand.cards) == 2:
            return True
        else:
            return False

    def player_double_down(self):
        pass

    def can_split(self):
        if len(self.player_hand.cards) == 2 and self.player_hand.cards[0].symbol == self.player_hand.cards[0].symbol:
            return True
        else:
            return False

    def player_split(self):
        pass

    def dealer_hit(self):
        self.dealer_hand.cards.append(self.deck.pop())
        self.check_game()

    def dealer_play(self):
        while not self.game_complete:
            if self.dealer_hand.get_hand_value() == 17 and self.dealer_hand.has_ace():
                self.dealer_hit()
            elif self.dealer_hand.get_hand_value() >= 17:
                self.dealer_stays = True
            else:
                self.dealer_hit()
            self.check_game()

    def display_hands(self):
        print("Dealer: {}\n{}\n\nPlayer: {}\n{}\n".format(self.dealer_hand.get_hand_value(),
                                                          self.dealer_hand.get_hand_ascii_art(),
                                                          self.player_hand.get_hand_value(),
                                                          self.player_hand.get_hand_ascii_art()))

    def check_game(self):
        if self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
            if self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
                self.payout = self.bet
                self.outcome = "push"
            elif self.player_hand.is_blackjack():
                self.payout = self.bet * 2.5
                self.outcome = "player blackjack"
            else:
                self.payout = 0
                self.outcome = "dealer blackjack"
            self.game_complete = True
        if self.dealer_stays:
            if self.dealer_hand.get_hand_value() > self.player_hand.get_hand_value():
                self.payout = 0
                self.outcome = "dealer wins"
            elif self.dealer_hand.get_hand_value() < self.player_hand.get_hand_value():
                self.payout = self.bet * 2
                self.outcome = "player wins"
            else:
                self.payout = self.bet
                self.outcome = "push"
            self.game_complete = True
        if self.dealer_hand.get_hand_value() > 21:
            if not self.dealer_hand.devalue_ace():
                self.payout = self.bet * 2
                self.outcome = "dealer busts"
                self.game_complete = True
        elif self.player_hand.get_hand_value() > 21:
            if not self.player_hand.devalue_ace():
                self.payout = 0
                self.outcome = "player busts"
                self.game_complete = True


class Hand(object):
    def __init__(self):
        self.cards = []
        self.blackjack = False

    def is_blackjack(self):
        return self.blackjack

    def get_hand_value(self):
        return sum([card.value for card in self.cards])

    def get_hand_ascii_art(self, dealer=False, ):
        line1 = '    '
        line2 = '    '
        line3 = '    '
        line4 = '    '
        for i, card in enumerate(self.cards):
            line1 += ' __ '
            line2 += '|  |'
            if dealer and i == 0:
                line3 += '|  |'
            else:
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
            if card.symbol == 'A' and card.value == 11:
                    card.value = 1
            if self.get_hand_value() <= 21:
                return True
        return False

    def __repr__(self):
        return "{} - {}".format(self.get_hand_value(), '|'.join([str(card) for card in self.cards]))


class Card(object):
    def __init__(self, suit, symbol, value, id):
        self.suit = suit  # [C,H,D,S]
        self.symbol = symbol  # [A,2,3,4,5,6,7,8,9,10,J,Q,K]
        self.value = value  # [1,2,3,4,5,6,7,8,9,10,11]
        self.id = id

    def __repr__(self):
        return "{}{}".format(self.symbol, self.suit)

    def __str__(self):
        return "{}{}".format(self.symbol, self.suit)


class Deck(object):
    def __init__(self):
        self.deck = [Card('C', 'A', 11, 0),
                     Card('C', '2', 2, 1),
                     Card('C', '3', 3, 2),
                     Card('C', '4', 4, 3),
                     Card('C', '5', 5, 4),
                     Card('C', '6', 6, 5),
                     Card('C', '7', 7, 6),
                     Card('C', '8', 8, 7),
                     Card('C', '9', 9, 8),
                     Card('C', 'T', 10, 9),
                     Card('C', 'J', 10, 10),
                     Card('C', 'Q', 10, 11),
                     Card('C', 'K', 10, 12),
                     Card('S', 'A', 11, 13),
                     Card('S', '2', 2, 14),
                     Card('S', '3', 3, 15),
                     Card('S', '4', 4, 16),
                     Card('S', '5', 5, 17),
                     Card('S', '6', 6, 18),
                     Card('S', '7', 7, 19),
                     Card('S', '8', 8, 20),
                     Card('S', '9', 9, 21),
                     Card('S', 'T', 10, 22),
                     Card('S', 'J', 10, 23),
                     Card('S', 'Q', 10, 24),
                     Card('S', 'K', 10, 25),
                     Card('H', 'A', 11, 26),
                     Card('H', '2', 2, 27),
                     Card('H', '3', 3, 28),
                     Card('H', '4', 4, 29),
                     Card('H', '5', 5, 30),
                     Card('H', '6', 6, 31),
                     Card('H', '7', 7, 32),
                     Card('H', '8', 8, 33),
                     Card('H', '9', 9, 34),
                     Card('H', 'T', 10, 35),
                     Card('H', 'J', 10, 36),
                     Card('H', 'Q', 10, 37),
                     Card('H', 'K', 10, 38),
                     Card('D', 'A', 11, 39),
                     Card('D', '2', 2, 40),
                     Card('D', '3', 3, 41),
                     Card('D', '4', 4, 42),
                     Card('D', '5', 5, 43),
                     Card('D', '6', 6, 44),
                     Card('D', '7', 7, 45),
                     Card('D', '8', 8, 46),
                     Card('D', '9', 9, 47),
                     Card('D', 'T', 10, 48),
                     Card('D', 'J', 10, 49),
                     Card('D', 'Q', 10, 50),
                     Card('D', 'K', 10, 51)]

    def shuffle(self):
        shuffle(self.deck)
        return self.deck
