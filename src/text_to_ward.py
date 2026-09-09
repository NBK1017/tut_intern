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
        # print(f"{node.surface}\t{features[0]}\t{features[1]}")
        if features[0] in ["動詞", "名詞", "形容詞"] and node.surface != "":
            if features[0] in ["動詞", "形容詞"] and features[1] in ["非自立", "形式名詞"]:
                node = node.next
                continue

            if features[0] == "名詞":
                base = node.surface
            else:
                base = features[7] if len(features) >= 8 and features[7] != "*" else node.surface

            #print(f"{node.surface}\t{features[0]}\t{features[1]}")
            tokens.append(base)
            freq_tmp[features[0]] += 1
        node = node.next

    return tokens


def text2BoW(text, token_idx_dict):
    BoW = np.zeros(len(token_idx_dict))

    tokens = text2word(text)
    for token in tokens:
        if token in token_idx_dict:
            BoW[token_idx_dict[token]] = 1

    return BoW

# text = get_text()

target_columns = [
    'Sentence',
]

df = pd.read_csv(
    'wrime-ver2.tsv',
    sep='\t',
    usecols=target_columns
)

freq_tmp = Counter()

df = df.iloc[:200]
tokens = []
for idx, row in df.iterrows():
    #tokens.append(text2word(row["Sentence"]))
    tokens += text2word(row["Sentence"])

print(freq_tmp)

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

token_idx_dict = {}
for i, (token, cnt) in enumerate(str_dict):
    token_idx_dict[token] = i

#print(str_dict)
#print(len(str_dict))
#print(token_idx_dict)

for idx, row in df.iterrows():
    BoW = text2BoW(row["Sentence"], token_idx_dict)
    print(idx, row["Sentence"])
    print(BoW)
    for idx2, flag in enumerate(BoW):
        if flag == 1:
           print(str_dict[idx2][0]) 

    if idx >= 3:
        break
