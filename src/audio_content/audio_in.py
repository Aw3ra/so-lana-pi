import pyaudio
import wave
import audioop
import time

from ctypes import *
from contextlib import contextmanager
import pyaudio
import time

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


def record_audio(silence_threshold=900, silence_duration=1, min_audio_duration=1):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 4096
    OUTPUT_FILENAME = "./src/audio_content/audio.wav"  # Using a placeholder for timestamp
    with noalsaerr():
        audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=1)  # Use the USB microphone

    frames = []
    silence_frames = 0
    recording_started = False

    while True:
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)  # Get the root mean square to measure volume

        if rms > silence_threshold:
            if not recording_started:
                print("Recording started...")
                recording_started = True
            frames.append(data)
            silence_frames = 0
        elif recording_started:
            frames.append(data)
            silence_frames += 1
            if silence_frames * CHUNK / RATE > silence_duration:
                break

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    audio.terminate()

    if len(frames) * CHUNK / RATE > min_audio_duration:
        filename = OUTPUT_FILENAME
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        return filename
    else:
        print("Recording was too short, discarding...")
        return None

if __name__ == "__main__":
    record_audio()
