import os
import json
import wave
import tempfile
from vosk import Model, KaldiRecognizer
import soundfile as sf

MODEL_PATH = "/home/wild/Desktop/epitech/T-AIA-901/T-AIA-901_par_1/API/app/models/vosk-model-fr-0.22"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model path '{MODEL_PATH}' does not exist")

model = Model(MODEL_PATH)

def process_audio_file(audio_bytes):
    """
    Process the audio bytes and return the transcribed text.
    Args:
        audio_bytes (bytes): The audio file content in bytes.
    Returns:
        str: The transcribed text.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file.flush()

        with wave.open(temp_audio_file.name, "rb") as wf:
            if wf.getnchannels() != 1:
                raise ValueError("Only mono audio files are supported. Please provide a mono WAV file.")

            recognizer = KaldiRecognizer(model, wf.getframerate())

            recognized_text = ""

            while True:
                data = wf.readframes(4096)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = json.loads(result).get("text", "")
                    if text:
                        recognized_text += text + " "

            final_result = recognizer.FinalResult()
            final_text = json.loads(final_result).get("text", "")
            if final_text:
                recognized_text += final_text

            return recognized_text.strip()