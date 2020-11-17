import datetime
import os

import tweepy

class CovidBot:
    """
    Twitter bot designed to centralize data and news regarding the
    ongoing COVID19 pandemic
    """
    def __init__(self):
        self.set_datetime_metadata()

    def set_datetime_metadata(self):
        """Set metadata regarding time of day, date, and day of week"""
        current_datetime = datetime.datetime.now()

