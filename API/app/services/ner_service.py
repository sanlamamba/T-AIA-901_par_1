import time

def extract_entities(text):
    """
    Extract named entities from the given text.
    Placeholder implementation; replace with actual NER logic.
    """
    # convert text to a float between 0 and 2 
    text_to_float = float(len(text) % 3) / 1.5
    time.sleep(text_to_float)
    
    return [
        {'status': "start", 'station': "La Douzillère"},
        {'status': "end", 'station': "Chalonnes"}
    ]
