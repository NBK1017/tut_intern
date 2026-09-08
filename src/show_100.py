import pandas as pd

target_columns = [
'Sentence',
'Writer_Joy',
'Writer_Sadness',
'Writer_Anticipation',
'Writer_Surprise',
'Writer_Anger',
'Writer_Fear',
'Writer_Disgust',
'Writer_Trust',
'Writer_Sentiment'
]

df = pd.read_csv(
'wrime-ver2.tsv',
sep='\t',
nrows=100,
usecols=target_columns
)

angry_cnt = 0
for index, row in df.iterrows():
    if row["Writer_Joy"] != 0:
        angry_cnt += 1
    sentence = row['Sentence']
    sadness_score = row['Writer_Sadness']
    print(f'{index}:{sentence}\n')

print(f"angry_cnt:{angry_cnt}")
