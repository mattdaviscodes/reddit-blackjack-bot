import praw
import sys  # Used only for exiting script
import time
import sqlite3

try:
    import config
except ImportError:
    # Handle error if no config.py file found
    pass

if __name__ == '__main__':
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME,
                         password=config.PASSWORD)

    # TODO: Verify that reddit class inst correctly

    loops = 0
    while True:
        loops += 1
        print("Loop {}".format(loops))
        try:
            for subreddit in config.SUBREDDITS:
                sub = reddit.subreddit(subreddit)
                for post in sub.new():
                    # TODO: Check if the post itself contains a summon
                    for comment in post.comments:
                        for summon in config.SUMMON_STRINGS:
                            if summon in comment.body.lower():
                                # TODO: Check if bot has already responded to this comment
                                print("Summoned by {} in thread {}. Comment ID: {}".format(comment.author, post.title,
                                                                                           comment.id))
                                comment.reply('Dealing')
        except KeyboardInterrupt:
            sys.exit()
        except praw.exceptions.APIException:
            # TODO: Investigate if this catches only rate limit exceptions, or more
            print("Rate limit exceeded. Sleeping for 10 minutes.")
            time.sleep(600)
        except Exception as e:
            print("EXCEPTION: {}".format(e))
