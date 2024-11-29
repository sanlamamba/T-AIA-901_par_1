"""
Utility functions for file handling.
"""

import pandas as pd
from typing import List


def load_station_data(csv_path: str) -> List[str]:
    """
    Load station names from a CSV file.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        List[str]: List of station names.
    """
    data = pd.read_csv(csv_path, delimiter=";")
    return data["LIBELLE"].dropna().unique().tolist()


def save_training_data(training_data: List[tuple], output_path: str) -> None:
    """
    Save training data to a text file.

    Args:
        training_data (List[tuple]): List of generated sentences and annotations.
        output_path (str): Path to the output file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for text, annotations in training_data:
            f.write(f"{text}\n")
            f.write(f"{annotations}\n")
            
            
def load_templates(file_path: str) -> list:
    """
    Load sentence templates from a text file.

    Args:
        file_path (str): Path to the template file.

    Returns:
        list: List of templates as strings.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        templates = [line.strip() for line in f if line.strip()]
    return templates