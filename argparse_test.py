from parsers import meta_args
import logging
import praw

def x(i):
    print i

if meta_args.test:
    # Create custom logger to overwrite external communications
    testmode = logging.getLogger('TestMode')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(asctime)s\n%(message)s')
    handler.setFormatter(formatter)
    testmode.addHandler(handler)

    # Replace all reddit responses with logs to new custom logger
    x = testmode.warn

x('hello')