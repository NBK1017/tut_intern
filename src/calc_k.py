import numpy as np
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
usecols=target_columns
)

df = df.iloc[:100]

'''
target_columns = [
    'idx',
    'is_saticify'
]

df1 = pd.read_csv(
    'anotation_1.csv',
    usecols=target_columns
)

df2 = pd.read_csv(
    'anotation_1.csv',
    usecols=target_columns
)

df = pd.DataFrame()
df["minami"] = df1["is_saticify"]
df["harada"] = df2["is_saticify"]
'''

minami_result = [0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,1,1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,1,0,1,0,0,1,1,0,1,0,0,0]
harada_result = [0,1,1,0,1,0,1,0,1,1,1,0,0,1,1,0,0,0,1,1,1,1,0,0,0,1,0,1,1,1,0,1,1,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,0,0,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,0]

df["minami"] = minami_result
df["harada"] = harada_result

mx = np.zeros((2, 2))
for h, m in zip(harada_result, minami_result):
    mx[0 if h == 1 else 1][0 if m == 1 else 1] += 1

print(mx)
print(" \tM1\tM0")
print(f"H1\t{mx[0][0]}\t{mx[0][1]}")
print(f"H0\t{mx[1][0]}\t{mx[1][1]}")

def calc_kappa(mx):
    s = np.sum(mx) 
    s_row = np.sum(mx, axis=1)
    s_column = np.sum(mx, axis=0)

    print(" \tM1\tM0\tsum")
    print(f"H1\t{mx[0][0]}\t{mx[0][1]}\t{s_row[0]}")
    print(f"H0\t{mx[1][0]}\t{mx[1][1]}\t{s_row[1]}")

    # print(s_row, s_column)
    po = (mx[0][0] + mx[1][1]) / s
    pe = s_row[0] / s * s_column[0] / s + s_row[1] / s * s_column[1] / s

    # print(po, pe)
    return (po - pe) / (1 - pe)

print(f"kappa: {calc_kappa(mx)}")
print(df[(df["minami"] == 1) & (df["harada"] == 0)]["Sentence"])

print("all_zero")

df2 = df[(df["minami"] == 0) & (df["harada"] == 0)]
for index, row in df2.iterrows():
    sentence = row['Sentence']
    print(f'{index}:{sentence}\n')
