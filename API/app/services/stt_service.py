import os
import json
import wave
import tempfile
from vosk import Model, KaldiRecognizer
import soundfile as sf
from pydub import AudioSegment
from config import config

vosk_models = {
    'fr-small': 'vosk-model-small-fr-0.22',
    'fr': 'vosk-model-fr-0.22',
}
MODEL_NAME = vosk_models["fr-small"]
MODEL_PATH = config['basedir'] + "/app/models" + "/" + MODEL_NAME

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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        try:
            temp_audio_file.write(audio_bytes)
            temp_audio_file.flush()

            audio = AudioSegment.from_file(temp_audio_file.name)
            audio = audio.set_channels(1).set_frame_rate(16000)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as mono_audio_file:
                audio.export(mono_audio_file.name, format="wav")
                mono_audio_file.flush()

                with wave.open(mono_audio_file.name, "rb") as wf:
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

        finally:
            os.unlink(temp_audio_file.name)
            if 'mono_audio_file' in locals():
                os.unlink(mono_audio_file.name)
