""" 
     This module contains functions to convert training data to spaCy binary format.
     
"""
import spacy
from spacy.tokens import DocBin
from pathlib import Path
from typing import List, Tuple, Dict


def convert_to_spacy_format(training_data: List[Tuple[str, Dict]], output_path: str):
    """
    Convert training data to spaCy binary format.

    Args:
        training_data (List[Tuple[str, Dict]]): List of sentences and annotations.
        output_path (str): Path to save the converted data.
    """
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    nlp = spacy.blank("fr")
    doc_bin = DocBin()

    for text, annotations in training_data:
        doc = nlp.make_doc(text)
        ents = [
            doc.char_span(start, end, label=label)
            for start, end, label in annotations["entities"]
            if doc.char_span(start, end, label=label)
        ]
        doc.ents = ents
        doc_bin.add(doc)

    doc_bin.to_disk(output_path)