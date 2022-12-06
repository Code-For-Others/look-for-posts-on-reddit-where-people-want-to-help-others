# Purpose of this project

This is a personal project to find posts on Reddit that are from people seeking advice on finding a meaningful career.

A lot of this is really rough draft stuff since I'm just using it mostly for myself. If you want to help with this  
project you can help me figure out better ways to advise people on how to have a meaningful career. It doesn't take  
technical skills to help with that, and would help a lot potentially, just need to research.

# How to get running

I can access my EC2 instance using my AWS account and [these instructions](https://docs.google.com/document/d/1VNgxYC3Xxcf0tzRThDEE2TUG6_OtVBFB9tppjFUAmtQ/edit) which has this bot running on it.

In order to set up the bot for your account you can follow instructions [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps).

Might want to install python3 in your [venv](https://docs.python.org/3/tutorial/venv.html).  
If `pip3` isn't available on the command line then install it with `brew install pip3` or `sudo apt install pip3` or something similar.  
Run `pip3 install praw`.  
Create a praw.ini file in this directory that looks something like,

```ini
[meaningful-cs-bot]
client_id=
client_secret=
password=
username=
user_agent='look up careers by /u/Max_Pietsch v1.0'
```

Create a configuration.py file that looks like this,

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

You need to create a new App Password for the `from@email.com` account using [these instructions](https://support.google.com/accounts/answer/185833). It's not too hard. I created an App Password for maxdicksize@gmail.com, i.e. `from@email.com` became `maxdicksize@gmail.com`. You may want to reuse maxdicksize@gmail.com for this purpose. After you create the App Password, you insert it in configuration.py where `password` is now.

If you want email functionality to work then install `yagmail` with `pip3 install yagmail[all]`.
The [yagmail README](https://github.com/kootenpv/yagmail) may help if you get stuck with emails.

Then just run the program. You can either execute,  
`python3 email_posts` to search the subreddits for all search parameters at the top of the file and then email them to you.

## How I use this

I save posts for my future self to look at, then I hide the posts to filter them out of future results.  
I also upvote posts if I was able to answer in a helpful way so that later I will be able to find out which search  
queries are most effective (the ones that turn up the most upvoted submissions will be most effective).

I have cron run this daily by adding the following using `crontab -e` command,
You have to cd because it loads the praw.ini file which is in that directory.

```
* * * * * cd /home/ubuntu/code/reddit-meaningful-careers-bot && /usr/bin/python3 /home/ubuntu/code/reddit-meaningful-careers-bot/email_posts.py > /home/ubuntu/code/reddit-meaningful-careers-bot/output.log 2>&1
```
