import numpy as np
import pandas as pd
import MeCab
from collections import Counter

def get_text():
    target_columns = [
        'Sentence',
    ]

    df = pd.read_csv(
        'wrime-ver2.tsv',
        sep='\t',
        usecols=target_columns
    )

    df = df.iloc[:200]

    text = ""
    for idx, row in df.iterrows():
        text += row["Sentence"]

    return text


def text2word(text):
    mecab = MeCab.Tagger()
    node = mecab.parseToNode(text)

    tokens = []
    while node:
        features = node.feature.split(",")
        if features[0] not in ["BOS/EOS", "補助記号", "空白"] and node.surface != "":
            tokens.append(node.surface)
        node = node.next

    return tokens 

# text = get_text()

target_columns = [
    'Sentence',
]

df = pd.read_csv(
    'wrime-ver2.tsv',
    sep='\t',
    usecols=target_columns
)

df = df.iloc[:200]
tokens = []
for idx, row in df.iterrows():
    #tokens.append(text2word(row["Sentence"]))
    tokens += text2word(row["Sentence"])

'''
text = "今日の月も白くて明るい。昨日より雲が少なくてキレイな〜 と立ち止まる帰り道。チャリなし生活も悪くない。"
tokens = text2word(text)
'''

freq = Counter()
for token in tokens:
    freq[token] += 1

str_dict = []
for token, cnt in freq.most_common():
    str_dict.append((token, cnt))

print(str_dict)
