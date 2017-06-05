from common import reddit_connect, db_connect, build_db
import praw
from repositories import PlayerRepository

if __name__ == '__main__':

    reddit = reddit_connect()
    build_db()

    while True:

        mentions = list(reddit.inbox.unread())
        for mention in mentions:

            if not isinstance(mention, praw.models.reddit.comment.Comment):
                continue

            author = mention.author.name
            sub = mention.subreddit.display_name

            # Testing environment
            if author != 'Davism72' or sub != 'testingground4bots':
                continue

            player_repo = PlayerRepository(db_connect())

            player = player_repo.player_get(author)
            if not player:
                player_repo.new_player(author)
                player = player_repo.player_get(author)

            print player.player_id, player.name, player.created_date
            mention.mark_read()
