from search_parameters import SearchParameters
from typing import List
from praw.reddit import Submission

class SearchResult:
    def __init__(self, subreddit_name: str, search_parameters: SearchParameters, submissions: List[Submission] = None):
        self.subreddit_name = subreddit_name
        self.search_parameters = search_parameters
        self.submissions = submissions
