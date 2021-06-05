import pandas as pd

def df_to_json(df, path):
    with open(path, 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False, orient="records")

# Read Excel sheet into dataframe
# df = pd.read_excel('wordFrequency.xlsx', sheet_name='Sheet2')

# Combine columns into a single list
# df['answers'] = df[['first', 'second']].values.tolist()
# df = df.drop(columns=['first', 'second'])