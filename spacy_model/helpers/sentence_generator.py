import random
from helpers.annotation_builder import build_annotations
from utils.file_handler import load_templates


def generate_sentence(stations: list, templates: list) -> tuple:
    """
    Generate a random sentence and corresponding annotations.

    Args:
        stations (list): List of station names.
        templates (list): List of sentence templates.

    Returns:
        tuple: Generated sentence and its annotations.
    """
    station1, station2 = random.sample(stations, 2)
    template = random.choice(templates)
    sentence = template.format(station1=station1, station2=station2)
    annotations = build_annotations(sentence, station1, station2)
    return sentence, annotations


def generate_training_data(stations: list, templates_path: str, n: int = 1000) -> list:
    """
    Generate a list of training sentences and annotations.

    Args:
        stations (list): List of station names.
        templates_path (str): Path to the sentence templates file.
        n (int): Number of sentences to generate.

    Returns:
        list: List of generated sentences and annotations.
    """
    templates = load_templates(templates_path)
    return [generate_sentence(stations, templates) for _ in range(n)]
