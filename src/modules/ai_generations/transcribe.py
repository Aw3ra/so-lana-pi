import openai
import os

def transcribe(OUTPUT_FILENAME):
    audio_file= open(OUTPUT_FILENAME, "rb")
    openai.api_key = os.environ["OPEN_AI_KEY"]
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript