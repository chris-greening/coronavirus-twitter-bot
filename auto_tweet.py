import datetime

from typing import List

class AutoTweet:
    def __init__(
            self,
            weekday: List[str] = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"),
            hour: List[int] = tuple(range(0,23)),
            end_of_month: bool = False
        ):
        self.weekday = weekday
        self.hour = hour
        self.end_of_month = end_of_month

    def compare_datetime(self, today_datetime):
        """Returns True if other_datetime matches the internal scheduled time"""
        today_weekday = today_datetime.strftime("%A")
        today_time = today_datetime.time()
        today_hour = self._round_hour(today_time)

        return True if today_datetime in self.weekday and today_hour in self.hour else False

    def _round_hour(self, time):
        """Return rounded hour"""
        return time.hour + 1 if time.minute // 30 ==  1 else time.hour

    @classmethod
    def connect_bot_api(cls, api):
        """Connect AutoTweetTask to Twitter API"""
        cls.api = api