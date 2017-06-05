

class BlackjackModelBase(object):
    """ Implements all basic functionality of a blackjack model. """

    def __init__(self):
        pass

    def build_table(self):
        """ Issues a complete CREATE TABLE statement based on child model fields. """
        pass

class FieldBase(object):

    def __init__(self):
        pass

class TextField(FieldBase):

    def __init__(self):
        pass

class Player(object):

    def __init__(self):
        self.player_id = None
        self.name = None
        self.credits = None
        self.is_blocked = None
        self.created_date = None
