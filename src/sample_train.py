import numpy as np
import pandas as pd
import MeCab
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, classification_report
from collections import Counter

def text2word(text):
    mecab = MeCab.Tagger()

    words = []
   
    node = mecab.parseToNode(text)
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
            words.append(base)
        node = node.next

    return words 


def texts2vocab(sentences):
    mecab = MeCab.Tagger()

    #_vocab = []

    '''
    freq = Counter()
    for idx, text in enumerate(sentences):
        words = text2word(text)
        for word in words:
            freq[word] += 1
    '''

    freq = Counter()
    cnt = 1
    for idx, text in enumerate(sentences):
        node = mecab.parseToNode(text)
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
                #_vocab.append(base)
                freq[base] += 1

            node = node.next

        if (idx + 1) >= len(sentences) * 0.02 * cnt:
            cnt += 1
            print("#", end="", flush=True)
    print()

    vocab = {}
    for idx, (word, cnt) in enumerate(freq.most_common()):
        vocab[word] = idx

    return vocab


def texts2bows(vocab_idx_dict, sentences):
    print((len(sentences), len(vocab_idx_dict)))
    bows = np.zeros((len(sentences), len(vocab_idx_dict)))

    cnt = 1
    for idx, text in enumerate(sentences):
        words = text2word(text)
        for word in words:
            if word in vocab_idx_dict:
                bows[idx][vocab_idx_dict[word]] = 1

        if (idx + 1) >= len(sentences) * 0.02 * cnt:
            cnt += 1
            print("#", end="", flush=True)
    print()

    return bows 


target_columns = [
    'Sentence',
    'Writer_Joy'
]

df = pd.read_csv(
    'wrime-ver2.tsv',
    sep='\t',
    nrows=20000,
    usecols=target_columns
)

sentences = []
labels = []
for index, row in df.iterrows():
    sentences.append(row['Sentence'])
    labels.append(1 if row['Writer_Joy'] > 0 else 0)

train_sentences = sentences[:18000]
test_sentences = sentences[18000:]
train_labels = labels[:18000]
test_labels = labels[18000:]

# TODO
vocab = texts2vocab(train_sentences) # 分詞、sort、辞書を作る
train_sentence_bows = texts2bows(vocab, train_sentences) # 18000個のbowリストを得る
test_sentence_bows = texts2bows(vocab, test_sentences)

print(train_sentence_bows[:10])
print(test_sentence_bows[:10])

# TODO: train_sentence_bows, test_sentence_bows, train_labels, test_labelsを
# numpy arrayにする

# 1. 訓練
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(train_sentence_bows, train_labels)

# 2. 予測
test_preds = clf.predict(test_sentence_bows)

f1_macro = f1_score(test_labels, test_preds, average='macro')
print(f"F1-score (Macro): {f1_macro:.4f}")

print("\n詳細報告:")
print(classification_report(test_labels, test_preds, target_names=["Not Joy (0)", "Joy (1)"]))
