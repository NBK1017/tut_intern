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

minami_result = [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0];
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

print("minami:1, harada:0\n")
df2 = df[(df["minami"] == 1) & (df["harada"] == 0)]
for index, row in df2.iterrows():
    sentence = row['Sentence']
    print(f'{index}:{sentence}\n')

print("all_zero")
df2 = df[(df["minami"] == 0) & (df["harada"] == 0)]
for index, row in df2.iterrows():
    sentence = row['Sentence']
    print(f'{index}:{sentence}\n')
