import datetime
import os

import tweepy

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
        self._connect_twitter_api()
        self._set_datetime_metadata()

    def _connect_twitter_api(self):
        """Connect bot to the Twitter API"""
        auth = tweepy.OAuthHandler(CovidBot.CONSUMER_KEY,
                                    CovidBot.CONSUMER_SECRET)
        auth.set_access_token(CovidBot.ACCESS_TOKEN,
                                CovidBot.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def _set_datetime_metadata(self):
        """Set metadata regarding time of day, date, and day of week"""
        current_datetime = datetime.datetime.now()
        self.time = current_datetime.time()
        self.date = current_datetime.date()
        # hour = (time.replace(second=0, microsecond=0, minute=0, hour=time.hour)
        #        + datetime.timedelta(hours=time.minute//30))
        self.weekday = self.date.strftime('%A')

if __name__ == '__main__':
    covid_bot = CovidBot()