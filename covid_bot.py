import datetime
import os

import tweepy

from auto_tweet import AutoTweet

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
        self.dt = datetime.datetime.now()
        AutoTweet.connect_bot_api(self.api)

    def _connect_twitter_api(self):
        """Connect bot to the Twitter API"""
        auth = tweepy.OAuthHandler(CovidBot.CONSUMER_KEY,
                                    CovidBot.CONSUMER_SECRET)
        auth.set_access_token(CovidBot.ACCESS_TOKEN,
                                CovidBot.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

if __name__ == '__main__':
    covid_bot = CovidBot()