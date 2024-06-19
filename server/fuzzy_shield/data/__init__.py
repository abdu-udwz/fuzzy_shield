"""
"""
import math
import json
import pandas as pd
from pathlib import Path
from fuzzy_shield.task import Task, BulkTaskRequest
from fuzzy_shield.services import schedule_task

Path('./datasets/out').mkdir(parents=True, exist_ok=True)


def is_sqli_dataset_prepared():
    filenames = ["sqli-sample", "sqli-mixed", "sqli-malicious"]
    return all([Path(f'./datasets/out/{filename}.csv').exists() for filename in filenames])


def is_xss_dataset_prepared():
    filenames = ["xss-sample", "xss-mixed", "xss-malicious"]
    return all([Path(f'./datasets/out/{filename}.csv').exists() for filename in filenames])


def prepare_sqli(sample_size: float):
    raw_set_file = Path('./datasets/sqli.csv')
    if not raw_set_file.exists():
        raise Exception(
            f'SQLi datasets is not available, ensure dataset file exists at {raw_set_file.absolute()}')

    dataset = pd.read_csv(raw_set_file)
    raw_stats = dataset.describe()
    raw_stats.loc["Malicious Count"] = dataset[dataset["Label"] == 1].count()
    raw_stats.loc["Safe Count"] = dataset[dataset["Label"] == 0].count()

    sample_count = math.ceil(sample_size * len(dataset) / 100)

    dataset.drop_duplicates(subset="Query", inplace=True)
    raw_without_duplicates_stats = dataset.describe()
    raw_without_duplicates_stats.loc["Malicious Count"] = dataset[dataset["Label"] == 1].count(
    )
    raw_without_duplicates_stats.loc["Safe Count"] = dataset[dataset["Label"] == 0].count(
    )

    sample_set = dataset.sample(n=sample_count, replace=False)
    sample_stats = sample_set.describe().copy()

    sample_stats.loc["Malicious Count"] = sample_set[sample_set["Label"] == 1].count()
    sample_stats.loc["Safe Count"] = sample_set[sample_set["Label"] == 0].count()

    sample_set.to_csv('./datasets/out/sqli-sample.csv', index=False)

    mixed_set = dataset.drop(sample_set.index)
    # keep a copy without the samples with both malicious & non-malicious
    sample_set.to_csv('./datasets/out/sqli-mixed.csv', index=False)

    malicious_set = mixed_set[mixed_set["Label"] == 1]
    dataset_stats = malicious_set.describe()
    malicious_set.to_csv('./datasets/out/sqli-malicious.csv', index=False)

    with pd.ExcelWriter('./datasets/out/sqli-info.xlsx') as writer:
        raw_stats.to_excel(writer, sheet_name='Raw')
        raw_without_duplicates_stats.to_excel(
            writer, sheet_name='Raw no duplicates')
        sample_stats.to_excel(writer, sheet_name='Sample')
        dataset_stats.to_excel(writer, sheet_name='Dataset')

    return len(sample_set)


def prepare_xss(sample_size: float):
    raw_set_file = Path('./datasets/xss.csv')
    if not raw_set_file.exists():
        raise Exception(
            f'XSS datasets is not available, ensure dataset file exists at {raw_set_file.absolute()}')

    dataset = pd.read_csv(raw_set_file)
    raw_stats = dataset.describe()
    raw_stats.loc["Malicious Count"] = dataset[dataset["Label"] == 1].count()
    raw_stats.loc["Safe Count"] = dataset[dataset["Label"] == 0].count()

    sample_count = math.ceil(sample_size * len(dataset) / 100)

    dataset.drop_duplicates(subset="Sentence", inplace=True)
    raw_without_duplicates_stats = dataset.describe()
    raw_without_duplicates_stats.loc["Malicious Count"] = dataset[dataset["Label"] == 1].count(
    )
    raw_without_duplicates_stats.loc["Safe Count"] = dataset[dataset["Label"] == 0].count(
    )

    sample_set = dataset.sample(n=sample_count, replace=False)
    sample_stats = sample_set.describe().copy()

    sample_stats.loc["Malicious Count"] = sample_set[sample_set["Label"] == 1].count()
    sample_stats.loc["Safe Count"] = sample_set[sample_set["Label"] == 0].count()

    sample_set.to_csv('./datasets/out/xss-sample.csv', index=False)

    mixed_set = dataset.drop(sample_set.index)
    # keep a copy without the samples with both malicious & non-malicious
    sample_set.to_csv('./datasets/out/xss-mixed.csv', index=False)

    malicious_set = mixed_set[mixed_set["Label"] == 1]
    dataset_stats = malicious_set.describe()
    malicious_set.to_csv('./datasets/out/xss-malicious.csv', index=False)

    with pd.ExcelWriter('./datasets/out/xss-info.xlsx') as writer:
        raw_stats.to_excel(writer, sheet_name='Raw')
        raw_without_duplicates_stats.to_excel(
            writer, sheet_name='Raw no duplicates')
        sample_stats.to_excel(writer, sheet_name='Sample')
        dataset_stats.to_excel(writer, sheet_name='Dataset')

    return len(sample_set)


def initialize(sample_size: float = 30):
    """
    Check if there datasets exist, if not it generates new datasets
    If datasets exist but the sample size is not the same as the one passed as arg: `sample_size`, datasets are regenerated
    :arg: sample_size as a percentage of the available
    """
    generate_sqli = not is_sqli_dataset_prepared()
    generate_xss = not is_xss_dataset_prepared()

    info = _read_current_output_info()
    if info is not None and info.get('sample_size') != sample_size:
        generate_sqli = True
        generate_xss = True
    elif info is not None and info.get('sample_size') == sample_size and not generate_sqli and not generate_sqli:
        return

    info = info or {}

    sqli_sample = info.get('sqli_sample', 0)
    if generate_sqli:
        sqli_sample = prepare_sqli(sample_size)

    xss_sample = info.get('xss_sample', 0)
    if generate_xss:
        xss_sample = prepare_xss(sample_size)

    _write_current_output_info(sample_size, sqli_sample, xss_sample)


info_file = Path('./datasets/out/info.json')


def _read_current_output_info() -> dict | None:
    info = None
    if info_file.exists():
        with open(info_file, 'r') as file:
            info = json.load(file)

    return info


def _write_current_output_info(sample_size: float, sqli_sample: int, xss_sample: int):
    with open(info_file, 'w', encoding='utf-8') as file:
        json.dump(
            {
                "sample_size": sample_size,
                "sqli_sample": sqli_sample,
                "xss_sample": xss_sample
            },
            file,
            indent=2
        )


def bulk_schedule_sample(config: BulkTaskRequest):

    tasks: list[Task] = []

    text_col = 'Query' if config.mode == 'sqli' else 'Sentence'

    def create_task(row):
        tasks.append(
            Task(text=row[text_col],
                 collection=config.collection,
                 designated_result=row['Label'], xss=config.mode == 'xss',
                 sqli=config.mode == 'sqli',
                 hamming=config.hamming,
                 naive=config.naive,
                 levenshtein_ratio=config.levenshtein_ratio,
                 levenshtein_sort=config.levenshtein_sort))

    if config.mode == 'sqli':
        sqli_sample = pd.read_csv('./datasets/out/sqli-sample.csv')
        sqli_sample.apply(create_task, axis=1)
    else:
        xss_sample = pd.read_csv('./datasets/out/xss-sample.csv')
        xss_sample.apply(create_task, axis=1)

    for task in tasks:
        schedule_task(task)
