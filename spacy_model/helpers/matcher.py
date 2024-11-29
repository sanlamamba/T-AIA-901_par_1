"""
Matcher utilities for station extraction.
"""

from spacy.matcher import PhraseMatcher
from fuzzywuzzy import fuzz, process
from spacy.language import Language
from typing import List


def create_matcher(nlp: Language, stations: List[str]) -> PhraseMatcher:
    """
    Create a PhraseMatcher for station names.

    Args:
        nlp (Language): spaCy language model.
        stations (List[str]): List of station names.

    Returns:
        PhraseMatcher: Configured PhraseMatcher instance.
    """
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    station_patterns = [nlp.make_doc(station) for station in stations]
    matcher.add("STATION", station_patterns)
    return matcher


def fuzzy_match_station(input_text: str, stations: List[str], threshold: int = 80) -> List[str]:
    """
    Find station names using fuzzy matching.

    Args:
        input_text (str): The input text.
        stations (List[str]): List of station names.
        threshold (int): Match confidence threshold.

    Returns:
        List[str]: List of fuzzy-matched station names.
    """
    matches = process.extractBests(input_text, stations, scorer=fuzz.ratio, score_cutoff=threshold)
    return [match[0] for match in matches]
