import os
from smtplib import SMTP
import praw
import yagmail
#import pprint
#from email.mime.image import MIMEImage
#from email.mime.multipart import MIMEMultipart
import smtplib
#from mailtools import SMTPMailer, ThreadedMailer
import time

r = praw.Reddit('meaningful-cs-bot')

subreddit = r.subreddit('cscareerquestions')
allOfReddit = r.subreddit('all')



#print(subreddit.title)
#print(r.config.username)
newSubmissions = []
for submission in subreddit.search("meaningful", limit=2, sort="new"):
    #print(submission.title)
    #print(submission.permalink)
    #pprint.pprint(vars(submission))
    haveCommented = False

    for comment in submission.comments.list():
        if comment.author == r.config.username:
            haveCommented = True

    newSubmissions.append(submission.permalink)

newSubmissionsAsSet = set(newSubmissions)
with open("already_covered_1.txt", "r") as f:
    unseen = set(newSubmissions).difference(set(f.read().splitlines()))


yagmail.SMTP('makeswell@gmail.com').send('maxwell.pietsch@gmail.com', 'subject2', 'This is the body2')

print("howdy")
