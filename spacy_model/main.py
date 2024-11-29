import argparse
from utils.file_handler import load_station_data
from helpers.sentence_generator import generate_training_data
from utils.data_converter import convert_to_spacy_format
from train import train_ner
from config.constants import CSV_PATH, TEMPLATES_PATH, TRAIN_SPACY_PATH, VAL_SPACY_PATH, OUTPUT_MODEL_DIR, METRIC_OUTPUT, N_ITER
from helpers.process_text import process_text


def train_model():
    """
    Main function to generate training and validation data, train the model, 
    and save the trained model to disk.
    """
    print("Starting training...")
    stations = load_station_data(CSV_PATH)
    training_data = generate_training_data(stations, TEMPLATES_PATH, n=100)
    validation_data = generate_training_data(stations, TEMPLATES_PATH, n=100)

    convert_to_spacy_format(training_data, TRAIN_SPACY_PATH)
    convert_to_spacy_format(validation_data, VAL_SPACY_PATH)

    train_ner(TRAIN_SPACY_PATH, VAL_SPACY_PATH, OUTPUT_MODEL_DIR, METRIC_OUTPUT, n_iter=N_ITER)
    print("Training completed!")


def process_user_text(text: str):
    """
    Process user input text using the trained model and extract station entities.

    Args:
        text (str): Input text to process.
    """
    print(f"Processing text: {text}")
    result = process_text(text, OUTPUT_MODEL_DIR)
    print("Result:")
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model or process text using a trained spaCy model.")
    parser.add_argument(
        "-t", "--text",
        type=str,
        help="Text to process with the trained model. If not provided, the script trains the model.",
    )

    args = parser.parse_args()

    if args.text:
        process_user_text(args.text)
    else:
        train_model()