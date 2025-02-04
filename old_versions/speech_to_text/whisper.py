import os
import whisper

audio_file_path = "./audio.wav"
output_text_file = "./transcription_output.txt"

if not os.path.exists(audio_file_path):
    print(f"Error: Audio file '{audio_file_path}' does not exist.")
    exit(1)

model = whisper.load_model("base")

try:
    result = model.transcribe(audio_file_path, language="fr")
    recognized_text = result["text"]
    print(recognized_text)

    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(recognized_text)


except Exception as e:
    print(f"Error during transcription: {e}")
