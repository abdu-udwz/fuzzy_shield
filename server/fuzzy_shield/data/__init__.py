"""
"""
import pandas as pd
import json
from pathlib import Path
from fuzzy_shield.task import Task
from fuzzy_shield.services import schedule_task

Path('./datasets/out').mkdir(parents=True, exist_ok=True)


def is_sqli_dataset_prepared():
    filenames = ["sqli-sample", "sqli-mixed", "sqli-malicious"]
    return all([Path(f'./datasets/out/{filename}.csv').exists() for filename in filenames])


def is_xss_dataset_prepared():
    filenames = ["xss-sample", "xss-mixed", "xss-malicious"]
    return all([Path(f'./datasets/out/{filename}.csv').exists() for filename in filenames])


def prepare_sqli(sample_size: int):
    raw_set_file = Path('./datasets/sqli.csv')
    if not raw_set_file.exists():
        raise Exception(
            f'SQLi datasets is not available, ensure dataset file exists at {raw_set_file.absolute()}')
    initial_set = pd.read_csv(raw_set_file)
    initial_set.drop_duplicates(subset="Query", inplace=True)
    print("Raw set without duplicates", initial_set.shape)

    sample_set = initial_set.sample(n=sample_size, replace=False)

    print("Sample", sample_set.shape)
    # print("Sample\n", sample_set.describe())
    sample_set.to_csv('./datasets/out/sqli-sample.csv', index=False)

    mixed_set = initial_set.drop(sample_set.index)
    # keep a copy without the samples with both malicious & non-malicious
    sample_set.to_csv('./datasets/out/sqli-mixed.csv', index=False)

    malicious_set = mixed_set[mixed_set["Label"] == 1]
    print("Malicious", malicious_set.shape)
    malicious_set.to_csv('./datasets/out/sqli-malicious.csv', index=False)


def prepare_xss(sample_size: int):
    raw_set_file = Path('./datasets/xss.csv')
    if not raw_set_file.exists():
        raise Exception(
            f'XSS datasets is not available, ensure dataset file exists at {raw_set_file.absolute()}')

    initial_set = pd.read_csv("./datasets/xss.csv")
    initial_set.drop_duplicates(subset="Sentence", inplace=True)
    print("Raw set without duplicates", initial_set.shape)

    sample_set = initial_set.sample(n=sample_size, replace=False)

    print("Sample", sample_set.shape)
    # print("Sample\n", sample_set.describe())
    sample_set.to_csv('./datasets/out/xss-sample.csv', index=False)

    mixed_set = initial_set.drop(sample_set.index)
    # keep a copy without the samples with both malicious & non-malicious
    sample_set.to_csv('./datasets/out/xss-mixed.csv', index=False)

    malicious_set = mixed_set[mixed_set["Label"] == 1]
    print("Malicious", malicious_set.shape)
    malicious_set.to_csv('./datasets/out/xss-malicious.csv', index=False)


def initialize(sample_size=200):
    """
    Check if there datasets exist, if not it generates new datasets
    If datasets exist but the sample size is not the same as the one passed as arg: `sample_size`, datasets are regenerated
    """
    generate_sqli = not is_sqli_dataset_prepared()
    generate_xss = not is_xss_dataset_prepared()

    info = _read_current_output_info()
    if info is not None and info.get('sample_size') != sample_size:
        generate_sqli = True
        generate_xss = True
    elif info is not None and info.get('sample_size') == sample_size and not generate_sqli and not generate_sqli:
        return

    if generate_sqli:
        prepare_sqli(sample_size)

    if generate_xss:
        prepare_xss(sample_size)

    _write_current_output_info(sample_size)


info_file = Path('./datasets/out/info.json')


def _read_current_output_info() -> dict | None:
    info = None
    if info_file.exists():
        with open(info_file, 'r') as file:
            info = json.load(file)

    return info


def _write_current_output_info(sample_size: int):
    with open(info_file, 'w', encoding='utf-8') as file:
        json.dump(
            {
                "sample_size": sample_size
            },
            file,
            indent=2
        )


def bulk_schedule_sample():
    sqli_sample = pd.read_csv('./datasets/out/sqli-sample.csv')

    sqli_tasks = []

    def create_task(row):
        sqli_tasks.append(
            Task(text=row['Query'], collection='bulk_1', designated_result=row['Label'], xss=0, hamming=0, naive=0))

    sqli_sample.apply(create_task, axis=1)

    for task in sqli_tasks:
        schedule_task(task)
    pass
