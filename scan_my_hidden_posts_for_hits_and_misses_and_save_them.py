from subprocess import call

from datetime import datetime

import praw
import time
from datetime import datetime
from praw.reddit import Subreddit
from praw.reddit import Submission
import pprint
import os
import json
from post import *

def print_my_hits():
    i = 0
    d = {}
    bot = praw.Reddit('meaningful-cs-bot')
    with open('storage.json', 'w+') as f:
        #d = json.load(f)
        for item in bot.user.me().hidden(limit=None):
            if item.likes == True:
                hit = Post('HIT')
                d[item.permalink] = hit
            else:
                miss = Post('MISS')
                d[item.permalink] = miss
            #if item.permalink not in d:
            #    print(item.permalink)
        t = json.dumps(d, default=vars, indent=4)
        f.write(t)

if __name__ == "__main__":
    print_my_hits()
