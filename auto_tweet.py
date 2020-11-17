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

    def compare_datetime(self, other_datetime):
        """Returns True if other_datetime matches the internal scheduled time"""
        pass

    @classmethod
    def connect_to_api(cls, api):
        """Connect AutoTweetTask to Twitter API"""
        cls.api = api