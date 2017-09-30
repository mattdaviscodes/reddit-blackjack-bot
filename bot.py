class RedditBot(object):

    def config(self):
        """Configure bot from config.py."""
        pass

    def get_mentions(self):
        """Get all username mentions for bot.

        Will be a highly-used method, driving most of the action of every loop.
        """
        pass

    def send_reply(self):
        """Send response to a reddit post."""
        pass

    def send_dm(self):
        """Send direct message.

        Can be used to respond to players who started a game via DM, or to
        communicate at scale with players.
        """
        pass
