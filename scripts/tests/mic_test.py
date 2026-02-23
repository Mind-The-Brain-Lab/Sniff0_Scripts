import sounddevice as sd
import os
from scipy.io.wavfile import write
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np
print(sd.query_devices()[1]) # Lists all input/output devices
mic_index = 1  # Change this to the correct index from the list

#sd.default.device = (mic_index, None)
sd.default.device = ('Microfono (USB Audio CODEC ), MME', None)  # Use device name'''
recording = sd.rec(3*44100, samplerate=44100, channels=1)

sd.wait()
write(os.path.join('C:\\Users\\neuroscienze\\PycharmProjects\\Sniff0_Scripts\\.trash','prova.wav'), 44100, recording)

