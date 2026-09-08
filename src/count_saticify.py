import pandas as pd

target_columns = [
    'idx',
    'is_saticify'
]

df = pd.read_csv(
    'anotation_1.csv',
    usecols=target_columns
)

#print("[", end="")
saticify_cnt = 0
for index, row in df.iterrows():
    #print(row["is_saticify"], end=",")
    if row["is_saticify"] > 0:
        saticify_cnt += 1

saticify_row = df[df["is_saticify"] > 0]
print(f"saticify_cnt:{saticify_cnt}")
print(saticify_row)
#print(str(df["is_saticify"]))
