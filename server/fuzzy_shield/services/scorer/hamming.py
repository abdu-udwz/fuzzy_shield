from thefuzz import process
from thefuzz.utils import full_process
from .decorator import scorer_profiler


@scorer_profiler
def score(query: str, choices: list[str]):
    return process.extractOne(query, choices, scorer=hamming_scorer)


def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        return None  # Indicate that lengths are not equal
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


def hamming_scorer(s1, s2):
    # Check if strings are of equal length
    if len(s1) != len(s2):
        return 0  # Return a score of zero if lengths are not equal

    # Calculate Hamming distance
    s1 = full_process(s1)
    s2 = full_process(s2)
    distance = hamming_distance(s1, s2)

    # Convert distance to a similarity score (0-100)
    max_distance = len(s1)  # maximum possible Hamming distance
    score = ((max_distance - distance) / max_distance) * 100
    return score
