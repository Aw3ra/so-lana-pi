import pvporcupine
import alsaaudio
import struct
import audioop
import numpy as np
import os

# AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
access_key = os.environ["PICOVOICE_KEY"]

handle = pvporcupine.create(access_key=access_key, keyword_paths=['wakewords.ppn'])
print(handle.sample_rate, handle.frame_length)

inp = alsaaudio.PCM(
    alsaaudio.PCM_CAPTURE,
    channels=2,
    rate=handle.sample_rate,
    format=alsaaudio.PCM_FORMAT_S32_LE,
    periodsize=handle.frame_length,
    device='plughw:1,0'
)


audio_buffer = []

def get_next_audio_frame():
    global audio_buffer
    l, pcm_data = inp.read()
    if l <= 0:
        return None
    pcm_32 = np.frombuffer(pcm_data, dtype=np.int32)
    pcm_16 = (pcm_32 >> 16).astype(np.int16)
    # Convert stereo to mono (since you mentioned stereo input earlier)
    pcm_mono = [(pcm_16[i] + pcm_16[i + 1]) // 2 for i in range(0, len(pcm_16), 2)]

    # Amplify the mono signal
    amplification_factor = 3
    amplified_mono = [int(i * amplification_factor) for i in pcm_mono]

    # Add the amplified audio to the buffer
    audio_buffer += amplified_mono

    # If buffer has enough samples, pop them and return
    if len(audio_buffer) >= handle.frame_length:
        frame = audio_buffer[:handle.frame_length]
        audio_buffer = audio_buffer[handle.frame_length:]
        return frame
    return None

print("Started listening")
while True:
    frame = get_next_audio_frame()
    if frame:
        keyword_index = handle.process(frame)
        if keyword_index >= 0:
            print("hello!")



