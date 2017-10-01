import random


def cards_to_ascii(cards):
    """Get single ascii string for all cards in hand.

    This method is totally unreadable, but it works. Might want to refactor
    later to be more developer-friendly.

    :param cards: list of Card objects
    :return: single-string ascii representation of all cards
    """
    ascii = [card.ascii.split('\n') for card in cards]
    return '\n'.join([' '.join(line) for line in zip(*ascii)])


class Card(object):
    """A playing card."""

    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value

    @property
    def ascii(self):
        template = """ __ \n|  |\n|{}{}|\n|__|"""
        return template.format(str(self.rank).upper(), self.suit.upper())


class Deck(object):
    """A deck of playing cards."""

    def __init__(self):
        self.cards = [
            Card('a', 's', 11),
            Card('2', 's', 2),
            Card('3', 's', 3),
            Card('4', 's', 4),
            Card('5', 's', 5),
            Card('6', 's', 6),
            Card('7', 's', 7),
            Card('8', 's', 8),
            Card('9', 's', 9),
            Card('t', 's', 10),
            Card('j', 's', 10),
            Card('q', 's', 10),
            Card('k', 's', 10),
            Card('a', 'd', 11),
            Card('2', 'd', 2),
            Card('3', 'd', 3),
            Card('4', 'd', 4),
            Card('5', 'd', 5),
            Card('6', 'd', 6),
            Card('7', 'd', 7),
            Card('8', 'd', 8),
            Card('9', 'd', 9),
            Card('t', 'd', 10),
            Card('j', 'd', 10),
            Card('q', 'd', 10),
            Card('k', 'd', 10),
            Card('a', 'c', 11),
            Card('2', 'c', 2),
            Card('3', 'c', 3),
            Card('4', 'c', 4),
            Card('5', 'c', 5),
            Card('6', 'c', 6),
            Card('7', 'c', 7),
            Card('8', 'c', 8),
            Card('9', 'c', 9),
            Card('t', 'c', 10),
            Card('j', 'c', 10),
            Card('q', 'c', 10),
            Card('k', 'c', 10),
            Card('a', 'h', 11),
            Card('2', 'h', 2),
            Card('3', 'h', 3),
            Card('4', 'h', 4),
            Card('5', 'h', 5),
            Card('6', 'h', 6),
            Card('7', 'h', 7),
            Card('8', 'h', 8),
            Card('9', 'h', 9),
            Card('t', 'h', 10),
            Card('j', 'h', 10),
            Card('q', 'h', 10),
            Card('k', 'h', 10),
        ]
        random.shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()

    @classmethod
    def from_notation(cls):
        pass
