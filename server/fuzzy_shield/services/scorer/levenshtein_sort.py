from thefuzz import fuzz, process
from .decorator import scorer_profiler


@scorer_profiler
def score(query: str, choices: list[str]):
    return process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
