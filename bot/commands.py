"""Allowed commands for Reddit Blackjack Bot"""

class Command(object):
    """Base class for all commands."""

    @staticmethod
    def parse(text):
        """Parse a Reddit comment's body text for valid commands.

        :param text: praw.models.Comment.body
        :return: Proper command class or None
        """
        command = None
        if 'deal me in' in text:
            command = Deal()
        return command

    @property
    def is_legal(self):
        """Dummy method. Will replace with actual checking later."""
        return True


class Deal(Command):
    pass
