import datetime
import os
from typing import List

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

    def __init__(self):
        self.scheduled_tasks = SCHEDULED_TASK_REGISTRY
        self.dt = datetime.datetime.now()
        self._connect_twitter_api()
        ScheduledTask.connect_bot_api(self.api)
        self._build_task_queue(self.dt, self.scheduled_tasks)
        self._execute_queue()

    def _execute_queue(self):
        for task in self.task_queue:
            task.execute()

    def _build_task_queue(self, dt: datetime.datetime, scheduled_tasks: List[ScheduledTask]):
        """Get a queue of all tasks that are to be performed this run"""
        self.task_queue = tuple([task for task in scheduled_tasks if task.is_scheduled_to_run(dt)])

    def _connect_twitter_api(self):
        """Connect bot to the Twitter API"""
        auth = tweepy.OAuthHandler(CovidBot.CONSUMER_KEY,
                                    CovidBot.CONSUMER_SECRET)
        auth.set_access_token(CovidBot.ACCESS_TOKEN,
                                CovidBot.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

if __name__ == '__main__':
    # DEBUG = True
    covid_bot = CovidBot()
