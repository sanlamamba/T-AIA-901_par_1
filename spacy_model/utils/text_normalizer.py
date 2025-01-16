"""
Text normalization utilities.
"""

from unidecode import unidecode


def normalize(text: str) -> str:
    """
    Normalize text to lowercase and remove accents.

    Args:
        text (str): The input text.

    Returns:
        str: Normalized text.
    """
    return unidecode(text.strip().lower())
