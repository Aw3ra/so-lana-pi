import wave
import audioop
import pvporcupine
import alsaaudio
import numpy as np
from ctypes import *
from contextlib import contextmanager
import pyaudio
from elevenlabs import generate, set_api_key, play, stream
import os
import time
import openai



# Configuration for Eleven Labs
os.environ['PATH'] += r";C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
OPENAI_KEY = os.environ["OPEN_AI_KEY"]
access_key = os.environ["PICOVOICE_KEY"]


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
    def __init__(self, silence_threshold=2550, silence_duration=5, min_audio_duration=3):
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.min_audio_duration = min_audio_duration
        self.OUTPUT_FILENAME = "test.wav"

    def record(self):
            # PV Porcupine initialization
            handle = pvporcupine.create(access_key=access_key, keyword_paths=['wakewords.ppn'])
            inp = alsaaudio.PCM(
                alsaaudio.PCM_CAPTURE,
                channels=2,
                rate=handle.sample_rate,
                format=alsaaudio.PCM_FORMAT_S32_LE,
                periodsize=handle.frame_length,
                device='plughw:1,0'
            )

            audio_buffer = []
            frames = []  # to save audio data
            silence_frames = 0
            recording_started = False

            def get_next_audio_frame():
                nonlocal audio_buffer
                l, pcm_data = inp.read()
                if l <= 0:
                    return None

                pcm_32 = np.frombuffer(pcm_data, dtype=np.int32)
                pcm_16 = (pcm_32 >> 16).astype(np.int16)
                pcm_mono = [(pcm_16[i] + pcm_16[i + 1]) // 2 for i in range(0, len(pcm_16), 2)]

                amplification_factor = 3
                amplified_mono = [int(i * amplification_factor) for i in pcm_mono]
                audio_buffer += amplified_mono

                if len(audio_buffer) >= handle.frame_length:
                    frame = audio_buffer[:handle.frame_length]
                    audio_buffer = audio_buffer[handle.frame_length:]
                    return frame
                return None

            print("Listening for wake word...")
            while True:
                frame = get_next_audio_frame()
                if frame:
                    keyword_index = handle.process(frame)
                    if keyword_index >= 0:
                        print("Wake word detected! Starting recording...")
                        recording_started = True

                    if recording_started:
                        rms = np.sqrt(np.mean(np.square(frame)))
                        print(f"RMS value: {rms}")  # Debug print
                        if rms > self.silence_threshold:
                            frames.append(np.array(frame, dtype=np.int16).tobytes())
                            silence_frames = 0
                        else:
                            silence_frames += 1
                            print(f"Silent frames: {silence_frames}")  # Debug print


                        if silence_frames * handle.frame_length / handle.sample_rate > self.silence_duration:
                            print("Recording finished.")
                            break

            if len(frames) * handle.frame_length / handle.sample_rate > self.min_audio_duration:
                filename = self.OUTPUT_FILENAME
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(handle.sample_rate)
                    wf.writeframes(b''.join(frames))
                return filename
            else:
                print("Recording was too short, discarding...")
                return None
    
    def transcribe(self, audio_filename):   # added audio_filename as an argument
        audio_file= open(audio_filename, "rb")
        openai.api_key = OPENAI_KEY
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text


class AudioPlayer:
    def __init__(self, voice="Lana - calm"):
        self.voice = voice
        self.printing = True

    def generate_and_play(self, text):
        audio_time_start = time.time()
        set_api_key = "cbbc88987232bc4e6af5db6015931420"
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
    print("started")
    recorder = AudioRecorder()
    recorder.record()

    print(recorder.transcribe("test.wav"))

