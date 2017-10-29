from bot import Session
from bot.bot import RedditBot
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

        game = Game(user_id=user.id, json=blackjack.json, bet=blackjack.bet)
        game.save()

        for hand in blackjack.player_hands:

            hand.active = True

            while hand.value <= 21:
                blackjack.display()
                action = raw_input("Hit, Stay, Double, or Split: ")
                if action.lower() == 'hit':
                    blackjack.hit(hand)
                    game.update(json=blackjack.json)
                elif action.lower() == 'double':
                    blackjack.hit(hand)
                    game.update(json=blackjack.json, bet=blackjack.bet)
                    break
                elif action.lower() == 'split':
                    blackjack.split(hand)
                    game.update(json=blackjack.json, bet=blackjack.bet)
                elif action.lower() == 'stay':
                    game.update(json=blackjack.json)
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
