import datetime
import logging
from typing import List

logger = logging.getLogger(__name__)

class ScheduledTask:
    """Scheduled tasks to be performed and then tweeted"""

    def __init__(
            self,
            task_function,
            weekdays: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            hours: List[int] = tuple(range(0,23)),
            end_of_month: bool = False
        ):
        """
        Parameters
        ----------
        task_function
            Function that handles the action to be taken
        weekdays : List[str]
            Days of the week this task is performed
        hours : List[int]
            Hour of the day this task is performed
        end_of_month : bool
            Run only on end of the month
        """
        self.task_function = task_function
        self.weekdays = weekdays
        self.hours = hours
        self.end_of_month = end_of_month

    def execute(self):
        tweet = self.task_function()
        if ScheduledTask.debug:
            print(tweet)
            print("-"*15)
        else:
            if tweet.image_filepath != '':
                self.api.update_with_media(tweet.image_filepath, tweet.tweet_text)
            else:
                self.api.update_status(tweet.tweet_text)
        logger.info(f"Tweeted:\n {tweet}")

    def is_scheduled_to_run(self, today_datetime):
        """
        Returns True if today_datetime matches the internal scheduled times

        Parameters
        ----------
        today_datetime : datetime.datetime
            The current datetime to be compared against this instances scheduled datetime

        Returns
        -------
        bool
            True if this task is scheduled for now else False
        """
        today_weekday = today_datetime.strftime("%A")
        today_time = today_datetime.time()
        today_hour = self._round_hour(today_time)

        #Special case if it's the end of the month
        if self.end_of_month:
            if self._is_end_of_month(today_datetime) and today_hour in self.hours:
                return True
        return True if today_weekday in self.weekdays and today_hour in self.hours else False

    def _is_end_of_month(self, dt):
        """Return True if the date is the end of the month"""
        todays_month = dt.month
        tomorrows_month = (dt + datetime.timedelta(days=1)).month
        return True if tomorrows_month != todays_month else False

    def _round_hour(self, time):
        """Return rounded hour"""
        hour = time.hour + 1 if time.minute // 30 ==  1 else time.hour
        if hour == 24:
            hour = 0
        return hour

    @classmethod
    def connect_bot_api(cls, api):
        """Connect AutoTweetTask to Twitter API"""
        cls.api = api

    @classmethod
    def set_debug(cls, debug: bool) -> None:
        cls.debug = debug
