from typing import List
from subprocess import call

from datetime import datetime

import time
from praw.reddit import Subreddit
from praw.reddit import Submission
import pprint

from main import create_bot, seconds_to_wait_between_api_calls
from search_parameters import SearchParameters
from configuration import *


class SearchResult:
    def __init__(self, subreddit_name: str, search_parameters: SearchParameters, submissions: List[Submission] = None):
        self.subreddit_name = subreddit_name
        self.search_parameters = search_parameters
        self.submissions = submissions

common_search_parameters_list = [
    SearchParameters("altruistic"),
    SearchParameters("altruist"),
    SearchParameters("title:meaningful"),
    SearchParameters("title:meaning"),
    SearchParameters("title:idealist"),
    SearchParameters("title:idealistic"),
    SearchParameters("title:charity")
]

search_parameters_list_by_subreddit_name = {
    'all': [
            SearchParameters("title:meaningful title:career"),
            SearchParameters("title:meaningful title:job"),
            SearchParameters("title:altruistic title:career"),
            SearchParameters("title:altruistic title:job"),
            SearchParameters("title:altruist title:career"),
            SearchParameters("title:altruist title:job"),
        ],

    'careerguidance': common_search_parameters_list,

    'cscareerquestions': common_search_parameters_list + [
        SearchParameters("title:volunteer"),
        SearchParameters("title:non-profit"),
        SearchParameters("title:nonprofit"),
    ],

    'personalfinance': [
            SearchParameters("title:charity"),
            SearchParameters("title:donate"),
            SearchParameters("title:nonprofit"),
            SearchParameters("title:donations"),
            SearchParameters("title:charities"),
        ],
}

r = create_bot()

def search_subreddit(subreddit_name: str, search_parameters: SearchParameters):
    subreddit: Subreddit = r.subreddit(subreddit_name)
    print('\nSearching /r/' + subreddit_name + ' for \'' + search_parameters.query +
          '\' with sort=' + str(search_parameters.sort))
    submissions_iterable = subreddit.search(search_parameters.query, sort=search_parameters.sort)
    submissions = []
    for submission in submissions_iterable:
        # only add submissions that haven't been archived,
        # because if they are archived can no longer comment on them anyways.
        # also filtering out posts that are hidden. This way I can hide posts I have already processed
        # so they are not sent to me again. Note that hidden submissions can still be accessed from the permalink
        # and are included in search results.
        if not submission.archived and not submission.hidden:
            submissions.append(submission)

    return submissions

def search(search_parameters_list_by_subreddit):
    search_results = []

    # Add any new submission from /r/Nonprofit_Jobs, unless it's a job ad
    nonprofit_jobs_submissions = []
    for submission in r.subreddit('Nonprofit_Jobs').new(limit=20):
        if not submission.archived and not submission.hidden and not submission.link_flair_text == 'Job advert':
            nonprofit_jobs_submissions.append(submission)
    search_results.append(SearchResult('Nonprofit_Jobs', None, nonprofit_jobs_submissions))

    for subreddit_name, search_parameters_list in search_parameters_list_by_subreddit.items():
        for search_parameters in search_parameters_list:
            search_result = SearchResult(subreddit_name, search_parameters)
            search_result.submissions = search_subreddit(subreddit_name, search_parameters)
            search_results.append(search_result)
            time.sleep(seconds_to_wait_between_api_calls)

    return search_results


def create_email_message(search_results: List[SearchResult]):
    m = ''
    submissions = []
    for search_result in search_results:
        for submission in search_result.submissions:
            submissions.append(submission)
    # Sort all the submissions, so it's easy for me to comment on the most recent ones. I think a non-trivial part of my impact with my comments is how quickly I comment. The quicker the better.
    submissions.sort(key=lambda submission: submission.created_utc)
    for submission in submissions:
        m += 'www.reddit.com' + submission.permalink + '\n'
    return m



def create_links_list(posts: dict):
    links = []
    for subreddit_name, search in posts.items():
        for search_parameters, submissions in search.items():
            for submission in submissions:
                links.append("www.reddit.com" + submission.permalink)
    return links


def send_email(message):
    # mm/dd/YY H:M:S
    date_and_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    email_title = "Meaningful careers search " + date_and_time

    yag.send(email_to, email_title, message)


def i_have_commented(a_submission):
    for comment in a_submission.comments.list():
        if comment.author == r.config.username:
            return True

    return False


if __name__ == "__main__":
    # 'submissions' refers to what you usually call reddit 'posts'. Praw uses the term 'submission' so I adopted it.
    search_results = search(search_parameters_list_by_subreddit_name)
    email_message = create_email_message(search_results)
    print(email_message)
    send_email(email_message)


