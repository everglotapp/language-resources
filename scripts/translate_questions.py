import os
import csv
import pandas as pd
import uuid
import argparse
from pathlib import Path
import json
import requests

DEEPL_API_KEY = ''
LANGS = ['ES', 'FR', 'IT', 'PT-PT', 'RU', 'JA']

def deepl_translate(sentence, target_lang):
    response = requests.post(url='https://api-free.deepl.com/v2/translate',
                          data = {
                            'target_lang' : target_lang,  
                            'auth_key' : DEEPL_API_KEY,
                            'text': sentence
                          })
    r = json.loads(response.text)
    translated = r['translations'][0]['text']
    return translated

def df_to_json(df, path):
    with open(path, 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False, orient="records")

def translate_random_questions(target_lang):
    df = pd.read_json('../resources/random_questions_en.json', orient='records')
    new_df = pd.DataFrame()
    new_df['question'] = df.apply(lambda row: deepl_translate(row['question'], target_lang.upper()), axis=1)
    print(new_df)
    df_to_json(new_df, f'../resources/random_questions_{target_lang.lower()}.json')

def translate_would_you_rather(target_lang):
    df = pd.read_json('./resources/would_you_rather_questions_en.json', orient='records')
    new_df = pd.DataFrame()
    new_df['question'] = df.apply(lambda row: deepl_translate(row['question'], target_lang.upper()), axis=1)
    new_df['answers'] = df.apply(lambda row: translate_list(row['answers'], target_lang.upper()), axis=1)
    print(new_df)
    df_to_json(new_df, f'./resources/would_you_rather_questions_{target_lang.lower()}.json')

if __name__ == "__main__":
    for lang in LANGS:
        translate_random_questions(lang)
        translate_would_you_rather(lang)