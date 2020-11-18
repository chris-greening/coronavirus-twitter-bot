import os 
import datetime
import json
import re

import requests
import pandas as pd
from bs4 import BeautifulSoup
import tweepy 

from tweet import Tweet

def scrape_worldometers_data(url: str):
    """Return scraped Worldometers data"""
    r = requests.get(url)
    tables = pd.read_html(r.text)
    data = tables[0]
    return data.iloc[0]

def construct_tweet(data) -> str:
    todays_date = datetime.datetime.now().strftime("%A, %m/%d/%Y")
    tweet_str = (
        "United States - Daily Update\n"
        f"{todays_date}\n\n"
        f"🤢 Total Infections: {data.TotalCases:,} ({data.NewCases})\n"
        f"⚰️ Total Deaths....: {data.TotalDeaths:,} ({data.NewDeaths})\n\n"
        "Source: https://www.worldometers.info/coronavirus/country/us/\n"
        "Daily update tweeted everyday @8PM EST"
    )
    return tweet_str

def get_daily_infections_data(url: str):
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
    df = pd.DataFrame(data, columns=["date", "infections"])
    return df

def get_daily_update():
    URL = "https://www.worldometers.info/coronavirus/country/us/"
    data = scrape_worldometers_data(URL)
    tweet_str = construct_tweet(data)

    tweet = Tweet()
    tweet.attach_text(tweet_str)
    return tweet

if __name__ == '__main__':
    URL = "https://www.worldometers.info/coronavirus/country/us/"

    data = scrape_worldometers_data(URL)
    tweet_str = construct_tweet(data)
