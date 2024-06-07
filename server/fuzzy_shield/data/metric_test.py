from thefuzz.fuzz import ratio, partial_ratio, token_set_ratio, token_sort_ratio, partial_token_sort_ratio, partial_token_set_ratio
from thefuzz import process
import pandas as pd
from pathlib import Path

Path('./datasets/results').mkdir(parents=True, exist_ok=True)

sqli = pd.read_csv("./datasets/out/sqli-malicious.csv")
sample_set = pd.read_csv("./datasets/out/sqli-sample.csv")["Query"]


sqli_set = sqli['Query']

algos = [
    ratio, token_set_ratio, token_sort_ratio
]
for algo in algos:
    print("Running Algo:", algo.__name__)

    df = pd.DataFrame({
        "sample": [],
        "score": [],
        "match": []
    })
    for sample in sample_set:
        result = process.extractOne(sample, sqli_set, scorer=algo)
        if len(result):
            df.loc[len(df)] = {
                "sample": sample,
                "score": result[1],
                "match": result[0]
            }

    print(df.describe())

    df.to_csv(f"./datasets/results/{algo.__name__}.csv")
