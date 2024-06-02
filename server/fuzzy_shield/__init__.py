
import sys
import logging
collection_prefix = "fuzzy_collection_"


class RedisSets:
    main = "fuzzy_tasks"
    main_incomplete = 'fuzzy_tasks_completed'
    main_completed = 'fuzzy_tasks_incomplete'

    collection_prefix = 'fuzzy_collection_'

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
