"""
Utility function for google cloud
"""
from Levenshtein.StringMatcher import distance
from extensions import names


def get_closest_string(string: str):
    string = string.lower()
    min_distance = 1000
    min_string = ""

    for name in names:
        dist = distance(name, string)
        if dist < min_distance:
            min_string = name
            min_distance = dist

    return min_string[0].upper() + min_string[1:]
