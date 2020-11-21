import re
import datetime
import os

import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from tweet import Tweet

def get_daily_infection_plot():
    url = 'https://www.worldometers.info/coronavirus/country/us/'
    df = _get_daily_infections_data(url)
    df = _prepare_data(df)
    _create_plot(df)
    img_fpath = _save_plot()
    tweet = Tweet()
    todays_date = datetime.datetime.now().strftime("%m/%d/%Y")
    tweet_str = (
        "United States - Infections per Day\n"
        f"{todays_date}\n"
        "https://www.worldometers.info/coronavirus/country/us/"
    )
    tweet.attach_text(tweet_str)
    tweet.attach_image(img_fpath)
    return tweet

def _get_daily_infections_data(url: str) -> pd.DataFrame:
    """Return a DataFrame containing scraped dates vs. daily infections"""

    #Parse all script tags from the URL's source code
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    script_tags = soup.find_all('script')

    #Loop through contents of script tags and find the one w Daily New Cases
    outer_break = False
    for script in script_tags:
        for c in script.contents:
            if 'Daily New Cases' in c:
                outer_break = True
                break
        if outer_break:
            break

    #Parse JavaScript array out of script tag
    matches = re.findall('\[(.+?)\]', c)
    dates = matches[0].split(',')
    new_infections = matches[1].split(',')

    #Zip data, remove null data points, and convert to pandas DataFrame
    data = list(zip(dates, new_infections))
    data = [d for d in data if d[1] != 'null']
    data = [(d[0], int(d[1])) for d in data]
    df = pd.DataFrame(data, columns=["date", "infections"])
    return df

def _prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return dataframe with processed data ready to be plotted"""
    df['date'] = df['date'].str.replace('"', '')
    df['7 day rolling average'] = df['infections'].rolling(window=7).mean()
    return df

def _save_plot():
    """Return fpath of the saved plot"""
    folder_fpath = os.path.abspath('plots')
    if not os.path.exists(folder_fpath):
        os.mkdir(folder_fpath)
    date_str = datetime.datetime.now().strftime("%m%d%Y")
    img_name = f'infections {date_str}.png'
    img_fpath = os.path.join(folder_fpath, img_name)
    plt.savefig(img_fpath)
    return img_fpath

def _create_plot(df: pd.DataFrame):
    """Create plot from scraped DataFrame"""
    x = range(len(df))
    plt.style.use("seaborn-darkgrid")
    plt.bar(x, df['infections'], label="Daily infections",
            color="black", width=1)
    plt.plot(x, df['7 day rolling average'],
             label="7 day rolling average", color="red", linewidth=4)
    _draw_plot_metadata()

def _draw_plot_metadata():
    """Draw all metadata for the plot"""
    date = datetime.datetime.now().strftime('%m/%d/%Y')
    plt.title(f'Daily COVID-19 cases as of {date}', fontsize=32)
    plt.xlabel('Date', fontsize=32)
    plt.ylabel('Daily infections', fontsize=32)
    plt.legend(loc="upper left", fontsize=32)
    plt.xticks(list(range(0, len(df), 50)), [
               df['date'].iloc[i] for i in range(0, len(df), 50)], rotation=10, fontsize=24)
    fig = plt.gcf()
    fig.set_size_inches(16, 9)

if __name__ == '__main__':
    url = 'https://www.worldometers.info/coronavirus/country/us/'
    df = _get_daily_infections_data(url)
    df = _prepare_data(df)
    _create_plot(df)
    img_fpath = _save_plot()
