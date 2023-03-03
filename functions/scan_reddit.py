from typing import List
from subprocess import call

from datetime import datetime

import json
import praw
import time
from datetime import datetime
from praw.reddit import Subreddit
from praw.reddit import Submission
import pprint
import os

from search_result import SearchResult
from post import Post
from search_parameters import SearchParameters
from search_parameters import search_parameters_list_by_subreddit_name

# the exclusions_list contains strings that aren't allowed in the permalink of posts
exclusions_list = [
        'u_ayaankKhan562',
        'r/COMMCoin',
]

r = praw.Reddit('meaningful-cs-bot')

def search_subreddit(subreddit_name: str, search_parameters: SearchParameters):
    subreddit: Subreddit = r.subreddit(subreddit_name)
    print('Searching /r/' + subreddit_name + ' for \'' + search_parameters.query + '\' with sort=' + str(search_parameters.sort))
    # 'submissions' refers to what you usually call reddit 'posts'. Praw uses the term 'submission' so I adopted it.
    submissions_iterable = subreddit.search(search_parameters.query, sort=search_parameters.sort)
    submissions = []
    for submission in submissions_iterable:
        for exclusion in exclusions_list:
            if exclusion in submission.permalink:
                print('not adding ' + submission.permalink + ' because it had ' + exclusion)
            else:
                submissions.append(submission)

    return submissions

def search(search_parameters_list_by_subreddit):
    search_results = []
  
    for subreddit_name, search_parameters_list in search_parameters_list_by_subreddit.items():
        for search_parameters in search_parameters_list:
            search_result = SearchResult(subreddit_name, search_parameters)
            search_result.submissions = search_subreddit(subreddit_name, search_parameters)
            search_results.append(search_result)

    return search_results

# This function will create a string which contains a list of the permalinks in search_results
def create_permalinks_string(search_results: List[SearchResult]):
    m = ''
    submissions = []
    for search_result in search_results:
        for submission in search_result.submissions:
            contains_exclusion = False
            for exclusion in exclusions_list:
                if exclusion in submission.permalink:
                    contains_exclusion = True
            # If submission is already in submissions, then don't add it again, so we don't have any duplicates.
            if submission not in submissions:
                if not contains_exclusion:
                    submissions.append(submission)
    # Sort all the submissions, so it's easy for me to comment on the most recent ones. I think a non-trivial part of my impact with my comments is how quickly I comment. The quicker the better.
    submissions.sort(key=lambda submission: submission.created_utc, reverse=True)
    for submission in submissions:
        m += 'https://www.reddit.com' + submission.permalink + '\n'
    return m


start_time = time.time()
search_results = search(search_parameters_list_by_subreddit_name)
create_permalinks_string(search_results)
print(os.path.basename(__file__) + " completed in %.2f seconds." % (time.time() - start_time))
