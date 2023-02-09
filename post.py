from typing import List
from search_parameters import SearchParameters
from enum import Enum

class Usefulness(Enum):
    HIT = 1
    MISS = 2


class Post:
    def __init__(self, usefulness: Usefulness, subreddit_name: str = None, search_parameters: SearchParameters = None):
        self.usefulness = usefulness
        # subreddit_name is the subreddit where the post was found, and could for instance be 'all'
        if subreddit_name != None:
            # Not setting this if it's None, rather than setting it, because it saves some space if it's unset when serializing it to JSON. Nothing will be output if it's not set when serializing it to JSON.
            self.subreddit_name = subreddit_name
        if search_parameters != None:
            self.search_parameters = search_parameters
