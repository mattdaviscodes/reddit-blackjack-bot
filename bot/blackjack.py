from deck import Deck, cards_to_ascii

if __name__ == '__main__':
    deck = Deck()

    player = []
    dealer = []
    game_over = False

    for _ in xrange(2):
        player.append(deck.deal_one())
        dealer.append(deck.deal_one())

    while not game_over:
        print cards_to_ascii(dealer)
        print cards_to_ascii(player)

        action = raw_input("""What would you like to do?
            1: Hit
            2: Stay
            Input: """)

        if action == str(1):
            player.append(deck.deal_one())
        elif action == str(2):
            game_over = True