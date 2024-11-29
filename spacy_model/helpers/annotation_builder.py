def build_annotations(sentence: str, station1: str, station2: str) -> dict:
    """
    Build entity annotations for a given sentence.

    Args:
        sentence (str): The generated sentence.
        station1 (str): First station name.
        station2 (str): Second station name.

    Returns:
        dict: Entity annotations in spaCy format.
    """
    annotations = []
    start1 = sentence.find(station1)
    if start1 != -1:
        end1 = start1 + len(station1)
        annotations.append((start1, end1, "STATION"))

    start2 = sentence.find(station2)
    if start2 != -1:
        end2 = start2 + len(station2)
        annotations.append((start2, end2, "STATION"))

    return {"entities": annotations}
