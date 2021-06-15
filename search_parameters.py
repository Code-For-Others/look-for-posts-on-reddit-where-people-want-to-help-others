"""
Given a subreddit and some SearchParameters, returns a dictionary with those SearchParameters as the keys
and a list of corresponding post permalinks as the values.
"""


class SearchParameters:
    def __init__(self, string: str, limit: int = None, sort: str = "new"):
        self.string = string
        self.limit = limit
        self.sort = sort
