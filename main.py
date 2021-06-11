import os
import pprint
from typing import List

from datetime import datetime
import praw
import yagmail
import time
from praw.reddit import Subreddit

# according to https://github.com/reddit-archive/reddit/wiki/API we shouldn't call the API more than 60 times a minute
# so waiting 2 seconds between API calls should be conservatively safe
seconds_to_wait_between_api_calls = 2

r = praw.Reddit('meaningful-cs-bot')

cscqSubreddit = r.subreddit('cscareerquestions')
allOfReddit = r.subreddit('all')

# newSubmissionsAsSet = set(newSubmissions)
# with open("already_covered_1.txt", "r") as f:
#     unseen = set(newSubmissions).difference(set(f.read().splitlines()))


print("howdy")


class SearchParameters:
    def __init__(self, string: str, limit: int, sort: str):
        self.string = string
        self.limit = limit
        self.sort = sort


'''
Given a subreddit and some SearchParameters, returns a dictionary with those SearchParameters as the keys
and a list of corresponding post permalinks as the values.
'''


def search_subreddit(subreddit: Subreddit, search_parameters: List[SearchParameters]):
    search_results = {}
    for search_parameter in search_parameters:
        submissions = subreddit.search(search_parameter.string, limit=search_parameter.limit,
                                       sort=search_parameter.sort)
        search_results[search_parameter] = submissions
        time.sleep(seconds_to_wait_between_api_calls)

        # for submission in submissions:
        #     print(submission.title)
        #     print(submission.permalink)
        #     pprint.pprint(vars(submission))

    return search_results


def search_and_modify(posts: dict, subreddit_name: str, search_parameters: List[SearchParameters]):
    print("Beginning search of /r/" + subreddit_name)
    posts[subreddit_name] = search_subreddit(r.subreddit(subreddit_name), search_parameters)


def find_posts():
    posts = {}

    search_and_modify(
        posts,
        'all',
        [SearchParameters("title:meaningful title:career", 10, "new"),
         SearchParameters("title:meaningful title:job", 10, "new")])

    search_and_modify(
        posts,
        'cscareerquestions',
        [SearchParameters("help society", 10, "new")])

    return posts


def create_email_message(posts: dict):
    m = ''
    for subreddit_name, searches in posts.items():
        for search_parameters, submissions in searches.items():
            permalinks = []
            for submission in submissions:
                permalinks.append(submission.permalink)
            m += "In /r/" + subreddit_name + \
                 " query \"" + search_parameters.string + \
                 "\" found:\nwww.reddit.com" + "\nwww.reddit.com".join(permalinks) + "\n"
    return m


def email_message(m2):
    # dd/mm/YY H:M:S
    date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    email_title = "Meaningful careers search " + date_and_time

    yagmail.SMTP('makeswell@gmail.com').send('maxwell.pietsch@gmail.com',
                                             email_title, m2)


def i_have_commented(a_submission):
    for comment in a_submission.comments.list():
        if comment.author == r.config.username:
            return True

    return False


if __name__ == "__main__":
    all_search_results = find_posts()
    message = create_email_message(all_search_results)
    print("Sending email with message:\n" + message)
    email_message(message)
