import praw

from config import DevConfig, ProdConfig
from commands import Command


class RedditBot(object):

    def __init__(self, dev=False):
        self.config = DevConfig if dev else ProdConfig
        self.reddit = praw.Reddit(client_id=self.config.CLIENT_ID,
                                  client_secret=self.config.CLIENT_SECRET,
                                  user_agent=self.config.CLIENT_SECRET,
                                  username=self.config.USERNAME,
                                  password=self.config.PASSWORD)

    def get_mentions(self):
        """Get all username mentions for bot.

        Will be a highly-used method, driving most of the action of every loop.
        """
        pass

    def send_reply(self):
        """Send response to a Reddit post."""
        pass

    def send_dm(self):
        """Send direct message.

        Can be used to respond to players who started a game via DM, or to
        communicate at scale with players.
        """
        pass

    def run(self):
        for comment in self.reddit.inbox.stream():

            # Only respond to my own comments if in dev mode
            if self.config.DEBUG and comment.author != 'Davism72':
                continue

            command = Command.parse(comment.body)
            if command:
                if command.is_legal:
                    # Respond Accordingly
                    print comment.author, comment.body
                else:
                    # Send error message
                    pass

if __name__ == '__main__':
    bot = RedditBot(dev=True)
    bot.run()