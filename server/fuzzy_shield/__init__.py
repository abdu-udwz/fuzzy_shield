
import sys
import logging
collection_prefix = "fuzzy_collection_"

ALGORITHMS = {
    "hamming": "Hamming distance",
    "naive": "Naive Algo",
    "levenshtein_ratio": "Levenshtein ratio",
    "levenshtein_sort": "Levenshtein sort"
}


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
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
