import praw

# according to https://github.com/reddit-archive/reddit/wiki/API we shouldn't call the API more than 60 times a minute
# so waiting 2 seconds between API calls should be conservatively safe
seconds_to_wait_between_api_calls = 1.5


def create_bot():
    return praw.Reddit('meaningful-cs-bot')
