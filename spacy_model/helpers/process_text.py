import spacy


def process_text(text: str, model_dir: str):
    """
    Load the trained model and process input text to extract stations with their statuses.

    Args:
        text (str): The input text to process.
        model_dir (str): Path to the trained model directory.

    Returns:
        list: A list of dictionaries representing stations and their statuses.
    """
    try:
        nlp = spacy.load(model_dir)
        doc = nlp(text)

        entities = [{"station": ent.text.lower(), "start_char": ent.start_char} for ent in doc.ents]
        entities = sorted(entities, key=lambda x: x["start_char"])

        output = []
        for i, entity in enumerate(entities):
            status = "start" if i == 0 else "end" if i == len(entities) - 1 else "intermediate"
            output.append({"status": status, "station": entity["station"]})

        return output

    except Exception as e:
        print(f"Error processing text: {e}")
        return []
