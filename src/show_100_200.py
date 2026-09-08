import numpy as np
import pandas as pd

target_columns = [
'Sentence',
]

df = pd.read_csv(
'wrime-ver2.tsv',
sep='\t',
usecols=target_columns
)

df = df.iloc[100:200]

for index, row in df.iterrows():
    sentence = row["Sentence"]
    print(f"{index}: {sentence}\n")
