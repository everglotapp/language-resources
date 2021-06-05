# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
from utils import df_to_json
import pandas as pd

WEB_URL = 'https://en.wiktionary.org/wiki/User:Matthias_Buchmeier/German_frequency_list-1-5000'
ACCEPTED_SYMBOLS = "[^A-Za-zöäßüÜÄÖ]"

def download_words(url):
    html = urlopen(url).read()
    bs = BeautifulSoup(html)
    worddiv = bs.find('div', { 'class': "mw-parser-output" })
    data = worddiv.p.text
    return data

def process_data(data):
    # Split words into list
    freq_list = [x.split(' ') for x in data.split('\n')]

    # Remove bad rows
    for pair in freq_list:
        if len(pair) != 2:
            freq_list.remove(pair)

    # Convert to pandas dataframe
    df = pd.DataFrame(freq_list)
    df.columns = ['frequency', 'word']

    # Remove rows containing undesired symbols
    df = df[~df.word.str.contains(ACCEPTED_SYMBOLS, regex=True, na=False)]

    # Remove duplicate words, case insensitive
    df['word_2'] = df['word'].str.strip()
    df['word_2'] = df['word'].str.lower()
    df.drop_duplicates(subset=['word_2'], inplace=True, keep="first")
    df.drop(columns='word_2', inplace=True)
    df.reset_index(inplace=True, drop=True)

    return df

if __name__ == "__main__":
    words = download_words(WEB_URL)
    df = process_data(words)
    df_to_json(df, "de.json")


