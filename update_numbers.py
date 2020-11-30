import os 
import datetime
import json
import re

import requests
import pandas as pd
from bs4 import BeautifulSoup
import tweepy 

from tweet import Tweet

def get_daily_update() -> Tweet:
    """Return Tweet containing daily update on Infection and Death numbers"""
    URL = "https://www.worldometers.info/coronavirus/country/us/"
    data = _scrape_worldometers_data(URL)
    tweet_str = _construct_tweet_str(data)

    tweet = Tweet()
    tweet.attach_text(tweet_str)
    return tweet

def _scrape_worldometers_data(url: str) -> pd.Series:
    """Return scraped Worldometers data"""
    r = requests.get(url)
    tables = pd.read_html(r.text)
    data = tables[0]
    return data.iloc[0]

def _construct_tweet_str(scraped_data: pd.Series) -> str:
    """Return the Tweet text constructed from the scraped data"""
    todays_date = datetime.datetime.now().strftime("%A, %m/%d/%Y")
    tweet_str = (
        "United States - Daily Update\n"
        f"{todays_date}\n\n"
        f"🤢 Total Infections: {_format_data_str(scraped_data.TotalCases, scraped_data.NewCases)}\n"
        f"⚰️ Total Deaths....: {_format_data_str(scraped_data.TotalDeaths, scraped_data.NewDeaths)}\n\n"
        "Source: https://www.worldometers.info/coronavirus/country/us/\n"
        "Daily update tweeted everyday @8PM EST"
    )
    return tweet_str

def _format_data_str(total: str, new: str) -> str:
    total_str = f"{int(total):,}"

    new_num_str = str(new)
    new_num_str = new_num_str.split('.')[0]
    new_num_str = new_num_str.replace("+", "")
    new_num_str = new_num_str.replace(",", "")
    new_str = f"+{int(new_num_str):,}"

    return f"{total_str} ({new_str})"

if __name__ == '__main__':
    URL = "https://www.worldometers.info/coronavirus/country/us/"

    data = _scrape_worldometers_data(URL)
    tweet_str = _construct_tweet_str(data)
