# Purpose of this project

This is a personal project to find posts on Reddit that are from people seeking advice on finding a meaningful career.

A lot of this is really rough draft stuff since I'm just using it mostly for myself. If you want to help with this
project you can help me figure out better ways to advise people on how to have a meaningful career. It doesn't take
technical skills to help with that, and would help a lot potentially, just need to research.

# How to get running

In order to set up the bot for your account you can follow instructions [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps).
You will also need to create a praw.ini file in this directory that looks something like,
```ini
[meaningful-cs-bot]
client_id=
client_secret=
password=
username=
user_agent=
```

To use this project, install `python3` in your [venv](https://docs.python.org/3/tutorial/venv.html).

Create a configuration.py file that will look something like this,
```python
import yagmail

should_send_email = False
should_print_email = False
should_print_all_search_results = True
should_open_in_browser = False
should_save = False
max_number_of_links_to_open = 30
email_to='to@email.com'

yag = yagmail.SMTP('from@email.com', 'password')
```

If you want email functionality to work then install `yagmail` with `pip3 install yagmail` (maybe have to run `brew install pip3`).
Then follow [yagmail README](https://github.com/kootenpv/yagmail) to provide your email password to your keychain so
the code can use it.

Then just run the program. You can either execute,
`python3 find_submissions` to search for all the search terms, and do whatever else `configuration.py` says to do
or
`python3 unsave` to unsave all the saved submissions on your account

## How I use this
I save posts for my future self to look at, then I hide the posts to filter them out of future results.
I also upvote posts if I was able to answer in a helpful way so that later I will be able to find out which search
queries are most effective (the ones that turn up the most upvoted submissions will be most effective).