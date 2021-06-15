from main import create_bot, seconds_to_wait_between_api_calls
import time


def unsave_all_saved_submissions():
    saved_submissions = create_bot().user.me().saved(limit=1000)
    for s in saved_submissions:
        s.unsave()
        time.sleep(seconds_to_wait_between_api_calls)


if __name__ == "__main__":
    unsave_all_saved_submissions()
    exit()
