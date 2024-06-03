"""
"""
import pandas as pd
from pathlib import Path

Path('./datasets/out').mkdir(parents=True, exist_ok=True)


def prepare_sqli():
    initial_set = pd.read_csv("./datasets/sqli.csv")
    initial_set.drop_duplicates(subset="Query", inplace=True)
    print("Raw set without duplicates", initial_set.shape)

    sample_set = initial_set.sample(n=200, replace=False)

    print("Sample", sample_set.shape)
    # print("Sample\n", sample_set.describe())
    sample_set.to_csv('./datasets/out/sqli-sample.csv', index=False)

    mixed_set = initial_set.drop(sample_set.index)
    # keep a copy without the samples with both malicious & non-malicious
    sample_set.to_csv('./datasets/out/sqli-mixed.csv', index=False)

    malicious_set = mixed_set[mixed_set["Label"] == 1]
    print("Malicious", malicious_set.shape)
    malicious_set.to_csv('./datasets/out/sqli-malicious.csv', index=False)


def main(*args, **argv):
    prepare_sqli()


if __name__ == '__main__':
    main()
