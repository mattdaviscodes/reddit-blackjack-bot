from deck import Deck, Card
from exceptions import NotEnoughCredits


PLAYER_ID = 1
DEALER_ID = 0

class Hand(object):
    """A blackjack hand."""

    def __init__(self, cards=None, dealer=False):
        self.dealer = dealer
        self.cards = cards
        if self.cards is None:
            self.cards = []

    @property
    def ascii(self):
        """Get single ascii string for all cards in hand.

        This method is totally unreadable, but it works. Might want to refactor
        later to be more developer-friendly.

        :return: single-string ascii representation of all cards
        """
        ascii = [card.ascii.split('\n') for card in self.cards]
        return '\n'.join([' '.join(line) for line in zip(*ascii)])

    @property
    def _raw_value(self):
        """Get numerical value of hand.

        This method makes no attempt to deal with Aces being valued at
        1 or 11. The property self.value should almost always be called,
        as it will try first to devalue any aces if a hand's value is
        greater than 21.
        """
        return sum([card.value for card in self.cards])

    @property
    def value(self):
        """Get numerical value of hand. Devalue aces if necessary.

        As aces may either be valued at 1 or 11, this method will attempt
        to keep the hand's total value below 11 if any aces are present by
        reducing their value to 1. Even if hand can not be devalued below
        21, the total value will be returned as an integer.

        :return: Integer value of all cards in hand, after devaluing aces.
        """
        while self._raw_value > 21:
            for card in self.cards:
                if card.value == 11:
                    card.value = 1
                    continue
            break
        return self._raw_value


class Blackjack(object):
    """A game of blackjack."""

    def __init__(self, user, bet, db_session, state=None):

        if user.credits < bet:
            raise NotEnoughCredits("Sorry, you can't afford to bet that much.")

        self.user = user
        self.bet = bet
        self.db_session = db_session
        self.state = state or self._init_state()
        self.deck = Deck()
        self.player_hands = [Hand()]
        self.dealer_hand = Hand(dealer=True)

    def _init_state(self):
        return "{1.51}"

    def _register_state_change(self):
        pass

    def charge_user(self):
        """Reduces user.credits by the amount bet on hand."""
        self.user.charge(self.bet)

    def pay_user(self):
        """Increases user.credits by double bet amount if user won."""
        if not self.player_hands[0].value > 21:
            if self.dealer_hand.value > 21 or self.player_hands[0].value > self.dealer_hand.value:
                self.user.pay(self.bet * 2)
            elif self.player_hands[0].value == self.dealer_hand.value:
                self.user.pay(self.bet)

    def deal(self):
        """Deal a game of blackjack.

        Two cards each for player and dealer, alternating.
        """
        for i in xrange(2):
            for hand in self.player_hands:
                hand.cards.append(self.deck.deal_one())
            self.dealer_hand.cards.append(self.deck.deal_one())

    def display(self):
        """Print state of game including hand values and ascii art."""
        print "Dealer: {}".format(self.dealer_hand.value)
        print self.dealer_hand.ascii

        for hand in self.player_hands:
            print "Player: {}".format(hand.value)
            print hand.ascii

    def hit(self, hand):
        """Deal one card to hand.

        Should error checking happen here? i.e. if hand.can_hit(): hit()
        """
        hand.cards.append(self.deck.deal_one())

    def split(self, hand):
        """Split hand into two hands. Deal one card to each."""
        card = hand.cards.pop()
        new_hand = Hand(cards=[card])
        hand.cards.append(self.deck.deal_one())
        new_hand.cards.append(self.deck.deal_one())
        self.player_hands.append(new_hand)


if __name__ == '__main__':
    blackjack = Blackjack()
    blackjack.deal()

    for hand in blackjack.player_hands:

        while hand.value <= 21:
            blackjack.display()
            action = raw_input("Hit, Stay, Double, or Split: ")
            if action.lower() == 'hit':
                blackjack.hit(hand)
            elif action.lower() == 'double':
                blackjack.hit(hand)
                break
            elif action.lower() == 'split':
                blackjack.split(hand)
            elif action.lower() == 'stay':
                break
            else:
                continue

    while blackjack.dealer_hand.value < 17:
        blackjack.hit(blackjack.dealer_hand)

    blackjack.display()
