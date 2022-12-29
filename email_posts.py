from typing import List
from subprocess import call

from datetime import datetime

import time
from datetime import datetime
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

career_subreddit_search_parameters_list = [
    SearchParameters('"help others"'),
    SearchParameters('"help people"'),
    SearchParameters('altruistic'),

    # some posts do just say 'social impact', but a lot of misses when you search for this phrase too, it seems
    # also search parameters like "doctor", "medical school", "software engineer", etc. all turn up at least some relevant posts, but
    # the hit / miss ratio might keep you from working on other stuff b/c you have to sort through all the junk to find them.
    #SearchParameters('"social impact"')

    SearchParameters('"help animals"')
]

# If you include multiple 'title:' terms in a SearchParameters, only one of them actually needs to be in the title for the submission (aka post) to match.
# For instance if you have SearchParameters("title:meaningful title:career"), then either "meaningful" or "career" needs to be in the title for reddit to return it. The other term can be in the submission body.
search_parameters_list_by_subreddit_name = {
    'all': [
            SearchParameters("title:meaningful title:career"),
            SearchParameters("title:meaningful title:job"),
            SearchParameters("title:altruistic title:career"),
            SearchParameters("title:altruistic title:job"),
            SearchParameters("title:altruist title:career"),
            SearchParameters("title:altruist title:job"),

            # not getting great results for "help people" search (see 12/25/22 metrics) so excluding it for now
            #SearchParameters('title:"help others" title:job'),
            #SearchParameters('title:"help others" title:career'),
            #SearchParameters('title:"help others" title:work'),
            #SearchParameters('"help people" title:job'),
            #SearchParameters('"help people" title:career'),
            #SearchParameters('"help people" title:work'),

            # For some reason, reddit doesn't really do searches for 3 words the way you'd expect, so I usually just put two of the words in quotes, like below.
            SearchParameters('"animal abuse" title:career'),
            SearchParameters('"animal abuse" title:work'),
            SearchParameters('"animal abuse" title:job'),

            SearchParameters('"animal rights" title:career'),
            SearchParameters('"animal rights" title:job'),
            SearchParameters('"animal rights" title:work'),

            SearchParameters("title:best title:charity"),
            SearchParameters("title:trust title:charity"),
            SearchParameters("title:pick title:charity"),
            SearchParameters("title:choose title:charity"),
            SearchParameters("title:effective title:charity"),
            SearchParameters("title:scam title:charity"),

            SearchParameters("title:donate title:money"),
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
    'college': [
        SearchParameters('"pick major" title:altruistic'),
        ],
    'vegan': [
            SearchParameters('title:career'),
            SearchParameters('title:job'),
            SearchParameters('title:profession'),
            SearchParameters('title:charity'),
            ],
    'findapath': career_subreddit_search_parameters_list,
    'careerguidance': career_subreddit_search_parameters_list,
}

r = create_bot()

def search_subreddit(metrics_file, subreddit_name: str, search_parameters: SearchParameters):
    subreddit: Subreddit = r.subreddit(subreddit_name)
    searching = '\nSearching /r/' + subreddit_name + ' for \'' + search_parameters.query + '\' with sort=' + str(search_parameters.sort) + '\n'
    print(searching)
    log = searching
    # 'submissions' refers to what you usually call reddit 'posts'. Praw uses the term 'submission' so I adopted it.
    submissions_iterable = subreddit.search(search_parameters.query, sort=search_parameters.sort)
    submissions = []
    hidden_count = 0
    upvoted_count = 0
    for submission in submissions_iterable:
        # only add submissions that haven't been archived,
        # because if they are archived can no longer comment on them anyways.
        # also filtering out posts that are hidden. This way I can hide posts I have already processed
        # so they are not sent to me again. Note that hidden submissions can still be accessed from the permalink
        # and are included in search results.
        # if submission.likes == None then I haven't upvoted or downvoted them yet. I'm using upvoting as a way to signal that
        # the submission is the kind of submission I'm looking for.
        if not submission.archived and not submission.hidden and submission.likes == None:
            submissions.append(submission)
            # add the permalinks to the log, so we know from which SearchParameter each permalink originated
            log += submission.permalink + '\n'

        if submission.hidden:
            hidden_count += 1

        # I do like submissions besides EA submissions found through this bot on this account, so I only count the submissions which
        # I liked AND hide. I don't hide submissions on this account unless I found them through this bot. I hide every submission
        # which I find through this bot, so I can analyze which are the most effective searches later.
        if submission.hidden and submission.likes == True:
            upvoted_count += 1

    
    metrics_file.write('successes ' + str(upvoted_count) + ' and misses ' + str(hidden_count) + ' for ' + subreddit_name + ', ' + search_parameters.query + ', sort=' + str(search_parameters.sort) + '\n')

    return (log, submissions)

def search(metrics_file, search_parameters_list_by_subreddit):
    search_results = []

    # Add any new submission from /r/Nonprofit_Jobs, unless it's a job ad
    nonprofit_jobs_submissions = []
    for submission in r.subreddit('Nonprofit_Jobs').new(limit=20):
        if not submission.archived and not submission.hidden and not submission.link_flair_text == 'Job advert':
            nonprofit_jobs_submissions.append(submission)
    search_results.append(SearchResult('Nonprofit_Jobs', None, nonprofit_jobs_submissions))
    time.sleep(seconds_to_wait_between_api_calls)

    log = ''
    for subreddit_name, search_parameters_list in search_parameters_list_by_subreddit.items():
        for search_parameters in search_parameters_list:
            search_result = SearchResult(subreddit_name, search_parameters)
            (l, search_result.submissions) = search_subreddit(metrics_file, subreddit_name, search_parameters)
            log += l
            search_results.append(search_result)
            time.sleep(seconds_to_wait_between_api_calls)

    return (log, search_results)


def create_email_message(log, search_results: List[SearchResult]):
    m = ''
    submissions = []
    for search_result in search_results:
        for submission in search_result.submissions:
            # only add them once so the final list doesn't contain duplicates
            if submission not in submissions:
                submissions.append(submission)
    # Sort all the submissions, so it's easy for me to comment on the most recent ones. I think a non-trivial part of my impact with my comments is how quickly I comment. The quicker the better.
    submissions.sort(key=lambda submission: submission.created_utc, reverse=True)
    for submission in submissions:
        print('adding ' + submission.permalink + ' created ' + str(submission.created_utc))
        m += 'www.reddit.com' + submission.permalink + '\n'
    m += '\nlogs are:\n' + log
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
    metrics_filename = 'metrics_' + datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
    with open('./metrics/' + metrics_filename, mode='w') as metrics_file:
        with open('log_from_email_posts.txt', encoding='utf-8', mode='w') as f:
            # log contains useful debugging info
            (log, search_results) = search(metrics_file, search_parameters_list_by_subreddit_name)
            email_message = create_email_message(log, search_results)
            f.write(log)
            send_email(email_message)
    print('wrote metrics to ./metrics/' + metrics_filename)
