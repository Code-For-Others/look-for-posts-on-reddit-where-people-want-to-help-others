from typing import List
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

from search_parameters import SearchParameters

class SearchResult:
    def __init__(self, subreddit_name: str, search_parameters: SearchParameters, submissions: List[Submission] = None):
        self.subreddit_name = subreddit_name
        self.search_parameters = search_parameters
        self.submissions = submissions

def create_bot():
    return praw.Reddit('meaningful-cs-bot')

r = create_bot()

SECONDS_IN_A_MONTH = 2628000.0

class Hit:
    def __init__(self, permalink: str, search_parameters: List[SearchParameters]):
        self.permalink = permalink
        self.search_parameters = search_parameters

class Miss:
    def __init__(self, permalink: str, search_parameters: List[SearchParameters]):
        self.permalink = permalink
        self.search_parameters = search_parameters

def print_my_hits():
    i = 0
    d = {'hits':[], 'misses':[]}
    #for item in r.user.me().hidden(limit=None):
    for item in r.user.me().hidden():
        if item.likes == True:
            hit = Hit(item.permalink, [])
            d['hits'].append(hit)
        elif item.likes == False:
            miss = Miss(item.permalink, [])
            d['misses'].append(miss)
    print(json.dumps(d, default=vars, indent=4))

if __name__ == "__main__":
    print_my_hits()
