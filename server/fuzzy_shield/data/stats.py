from typing_extensions import Optional
from pathlib import Path

import pandas as pd

from fuzzy_shield import Algorithms
from fuzzy_shield.task import CollectionStatsConfig, Task

Path('./datasets/stats').mkdir(parents=True, exist_ok=True)


def compute_stats(tasks: list[Task], config: CollectionStatsConfig):
    df = pd.DataFrame(tasks)

    # drop the algorithms enable properties
    cols_to_drop = list(Algorithms.algorithms) + \
        ['task_id', 'status', 'xss', 'sqli', 'collection', 'created_at']

    if not config.sqli:
        cols_to_drop.extend(Algorithms.sqli_properties())

    if not config.xss:
        cols_to_drop.extend(Algorithms.xss_properties())

    for algo in config.get_disabled_algorithms():
        cols_to_drop.extend(Algorithms.properties(algo))

    cols_to_drop = list(set(cols_to_drop))
    df.drop(columns=cols_to_drop, inplace=True)

    info_sheets = []

    def compute_algorithm_stats(prefix: str, name_prefix: str):
        threshold = getattr(config, prefix)

        score_col = f'{prefix}_score'
        time_col = f'{prefix}_time'
        cpu_col = f'{prefix}_cpu'
        memory_col = f'{prefix}_memory'
        match_col = f'{prefix}_match'

        result_col = f'{prefix}_result'
        df[result_col] = (df[score_col] > threshold).astype(int)

        fp_col = f'{prefix}_false_positive'
        fn_col = f'{prefix}_false_negative'
        df[fp_col] = ((df[result_col] == 1) & (
            df['designated_result'] == 0)).astype(int)

        df[fn_col] = ((df[result_col] == 0) & (
            df['designated_result'] == 1)).astype(int)

        algo_subset = df[['text', score_col, time_col, cpu_col,
                          memory_col, 'designated_result', result_col, fp_col, fn_col, match_col]]
        info_sheets.append((f'{name_prefix} results', algo_subset))

        algo_subset = algo_subset.copy()

        success_set = algo_subset[(
            algo_subset[result_col] == algo_subset['designated_result'])].copy()
        success_set.drop(columns=[fp_col, fn_col], inplace=True)
        ss_set = success_set[(success_set[result_col] == 0)]
        sm_set = success_set[(success_set[result_col] == 1)]
        info_sheets.append((f'{name_prefix} S results', success_set))
        info_sheets.append((f'{name_prefix} SS results', ss_set))
        info_sheets.append((f'{name_prefix} SM results', sm_set))

        failure_set = algo_subset[(
            algo_subset[result_col] != algo_subset['designated_result'])].copy()
        fp_set = algo_subset[(algo_subset[fp_col] == 1)].copy()
        fn_set = algo_subset[(algo_subset[fn_col] == 1)].copy()

        info_sheets.append((f'{name_prefix} F results', failure_set))
        info_sheets.append((f'{name_prefix} FP results', fp_set))
        info_sheets.append((f'{name_prefix} FN results', fn_set))

        stats = algo_subset.describe().copy()
        stats.drop(columns=['designated_result',
                   result_col, fp_col, fn_col], inplace=True)

        fp_count = df[(df[fp_col] == 1)].count()
        fn_count = df[(df[fn_col] == 1)].count()

        stats.loc['Threshold'] = threshold
        stats.loc['Successful count'] = len(success_set)
        stats.loc['Successful percentage'] = len(success_set) / len(df) * 100

        stats.loc['Failed count'] = len(failure_set)
        stats.loc['Failed percentage'] = len(failure_set) / len(df) * 100

        stats.loc['False positive count'] = fp_count
        stats.loc['False positive percentage'] = fp_count / \
            len(failure_set) * 100
        stats.loc['False positive overall percentage'] = fp_count / \
            len(df) * 100

        stats.loc['False negative count'] = fn_count
        stats.loc['False negative percentage'] = fn_count / \
            len(failure_set) * 100
        stats.loc['False negative overall percentage'] = fn_count / \
            len(df) * 100

        info_sheets.append((f'{name_prefix} STATS', stats))

        success_set = success_set.copy()
        success_set.drop(
            columns=['designated_result', result_col], inplace=True)
        ss_set.drop(
            columns=['designated_result', result_col], inplace=True)
        sm_set.drop(
            columns=['designated_result', result_col], inplace=True)

        failure_set = failure_set.copy()
        failure_set.drop(columns=['designated_result',
                         result_col, fp_col, fn_col], inplace=True)
        fp_set.drop(columns=['designated_result',
                             result_col, fp_col, fn_col], inplace=True)
        fn_set.drop(columns=['designated_result',
                             result_col, fp_col, fn_col], inplace=True)

        info_sheets.append(
            (f'{name_prefix} S STATS', success_set.describe()))
        info_sheets.append(
            (f'{name_prefix} SS STATS', ss_set.describe()))
        info_sheets.append(
            (f'{name_prefix} SM STATS', sm_set.describe()))

        info_sheets.append((f'{name_prefix} F STATS', failure_set.describe()))
        info_sheets.append((f'{name_prefix} FP STATS', fp_set.describe()))
        info_sheets.append((f'{name_prefix} FN STATS', fn_set.describe()))

    for algo in config.get_enabled_algorithms():
        if config.sqli:
            compute_algorithm_stats(
                f'{algo}_sqli', f'{Algorithms.get_shortcut(algo)} SQLi')
        if config.xss:
            compute_algorithm_stats(
                f'{algo}_xss', f'{Algorithms.get_shortcut(algo)} XSS')

    with pd.ExcelWriter(f'./datasets/stats/{config.collection}.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Results', index=False)
        for (sheetname, sheet) in info_sheets:
            sheet.to_excel(writer, sheet_name=sheetname)
