from datetime import datetime
from configuration import *


def send_email(message):
    # mm/dd/YY H:M:S
    date_and_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    email_title = "Meaningful careers search " + date_and_time

    yag.send(email_to, email_title, message)

if __name__ == "__main__":
    send_email('New meaningful careers / best charities results available at:\nhttp://maximumpeaches.com/altruism.txt')

