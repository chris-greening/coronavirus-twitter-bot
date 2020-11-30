import datetime
import os
from typing import List
import logging

import tweepy

from scheduled_task_registry import SCHEDULED_TASK_REGISTRY
from scheduled_task import ScheduledTask

class CovidBot:
    """
    Twitter bot designed to centralize data and news regarding the
    ongoing COVID19 pandemic.
    """
    CONSUMER_KEY = os.environ.get("COVID19_TWITTER_CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("COVID19_TWITTER_CONSUMER_SECRET")
    ACCESS_TOKEN = os.environ.get("COVID19_TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("COVID19_TWITTER_ACCESS_TOKEN_SECRET")

    def __init__(self, debug):
        self.debug = debug

        self.scheduled_tasks = SCHEDULED_TASK_REGISTRY
        self.dt = datetime.datetime.now()
        self._connect_twitter_api()
        ScheduledTask.connect_bot_api(self.api)
        ScheduledTask.set_debug(debug=self.debug)
        self._build_task_queue(self.dt, self.scheduled_tasks)
        self._execute_queue()

    def _execute_queue(self):
        for task in self.task_queue:
            task.execute()

    def _build_task_queue(self, dt: datetime.datetime, scheduled_tasks: List[ScheduledTask]):
        """Get a queue of all tasks that are to be performed this run"""
        self.task_queue = tuple([task for task in scheduled_tasks if task.is_scheduled_to_run(dt)])
        logging.info(f"Task queue built, {len(self.task_queue)} tasks scheduled")

    def _connect_twitter_api(self):
        """Connect bot to the Twitter API"""
        auth = tweepy.OAuthHandler(CovidBot.CONSUMER_KEY,
                                    CovidBot.CONSUMER_SECRET)
        auth.set_access_token(CovidBot.ACCESS_TOKEN,
                                CovidBot.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)
        logging.info("Twitter successfully authenticated")

if __name__ == '__main__':
    def log_fpath():
        now_datetime = datetime.datetime.now()
        now_date_str = now_datetime.strftime("%m%d%Y")
        hour = round_hour(now_datetime)

        fname = f"{now_date_str}-{hour}.log"
        log_folder = os.path.abspath('log')
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        return os.path.join(log_folder, fname)

    def round_hour(time):
        """Return rounded hour"""
        hour = time.hour + 1 if time.minute // 30 == 1 else time.hour
        if hour == 24:
            hour = 0
        return hour

    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(
        # stream=sys.stdout,
        format=FORMAT,
        # filename=log_file,
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(log_fpath(), encoding='utf8'),
            # logging.StreamHandler()
        ]
    )

    covid_bot = CovidBot(debug=False)
