import pandas as pd

df = pd.read_csv("wrime-ver2.tsv", sep="\t")

data = df[["Sentence", "Writer_Anger"]]

# print(sentences[0:100])

angry_cnt = 0
for i in range(100):
    if int(data["Writer_Anger"][i]) != 0:
        angry_cnt += 1
    print(i, data["Sentence"][i], data["Writer_Anger"][i])

print(f"angry_cnt:{angry_cnt}")
data.to_csv("sentences.tsv", sep="\t", index=False)
