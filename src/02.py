import csv

with open("wrime-ver2.tsv", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")

    for row in reader:
        print(row)
