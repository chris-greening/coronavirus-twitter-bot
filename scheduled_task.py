import datetime

from typing import List

class ScheduledTask:
    """Scheduled tasks to be performed and then tweeted"""

    def __init__(
            self,
            action,
            weekdays: List[str] = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"),
            hours: List[int] = tuple(range(0,23)),
            end_of_month: bool = False
        ):
        """
        Parameters
        ----------
        action
            Function that handles the action to be taken
        weekdays : List[str]
            Days of the week this task is performed
        hours : List[int]
            Hour of the day this task is performed
        end_of_month : bool
            Run only on end of the month
        """
        self.action = action
        self.weekdays = weekdays
        self.hours = hours
        self.end_of_month = end_of_month

    def perform_action(self):
        tweet = self.action()
        self.api.update_status(tweet.tweet_text)

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
        if self._is_end_of_month(today_datetime) and today_hour in self.hours:
            return True

        return True if today_weekday in self.weekdays and today_hour in self.hours else False

    def _is_end_of_month(self, dt):
        """Return True if the date is the end of the month"""
        todays_month = dt.month
        tomorrows_month = (dt + datetime.timedelta(days=1)).month
        return True if tomorrows_month == todays_month else False

    def _round_hour(self, time):
        """Return rounded hour"""
        return time.hour + 1 if time.minute // 30 ==  1 else time.hour

    @classmethod
    def connect_bot_api(cls, api):
        """Connect AutoTweetTask to Twitter API"""
        cls.api = api
