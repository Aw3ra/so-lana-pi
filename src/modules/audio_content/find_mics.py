import pyaudio

p = pyaudio.PyAudio().get_device_info_by_host_api_device_index(0, 0)
print(p)
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i, dev['name'], dev['maxInputChannels']))
    
