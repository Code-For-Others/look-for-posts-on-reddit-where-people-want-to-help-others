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

from search_result import SearchResult
from search_parameters import SearchParameters
from search_parameters import search_parameters_list_by_subreddit_name

# the exclusions_list contains strings that aren't allowed in the permalink of posts
exclusions_list = [
        'u_ayaankKhan562',
        'r/COMMCoin',
]

# local can be set to True so that you won't use Google Cloud features
local = True
# only_vegan_subreddit can be set to True when testing so that the test doesn't iterate through every subreddit and therefore completes faster
only_vegan_subreddit = False

def access_secret_version(client, version_id):
    return client.access_secret_version(request={'name':version_id}).payload.data.decode('UTF-8')

if local:
    r = praw.Reddit('meaningful-cs-bot')
else:
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    r = praw.Reddit(
            client_id = access_secret_version(client, 'projects/868719180965/secrets/praw_client_id/versions/1'),
            client_secret = access_secret_version(client, 'projects/868719180965/secrets/praw_client_secret/versions/1'),
            password = access_secret_version(client, 'projects/868719180965/secrets/praw_password/versions/1'),
            user_agent = access_secret_version(client, 'projects/868719180965/secrets/praw_user_agent/versions/1'),
            username = access_secret_version(client, 'projects/868719180965/secrets/praw_username/versions/1')
    )

def search_subreddit(subreddit_name: str, search_parameters: SearchParameters):
    if only_vegan_subreddit and subreddit_name != 'vegan':
        return []
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
    # Sort all the submissions, so it's easy for us to comment on the most recent ones. I think a non-trivial part of our impact with my comments is how quickly we comment. The quicker the better.
    submissions.sort(key=lambda submission: submission.created_utc, reverse=True)
    for submission in submissions:
        m += 'https://www.reddit.com' + submission.permalink + '\n'
    return m

def write_to_storage(local, permalinks):
    if local:
        print('permalinks:\n' + permalinks)
    else:
        from google.cloud import storage
        storage_client = storage.Client()
        bucket = storage_client.bucket('latestpermalinks')
        blob = bucket.blob('allpermalinks')
        print('writing permalinks to latestpermalinks/allpermalinks in Cloud Storage')
        with blob.open("w") as f:
            f.write(permalinks)

def scan_reddit(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    start_time = time.time()
    search_results = search(search_parameters_list_by_subreddit_name)
    permalinks = create_permalinks_string(search_results)
    write_to_storage(local, permalinks)
    print(os.path.basename(__file__) + " completed in %.2f seconds." % (time.time() - start_time))

if local:
    scan_reddit(None, None)
