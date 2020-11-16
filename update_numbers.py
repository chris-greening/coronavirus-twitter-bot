import os 
import datetime

import requests
import pandas as pd
import tweepy 

CONSUMER_KEY = os.environ.get("COVID19_TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("COVID19_TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("COVID19_TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("COVID19_TWITTER_ACCESS_TOKEN_SECRET")

def return_api():
    """Return the API"""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def scrape_worldometers_data(url):
    """Return scraped Worldometers data"""
    r = requests.get(url)
    tables = pd.read_html(r.text)
    data = tables[0]
    return data.iloc[0]

def construct_tweet(data):
    todays_date = datetime.datetime.now().strftime("%A, %m/%d/%Y")
    tweet_str = (
        f"United States - Daily Update\n"
        f"{todays_date}\n\n"
        f"🤢 Total Infections: {data.TotalCases:,} ({data.NewCases:,})\n"
        f"⚰️ Total Deaths....: {data.TotalDeaths:,} ({data.NewDeaths:,})\n\n"
        f"Source: https://www.worldometers.info/coronavirus/country/us/\n"
        f"Daily update tweeted everyday @8PM EST"
    )
    return tweet_str

def tweet_daily_numbers(api, tweet_str):
    api.update_status(tweet_str)

if __name__ == '__main__':
    URL = "https://www.worldometers.info/coronavirus/country/us/"

    api = return_api()
    data = scrape_worldometers_data(URL)
    tweet_str = construct_tweet(data)
    tweet_daily_numbers(api, tweet_str)
