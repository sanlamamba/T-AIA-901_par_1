import spacy
from spacy.util import minibatch
from pathlib import Path
import random
import pandas as pd


def train_ner(train_data_path: str, val_data_path: str, output_dir: str, metrics_output_path: str, n_iter: int = 10):
    """
    Train and evaluate a spaCy NER model, and save detailed training metrics to an Excel file.

    Args:
        train_data_path (str): Path to the training data (.spacy file).
        val_data_path (str): Path to the validation data (.spacy file).
        output_dir (str): Directory to save the trained model.
        metrics_output_path (str): Path to save the training metrics as an Excel file.
        n_iter (int): Number of training iterations.
    """
    nlp = spacy.blank("fr")
    ner = nlp.add_pipe("ner", last=True)

    train_data = list(spacy.tokens.DocBin().from_disk(train_data_path).get_docs(nlp.vocab))
    val_data = list(spacy.tokens.DocBin().from_disk(val_data_path).get_docs(nlp.vocab))

    optimizer = nlp.begin_training()

    metrics = [] 

    for epoch in range(n_iter):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=8)

        for batch in batches:
            examples = [
                spacy.training.Example.from_dict(
                    doc, {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]}
                )
                for doc in batch
            ]
            nlp.update(examples, drop=0.5, losses=losses)

        training_examples = [
            spacy.training.Example.from_dict(
                doc, {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]}
            )
            for doc in train_data
        ]
        train_scores = nlp.evaluate(training_examples)

        validation_examples = [
            spacy.training.Example.from_dict(
                doc, {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]}
            )
            for doc in val_data
        ]
        val_scores = nlp.evaluate(validation_examples)

        print(
            f"Epoch {epoch + 1}: "
            f"Training Loss = {losses['ner']:.3f}, "
            f"Training Precision = {train_scores['ents_p']:.3f}, "
            f"Validation Precision = {val_scores['ents_p']:.3f}, "
            f"Validation Loss = {losses['ner']:.3f}"
        )

        metrics.append({
            "Epoch": epoch + 1,
            "training_precision": train_scores["ents_p"],
            "training_loss": losses["ner"],
            "validation_precision": val_scores["ents_p"],
            "validation_loss": losses["ner"],
        })

    metrics_df = pd.DataFrame(metrics)
    Path(metrics_output_path).parent.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(metrics_output_path, index=False)
    print(f"Training metrics saved to {metrics_output_path}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_dir)
    print(f"Model saved to {output_dir}")
