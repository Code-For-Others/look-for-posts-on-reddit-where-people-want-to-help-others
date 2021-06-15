There is a good amount of traffic in /r/careerguidance. It'd make sense to search for the same terms there as on
other career-specific subreddits, like /r/cscareerquestions, and then more specific terms in /r/all.
For instance searching for "meaningful" in /r/careerguidance, but searching for "title:meaningful title:career" in
/r/all. This helps keep the search both broad enough to find relevant posts, but narrow enough to reduce the number
of false positives.

some career-related subreddits:
/r/careerguidance
/r/findapath
/r/LifeAfterSchool
/r/LawFirm
/r/HowsYourJob
/r/Meaningfulcareer

I searched through /r/cscareerquestions for different keywords.
Some that turned up things:
"altruistic"
almost all searches for "altruistic" were not false positives, but not too many results showed up.
"help society" - turned up a few actually. could also try "helps society" and "give back to society"
"give back" turned up a few, but some false positives (although not many false positives in absolute terms)
"meaningful"
just searching for "meaningful" sort by new in /r/cscareerquestions turned up a huge number of false positives (I went through about 30 and only saw false positives)
searching for "title:meaningful" sort by new in /r/cscareerquestions turned up much fewer results, but roughly 50% were what I was looking for.
searching for "title:meaning" sort by new in /r/cscareerquestions turned up few results but around 50% were false positives so that was good.
searching for "meaningful" sort by *relevance* in /r/cscareerquestions turned up good ones, at least the first couple results, but they overlapped with "title:meaningful" and "title:meaning" searches when they were what I was looking for, anyways, so probably not necessary, but could try it at some future time.
not many results from searching "title:idealist" and "title:idealistic" in /r/cscareerquestions+careerguidance but also very few false positives so I would include them.
got fewer false positives from searching "meaningful" in /r/careerguidance sorted by new, compared with the same search in /r/cscareerquestions, but still much fewer false positives by just searching for "title:meaningful" instead, or "meaningful" and then sort by relevance. (I think sort by relevance just sorts them at the top if they have the search term in the title anyways.)

"artificial intelligence phd" and "machine learning phd" turned up quite a few in /r/cscareerquestions, 
but not /r/ExperiencedDevs, which makes sense since the former consists of younger folks
"purpose" turned up a few I wouldn't've found otherwise. Relatively lots of false positives, but not so many I couldn't just ignore if they came to me.
"meaning" also turned up a few I wouldn't've found otherwise, with relatively high false positives.

Ok so one thing to note is that I had trouble searching for "give back" where the two words have to be placed together.
When I searched "give back" using praw, I got results that had "give" and "back" not occurring next to each other.
I also looked at [the reddit search doc](https://www.reddit.com/wiki/search) and didn't see any tricks to get this to
work, so it may just not be possible using praw, at least. I was able to find posts only when "give" and "back" are
adjacent by using the search functionality manually on reddit, so it is definitely possible somehow (maybe have a
script that opens a browser) but is not super easy to do.

/r/meaningfulcareer is pretty much empty
I found a bunch of posts by searching all of reddit for "meaningful career" (without the quotes),
but when I sorted by "new" instead of "relevant" there were a ton of false positives.
So one tactic is to search all of reddit for "meaningful career" in order to find subreddits where people typically
ask these questions.
Another trick is to search for "title:meaningful title:career" to just turn up posts which have "meaningful" and
"career" in the title itself. This did help to whittle down the results to a much more relevant bunch.
Search terms for all of reddit:
"title:meaningful title:career"
"title:meaningful title:job"
"title:altruistic title:career" 
"title:altruistic title:job"
Another thing that would be nice is to be able to manually enter a search string, and then this script would be able
to run it and compare the results to posts I have already processed.
It would also make sense to work backwards in the sense of finding careers that can be massively beneficial, and then
making sure that posts on reddit by people who can do them are found by this project.

Also the final version of this code should have something like `reddit.subreddit("redditdev+learnpython+botwatch")`
so can search multiple subreddits at once if they have the same search terms, to reduce number of needed API calls.