# Purpose of this project

This is a personal project to find posts on Reddit that are from people seeking advice on finding a meaningful career or more effective charity.

This code is in rough draft mode because it's a pet project which only I'm using.

If you're interested in reaching out to people on reddit about how they can be more impactful or live more meaningful lives (maybe you're really into pandemic prevention, for instance, and want to scan reddit for posts about pandemic prevention to share info with others) then please reach out to me at maxwell.pietsch@gmail.com and I can set this reddit bot up to send you new posts or you can help me to figure out better ways to answer posts myself.

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

yag = yagmail.SMTP('from@email.com', 'app password')
```

(If I'm the one setting this up then I can just reuse maximumpeaches@gmail.com without setting up a new account.) You need to create a new App Password for the `from@email.com` account using [these instructions](https://support.google.com/accounts/answer/185833). It's not too hard. I created an App Password for maximumpeaches@gmail.com, i.e. `from@email.com` became `maximumpeaches@gmail.com`. After you create the App Password, you insert it (without spaces) in configuration.py where `app password` is now. It's best to use an account for `from@email.com` which doesn't have too much power in case the app password is compromised.

If you want email functionality to work then install `yagmail` with `pip3 install yagmail[all]`.  
The [yagmail README](https://github.com/kootenpv/yagmail) may help if you get stuck with emails.

Then just run the program. You can either execute,  
`python3 email_posts` to search the subreddits for all search parameters at the top of the file and then email them to you.

### Github authentication

You may want to install `gh` on the command line, and then create a new personal token using `gh auth login`. This allows you to run `git push origin main` to push your commits to the main branch.

## How I use this

I save posts for my future self to look at, then I hide the posts to filter them out of future results.  
I also upvote posts if I was able to answer in a helpful way so that later I will be able to find out which search  
queries are most effective (the ones that turn up the most upvoted submissions will be most effective).

I have cron run this daily by adding the following using `crontab -e` command,

```
0 0 * * * cd /home/ubuntu/code/reddit-meaningful-careers-bot && /usr/bin/python3 /home/ubuntu/code/reddit-meaningful-careers-bot/email_posts.py > /home/ubuntu/code/reddit-meaningful-careers-bot/output.log 2>&1
```

The `cd` command is in the crontab above because the praw.ini file is loaded from the current directory.  
I also had to install postfix when using an EC2 instance in order for the email to work, with `sudo apt install postfix`. I selected the default options when the postfix installer prompted me, and that worked.

### Generating requirements.txt

Run `pip install pipreqs && pipreqs .` to generate the requirements.txt file for everything in the directory. See [this question for more info](https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt).
