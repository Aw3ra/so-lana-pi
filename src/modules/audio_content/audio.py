from elevenlabs import generate, set_api_key, play, stream
import os
import time
os.environ['PATH'] += r";C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
set_api_key(os.environ["ELEVEN_LABS_KEY"])

printing = True


def generate_and_play_audio(text):
  audio_time_start = time.time()
  audio = generate(
    text="--"+text,
    voice="Lana - calm",
  )
  audio_time_end = time.time()
  print("Audio time: " + str(audio_time_end - audio_time_start))
  play(audio)

def generate_and_stream_audio(text):
  if printing:
    print(text)
  else:
    audio = generate(
      text="--"+text,
      voice="Lana - calm",
      stream=True,
    )
    stream(audio)