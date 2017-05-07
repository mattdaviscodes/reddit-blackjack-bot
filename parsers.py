import argparse

# Meta Parser
# Only good for test mode right now
meta_parser = argparse.ArgumentParser()
meta_parser.add_argument('--test', action="store_true")
meta_args = meta_parser.parse_args()

class MentionParser(argparse.ArgumentParser, object):
    """
    A class to parse mentions by Reddit users for commands.
    """

    def __init__(self):
        # Initialize base class
        super(MentionParser, self).__init__()

        # Define our arguments
        self.add_argument('-b', '--bet', type=self.bet_type,
                          help='specify a bet other than the default. must be used with -d/--deal. example: "--deal --bet 100"')
        self.add_argument('-d', '--deal', action='store_true', help='deal a new hand')
        self.add_argument('--hit', action='store_true', help='issue a hit command')
        self.add_argument('-s', '--stay', action='store_true',
                          help='issue a stay command and allow dealer to play out hand')
        self.add_argument('-dd', '--doubledown', '--double', dest='double_down', action='store_true',
                          help='issue a double down command')
        self.add_argument('-sp', '--split', action='store_true', help='issue a split command - CURRENTLY INOPERABLE')
        self.add_argument('--history', action='store_true', help='display user hand history - CURRENTLY INOPERABLE')
        self.add_argument('--highscores', '--leaderboard', dest='high_scores', action='store_true',
                          help='display the highest scoring users')
        self.add_argument('--recharge', action='store_true',
                          help='reset credits to the default 500. only works if bankroll < 500')

    def valid_command_received(self, mention):
        """ Test if any valid command is found in a mention. """
        valid, invalid = self.parse_known_args(mention)
        for k, v in valid.__dict__.iteritems():
            if v:
                return True
        else:
            return False

    def parse_known_args(self, args=None, namespace=None):
        """ Standardize input (if any) before passing to ArgumentParser.parse_known_args. """
        if isinstance(args, basestring):
            args = args.lower().split()
            return super(MentionParser, self).parse_known_args(args)
        else:
            return super(MentionParser, self).parse_known_args()

    def bet_type(self, bet):
        try:
            bet = int(bet)
        except ValueError:
            raise Exception("Invalid bet")
        except TypeError:
            raise Exception("Invalid bet")

        if bet <= 0:
            raise Exception("Invalid bet - must be positive")
        return bet

class BetAction(argparse.Action):
    """ Custom argparse action to ensure bets are positive integers """
    def __call__(self, parser, namespace, values, option_string=None):
        if not isinstance(values, int):
            raise ValueError("--bet requires integer argument")
        if values <= 0:
            raise ValueError("--bet must be greater than zero")
        setattr(namespace, self.dest, values)

