import pandas as pd
from datetime import datetime

def df_to_json(df, path):
    with open(path, 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False, orient="records")

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return int(unix_time(dt) * 1000)

# Read Excel sheet into dataframe
# df = pd.read_excel('wordFrequency.xlsx', sheet_name='Sheet2')

# Combine columns into a single list
# df['answers'] = df[['first', 'second']].values.tolist()
# df = df.drop(columns=['first', 'second'])