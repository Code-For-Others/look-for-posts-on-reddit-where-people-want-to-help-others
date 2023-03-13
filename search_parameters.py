"""
Given a subreddit and some SearchParameters, returns a dictionary with those SearchParameters as the keys
and a list of corresponding post permalinks as the values.
"""


class SearchParameters:
    def __init__(self, query: str, sort: str = "new"):
        self.query = query
        self.sort = sort

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
    'all': [
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
            # Got a ton of false positives when we had the SearchParameters below which mention donating, so I'm commenting them out. How do we pick up posts like this one? https://old.reddit.com/r/cscareerquestions/comments/zzghe2/where_do_you_donate/
            #SearchParameters("where donate"),
            #SearchParameters("best donation"),
            #SearchParameters("choose donate"),
            #SearchParameters("choose donation"),
            #SearchParameters("pick donation"),
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
