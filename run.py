from bot import Session
from bot.blackjack import Blackjack
from bot.sql import User, Game


if __name__ == '__main__':

    # Base.metadata.create_all(engine)

    session = Session()

    user = session.query(User).filter_by(username='matt').one()

    while True:

        blackjack = Blackjack(user, 50, session)
        blackjack.charge_user()
        blackjack.deal()

        for hand in blackjack.player_hands:

            hand.active = True

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

            hand.active = False

        while blackjack.dealer_hand.value < 17:
            blackjack.hit(blackjack.dealer_hand)

        blackjack.display()
        blackjack.pay_user()

        play_again = raw_input("Play again? (y/n)")
        if play_again == 'n':
            break
