
import sys
import logging
from typing_extensions import Literal

collection_prefix = "fuzzy_collection_"

TScorerAlgorithm = Literal["hamming",    "naive",
                           "levenshtein_ratio",    "levenshtein_sort"]
TScorerAlgorithmProperty = Literal["score", 'time', 'memory', 'cpu', 'match']


class Algorithms:

    algorithms: list[TScorerAlgorithm] = ["hamming",    "naive",
                                          "levenshtein_ratio",    "levenshtein_sort"]
    algorithm_properties: TScorerAlgorithmProperty = [
        "score", 'time', 'memory', 'cpu', 'match']

    @staticmethod
    def properties(algo: TScorerAlgorithm | None = None) -> list[TScorerAlgorithmProperty]:
        return Algorithms.sqli_properties(algo) + Algorithms.xss_properties(algo)

    @staticmethod
    def sqli_properties(algo: TScorerAlgorithm | None = None) -> list[TScorerAlgorithmProperty]:
        return Algorithms.__properties(algo, 'sqli')

    @staticmethod
    def xss_properties(algo: TScorerAlgorithm | None = None) -> list[TScorerAlgorithmProperty]:
        return Algorithms.__properties(algo, 'xss')

    @staticmethod
    def __properties(algo: TScorerAlgorithm | None = None, attack: str = 'sqli') -> list[TScorerAlgorithmProperty]:
        props = []
        algos_to_use = []

        if algo is None:
            algos_to_use = Algorithms.algorithms
        else:
            algos_to_use = [algo]

        for _algo in algos_to_use:
            for prop in Algorithms.algorithm_properties:

                props.append(f'{_algo}_{attack}_{prop}')

        return props


class RedisSets:
    main = "fuzzy_tasks"
    main_incomplete = 'fuzzy_tasks_completed'
    main_completed = 'fuzzy_tasks_incomplete'

    collection_prefix = 'fuzzy_collection_'

    updates_channel = "task_updates"

    @staticmethod
    def collection(name: str): return f'{collection_prefix}{name}'

    @staticmethod
    def collection_incomplete(
        name: str): return f'{collection_prefix}{name}_incomplete'

    @staticmethod
    def collection_completed(name: str):
        return f'{collection_prefix}{name}_completed'


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
