"""
Given a subreddit and some SearchParameters, returns a dictionary with those SearchParameters as the keys
and a list of corresponding post permalinks as the values.
"""


class SearchParameters:
    def __init__(self, query: str, sort: str = "new"):
        self.query = query
        self.sort = sort
