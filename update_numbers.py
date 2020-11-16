import os 

import tweepy 

CONSUMER_KEY = os.environ.get("COVID19_TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("COVID19_TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("COVID19_TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("COVID19_TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

api.update_status('Welcome to Coronavirus News!\n\nThis is a volunteer, semi-autonomous Twitter page dedicated to centralizing and providing accurate information regarding the ongoing COVID19 health crisis.\n\nMessage me here or @ChrisGreening2 if you have any questions.')