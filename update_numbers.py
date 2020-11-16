import os 
import datetime
import json
import re

import requests
import pandas as pd
from bs4 import BeautifulSoup
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

def get_daily_infections_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    script_tags = soup.find_all('script')
    outer_break = False
    for script in script_tags:
        for c in script.contents:
            if 'Daily New Cases' in c:
                outer_break = True
                break
        if outer_break:
            break
    matches = re.findall('\[(.+?)\]', c)
    date = matches[0].split(',')
    new_infections = matches[1].split(',')
    data = list(zip(date, new_infections))
    data = [d for d in data if d[1] != 'null']
    data = [(d[0], int(d[1])) for d in data]
    df = pd.DataFrame(data)
    print(df)

def tweet_daily_numbers(api, tweet_str):
    api.update_status(tweet_str)

if __name__ == '__main__':
    URL = "https://www.worldometers.info/coronavirus/country/us/"

    api = return_api()
    data = scrape_worldometers_data(URL)
    # tweet_str = construct_tweet(data)
    # tweet_daily_numbers(api, tweet_str)
    get_daily_infections_data(URL)
