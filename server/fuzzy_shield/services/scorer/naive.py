from .decorator import scorer_profiler
from thefuzz import fuzz, process
from thefuzz.utils import full_process


@scorer_profiler
def score(query: str, choices: list[str]):
    return process.extractOne(query, choices, scorer=naive_pattern_scorer)


def naive_pattern_match(text, pattern):
    """
    Naive pattern matching algorithm.

    :param text: The text in which to search for the pattern.
    :param pattern: The pattern to search for.
    :return: The number of positions where the pattern matches the text.
    """
    n = len(text)
    m = len(pattern)
    match_count = 0

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            match_count += 1

    return match_count


def naive_pattern_scorer(query, choice):
    """
    Custom scorer that uses the naive pattern matching algorithm.

    :param query: The query string.
    :param choice: The choice string to compare against the query.
    :return: The similarity score based on naive pattern matching.
    """
    query = full_process(query)
    choice = full_process(choice)

    if not query or not choice:
        return 0

    match_count = naive_pattern_match(choice, query)

    # Calculate the similarity score
    score = (match_count / len(choice)) * 100 if len(choice) > 0 else 0
    return int(score)
