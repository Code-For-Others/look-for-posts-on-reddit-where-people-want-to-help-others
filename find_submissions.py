from typing import List
from subprocess import call

from datetime import datetime

import yagmail
import time
from praw.reddit import Subreddit
import pprint

from main import create_bot, seconds_to_wait_between_api_calls
from search_parameters import SearchParameters
from configuration import *


search_terms_a = [
    SearchParameters("altruistic"),
    SearchParameters("altruist"),
    SearchParameters("title:meaningful"),
    SearchParameters("title:meaning"),
    SearchParameters("title:idealist"),
    SearchParameters("title:idealistic"),
    SearchParameters("title:non-profit"),
    SearchParameters("title:nonprofit"),
    SearchParameters("title:charity")
];

searches = {
    # 'all': [
    #         SearchParameters("title:meaningful title:career"),
    #         SearchParameters("title:meaningful title:job"),
    #         SearchParameters("title:altruistic title:career"),
    #         SearchParameters("title:altruistic title:job"),
    #     ],

    'careerguidance': search_terms_a,

    'cscareerquestions': search_terms_a + [
        SearchParameters("volunteer")
    ],
}

r = create_bot()


def search_subreddit(subreddit_name: str, search_parameters: List[SearchParameters]):
    print("Beginning search of /r/" + subreddit_name)
    search_results = {}
    subreddit: Subreddit = r.subreddit(subreddit_name)
    number_saved_for_this_subreddit = 0
    for search_parameter in search_parameters:
        number_saved_for_this_search_query = 0
        print('\nsearching /r/' + subreddit_name + ' for \'' + search_parameter.string +
              '\' with limit=' + str(search_parameter.limit) + ' and sort=' + str(search_parameter.sort))
        if search_parameter.limit is None:
            submissions_iterable = subreddit.search(search_parameter.string, sort=search_parameter.sort)
        else:
            submissions_iterable = subreddit.search(search_parameter.string, limit=search_parameter.limit,
                                                    sort=search_parameter.sort)
        submissions = []
        for submission in submissions_iterable:
            if should_print_all_search_results:
                print(submission.permalink)
                # pprint.pprint(vars(submission))
                # print(submission.title)
            # only add submissions that haven't been archived,
            # because if they are archived can no longer comment on them anyways.
            # also filtering out posts that are hidden. This way I can hide posts I have already processed
            # so they are not sent to me again. Note that hidden submissions can still be accessed from the permalink
            # and are included in search results.
            if not submission.archived and not submission.hidden:
                submissions.append(submission)
                if should_save and not submission.saved:
                    submission.save()
                    number_saved_for_this_subreddit += 1
                    number_saved_for_this_search_query += 1
                    time.sleep(seconds_to_wait_between_api_calls)
            # else:
            # print('filtering out: ' + submission.permalink)
            # pprint.pprint(vars(submission))
        search_results[search_parameter] = submissions
        print('number saved for this search query: ' + str(number_saved_for_this_search_query))
        time.sleep(seconds_to_wait_between_api_calls)

    print('number saved for this subreddit: ' + str(number_saved_for_this_subreddit))
    return search_results


def search_and_modify(posts: dict, subreddit_name: str, search_parameters: List[SearchParameters]):
    posts[subreddit_name] = search_subreddit(subreddit_name, search_parameters)


def find_posts():
    posts = {}

    for subreddit_name, search_parameters in searches.items():
        search_and_modify(posts, subreddit_name, search_parameters)

    return posts


def create_email_message(posts: dict):
    m = ''
    for subreddit_name, search in posts.items():
        for search_parameters, submissions in search.items():
            permalinks = []
            likes = 0
            for submission in submissions:
                permalinks.append(submission.permalink)
                if submission.likes:
                    likes += 1
            if len(permalinks) > 0:
                m += "In /r/" + subreddit_name + \
                     " query \"" + search_parameters.string + \
                     "\"\n" + \
                     "I liked " + str(round(likes / len(permalinks) * 100)) + "% of " + str(len(permalinks)) + \
                     "\nwww.reddit.com" + "\nwww.reddit.com".join(permalinks) + "\n"
            else:
                m += "In /r/" + subreddit_name + \
                     " query \"" + search_parameters.string + \
                     "\" found nothing."
    return m


def create_links_list(posts: dict):
    links = []
    for subreddit_name, search in posts.items():
        for search_parameters, submissions in search.items():
            for submission in submissions:
                links.append("www.reddit.com" + submission.permalink)
    return links


def send_email(m2):
    # dd/mm/YY H:M:S
    date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    email_title = "Meaningful careers search " + date_and_time

    yagmail.SMTP(email_from).send(email_to, email_title, m2)


def i_have_commented(a_submission):
    for comment in a_submission.comments.list():
        if comment.author == r.config.username:
            return True

    return False


if __name__ == "__main__":
    all_search_results = find_posts()

    if should_open_in_browser:
        i = 0
        for link in create_links_list(all_search_results):
            call(["open", "http://" + link])
            if i > max_number_of_links_to_open:
                break
            time.sleep(seconds_to_wait_between_api_calls)
            i += 1
    message = create_email_message(all_search_results)
    if should_print_email:
        print(message)
    if should_send_email:
        send_email(message)
