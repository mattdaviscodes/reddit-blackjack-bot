import sqlalchemy


class User:
    """Model to represent users.

    Tempted to call this Player, but I might want to create users for
    people who haven't started a game yet -- if they just issue a
    non game-starting command.
    """
    pass


class Game:
    """Model to represent hands of blackjack.

    Fields:
        start date
        end date
        player (FK)
        game state (blackjack notation)
        bet
    """
    pass


class Achievement:
    """Lookup table for player achievements.

    Fields:
        name
        description
        bounty -- point award for earning achievement?

    Possible:
        hit blackjack
        pushed on a blackjack
        hit 21 on doble down
        stayed on <10 and won
        hit on 19> and didn't bust
    """
    pass


class UserAchievement:
    """Mapping table -- users to achievements

    Not sure if this is required. If sqlalchemy works the same without Flask
    as it does with Flask, then all I need is the two tables, and sqlalchemy
    will take care of the relationship for me.
    """
    pass




