import re
import datetime
import os

import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from tweet import Tweet

def _get_daily_infections_data(url: str):
    """Get the daily infections data from URL and return a DataFrame"""
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

def _prepare_data(df):
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

def _create_plot(df):
    x = range(len(df))
    # x_recent = range(len(df)-7, len(df))
    plt.style.use("seaborn-darkgrid")
    plt.bar(x, df['infections'], label="Daily infections", color="black", width=1)
    # plt.bar(x_recent, [df['infections'].iloc[i] for i in x_recent])
    plt.plot(x, df['7 day rolling average'], label="7 day rolling average", color="red", linewidth=3)
    plt.title('Daily infections per Day', fontsize=24)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Daily infections', fontsize=18)
    plt.legend(loc="upper left", fontsize=18)
    plt.xticks(list(range(0, len(df), 50)), [df['date'].iloc[i] for i in range(0, len(df), 50)], rotation=10)
    fig = plt.gcf()
    fig.set_size_inches(16,9)

def get_daily_infection_plot():
    url = 'https://www.worldometers.info/coronavirus/country/us/'
    df = _get_daily_infections_data(url)
    df = _prepare_data(df)
    _create_plot(df)
    img_fpath = _save_plot()
    tweet = Tweet()
    tweet.attach_text('Daily COVID-19 infections per day')
    tweet.attach_image(img_fpath)

if __name__ == '__main__':
    url = 'https://www.worldometers.info/coronavirus/country/us/'
    df = _get_daily_infections_data(url)
    df = _prepare_data(df)
    _create_plot(df)
    img_fpath = _save_plot()
