import wave
import audioop
from ctypes import *
from contextlib import contextmanager
import pyaudio
from elevenlabs import generate, set_api_key, play, stream
import os
import time
import openai



# Configuration for Eleven Labs
os.environ['PATH'] += r";C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
set_api_key(os.environ["ELEVEN_LABS_KEY"])

# Error handler for ALSA
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


class AudioRecorder:
    def __init__(self, silence_threshold=900, silence_duration=1, min_audio_duration=1):
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.min_audio_duration = min_audio_duration
        self.OUTPUT_FILENAME = "./src/audio_content/audio.wav"

    def record(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 4096
        
        with noalsaerr():
            audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK,
                            input_device_index=1)

        frames = []
        silence_frames = 0
        recording_started = False

        while True:
            data = stream.read(CHUNK)
            rms = audioop.rms(data, 2)

            if rms > self.silence_threshold:
                if not recording_started:
                    print("Recording started...")
                    recording_started = True
                frames.append(data)
                silence_frames = 0
            elif recording_started:
                frames.append(data)
                silence_frames += 1
                if silence_frames * CHUNK / RATE > self.silence_duration:
                    break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        if len(frames) * CHUNK / RATE > self.min_audio_duration:
            filename = self.OUTPUT_FILENAME
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            return filename
        else:
            print("Recording was too short, discarding...")
            return None

    def transcribe(OUTPUT_FILENAME):
        audio_file= open(OUTPUT_FILENAME, "rb")
        openai.api_key = os.environ["OPEN_AI_KEY"]
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript


class AudioPlayer:
    def __init__(self, voice="Lana - calm"):
        self.voice = voice
        self.printing = True

    def generate_and_play(self, text):
        audio_time_start = time.time()
        audio = generate(text="--" + text, voice=self.voice)
        audio_time_end = time.time()
        print("Audio time: " + str(audio_time_end - audio_time_start))
        play(audio)

    def generate_and_stream(self, text):
        if self.printing:
            print(text)
        else:
            audio = generate(text="--" + text, voice=self.voice, stream=True)
            stream(audio)


# Usage example:
if __name__ == "__main__":
    recorder = AudioRecorder()
    recorded_file = recorder.record()

    if recorded_file:
        player = AudioPlayer()
        player.generate_and_play("Recording saved!")
