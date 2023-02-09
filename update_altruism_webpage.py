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

# the exclusions_list contains strings that aren't allowed in the permalink of posts
exclusions_list = [
        'u_ayaankKhan562',
        'r/COMMCoin',
]

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

    SearchParameters('"help animals"'),
    SearchParameters('"make a difference"'),
    SearchParameters('"have an impact"'),
    SearchParameters('"ai safety"'),
    SearchParameters('"machine learning"'),
]

# If you include multiple 'title:' terms in a SearchParameters, only one of them actually needs to be in the title for the submission (aka post) to match.
# For instance if you have SearchParameters("title:meaningful title:career"), then either "meaningful" or "career" needs to be in the title for reddit to return it. The other term can be in the submission body.
search_parameters_list_by_subreddit_name = {
    'all-chanceme-redditserials-COMMCoin': [
            SearchParameters('"charity navigators"'),
            SearchParameters("title:meaningful title:career"),
            SearchParameters("title:meaningful title:job"),
            SearchParameters("title:altruistic title:career"),
            SearchParameters("title:altruistic title:job"),
            SearchParameters("title:altruist title:career"),
            SearchParameters("title:altruist title:job"),

            # a lot of misses for the searches below on /r/all, and I have /r/careerguidance and /r/findapath searches for these terms already, so excluding it for now
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
            SearchParameters("charity suggestions"),
            SearchParameters("charity recommendations"),

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

def create_bot():
    return praw.Reddit('meaningful-cs-bot')

r = create_bot()

SECONDS_IN_A_MONTH = 2628000.0

def search_subreddit(subreddit_name: str, search_parameters: SearchParameters):
    subreddit: Subreddit = r.subreddit(subreddit_name)
    print('Searching /r/' + subreddit_name + ' for \'' + search_parameters.query + '\' with sort=' + str(search_parameters.sort))
    # 'submissions' refers to what you usually call reddit 'posts'. Praw uses the term 'submission' so I adopted it.
    submissions_iterable = subreddit.search(search_parameters.query, sort=search_parameters.sort)
    submissions = []
    hidden_submissions = []
    for submission in submissions_iterable:

        # Sometimes I hide a submission in my Saved list, but don't unsave it. I could iterate through my Saved list and find all that are hidden and hide them. A quicker fix for now is to unsave them as I look them up.
        if submission.saved and submission.hidden:
            submission.unsave()

        #TODO it'd be cleaner to just return all submissions, and then only put the hidden ones on my webpage. I also need to add the hidden ones to storage.json, so that's why I'm returning the hidden ones too. It's late and I don't want to do this in a clean way right now, so I'm returning both lists separately.
        if submission.hidden:
            hidden_submissions.append(submission)
        
        # only add submissions that haven't been archived,
        # because if they are archived I can no longer comment on them anyways.
        # also filtering out posts that are hidden. This way I can hide posts I have already processed
        # so they are not sent to me again. Note that hidden submissions can still be accessed from the permalink
        # and are included in search results.
        if not submission.archived and not submission.hidden:

            # if the submission is older than a certain time period, I'm not saving it. The reason for this behavior is that my Saved list on Reddit can't be sorted by date, and commenting on old submissions is less effective than commenting on new ones.
            if submission.created_utc > time.time() - SECONDS_IN_A_MONTH and not submission.saved:
                submission.save(category='ea')

            submissions.append(submission)

    return hidden_submissions, submissions

def search(search_parameters_list_by_subreddit):
    search_results = []

    # Add any new submission from /r/Nonprofit_Jobs, unless it's a job ad
    nonprofit_jobs_submissions = []
    for submission in r.subreddit('Nonprofit_Jobs').new(limit=20):
        if not submission.archived and not submission.hidden and not submission.link_flair_text == 'Job advert':
            nonprofit_jobs_submissions.append(submission)
    search_results.append(SearchResult('Nonprofit_Jobs', None, nonprofit_jobs_submissions))
  
    hidden_search_results = []
    for subreddit_name, search_parameters_list in search_parameters_list_by_subreddit.items():
        for search_parameters in search_parameters_list:
            search_result = SearchResult(subreddit_name, search_parameters)
            hidden_search_result = SearchResult(subreddit_name, search_parameters)
            hidden_search_result.submissions, search_result.submissions = search_subreddit(subreddit_name, search_parameters)
            search_results.append(search_result)
            hidden_search_results.append(hidden_search_result)

    something_changed = False
    history = {}
    with open('storage.json', 'r') as storage_file:
        # history will be a dictionary
        history = json.load(storage_file)

    #TODO don't have two separate search_results. See the other TODO  in this file for more context.
    if do_stuff(search_results, history) or do_stuff(hidden_search_results, history):
        with open('storage.json', 'w') as storage_file:
            replacement_json = json.dumps(history, default=vars, indent=4)
            storage_file.write(replacement_json)

    return search_results

def do_stuff(search_results, history):
    something_changed = False
    for search_result in search_results:
        for submission in search_result.submissions:
            if submission.hidden:
                # I do like submissions besides EA submissions found through this bot on this account, so I only count the submissions which
                # I liked AND hide as 'hits'. I don't hide submissions on this account unless I found them through this bot. I hide every submission
                # which I find through this bot, so I can analyze which are the most effective searches later.
                if submission.likes == True:
                    history[submission.permalink] = Post('HIT', subreddit_name = search_result.subreddit_name, search_parameters = search_result.search_parameters)
                else:
                    history[submission.permalink] = Post('MISS', subreddit_name = search_result.subreddit_name, search_parameters = search_result.search_parameters)
                something_changed = True
    return something_changed


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
        #print('adding ' + submission.permalink + ' created ' + str(submission.created_utc))
        m += '"https://www.reddit.com' + submission.permalink + '",\n'
    return m



def create_links_list(posts: dict):
    links = []
    for subreddit_name, search in posts.items():
        for search_parameters, submissions in search.items():
            for submission in submissions:
                links.append("www.reddit.com" + submission.permalink)
    return links

def i_have_commented(a_submission):
    for comment in a_submission.comments.list():
        if comment.author == r.config.username:
            return True

    return False

pre = """let i = 0;
function openNextLinks() {
    const stepSize = 5;
    const urls = ["""
post = """];
    for (let temp = i; i < urls.length && i < temp + stepSize; i++) {
        // the "window" + i.toString() part is a trick to open multiple tabs at once on Chrome. See https://stackoverflow.com/questions/24364117/open-multiple-links-in-chrome-at-once-as-new-tabs
        window.open(urls[i], "window" + i.toString());
    }
}"""


if __name__ == "__main__":
    start_time = time.time()
    with open('/home/ubuntu/code/personal-website/urls.js', mode='w') as personal_website_file:
        search_results = search(search_parameters_list_by_subreddit_name)
        permalinks = create_permalinks_string(search_results)
        personal_website_file.write(pre + permalinks + post)
        # the line below will commit the changes made to personal_website_file to git and push them, which will cause them to show up at http://maximumpeaches.com/altruism.txt
        # btw, the reason there's a ; after the commit step is because if there's nothing to commit then it would end. this can happen if the altruism file hasn't changed.
        os.system('cd /home/ubuntu/code/personal-website && git add . && git commit -m "automatically committing"; git push origin main')
    print(os.path.basename(__file__) + " completed in %.2f seconds." % (time.time() - start_time))
