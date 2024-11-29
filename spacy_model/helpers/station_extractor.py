"""
Station extraction logic.
"""

from utils.text_normalizer import normalize
from helpers.matcher import create_matcher, fuzzy_match_station
from typing import List, Dict


def extract_stations(text: str, stations: List[str]) -> List[Dict[str, str]]:
    """
    Extract stations and their roles (start, intermediate, end) from text.

    Args:
        text (str): The input text.
        stations (List[str]): List of station names.

    Returns:
        List[Dict[str, str]]: Extracted stations with roles.
    """
    normalized_text = normalize(text)

    import spacy
    nlp = spacy.load("fr_core_news_sm")
    matcher = create_matcher(nlp, stations)
    doc = nlp(normalized_text)

    matches = matcher(doc)
    direct_matches = [{"text": doc[start:end].text, "start": start, "end": end} for match_id, start, end in matches]
    fuzzy_matches = fuzzy_match_station(normalized_text, stations)

    all_matches = {normalize(match["text"]): match for match in direct_matches}
    for fuzzy_match in fuzzy_matches:
        if fuzzy_match not in all_matches:
            all_matches[fuzzy_match] = {"text": fuzzy_match}

    sorted_matches = sorted(all_matches.values(), key=lambda x: text.find(x["text"]))

    station_context = {"from": None, "to": None, "intermediaries": []}

    for match in sorted_matches:
        if not station_context["from"]:
            station_context["from"] = match["text"]
        elif not station_context["to"]:
            station_context["to"] = match["text"]
        else:
            station_context["intermediaries"].append(match["text"])

    result = [{"status": "start", "station": station_context["from"]}]
    result.extend({"status": "intermediate", "station": station} for station in station_context["intermediaries"])
    result.append({"status": "end", "station": station_context["to"]})

    return result
