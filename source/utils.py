import serial
from serial.tools import list_ports
import threading
from psychopy import core, logging
from typing import List
import sounddevice as sd
import numpy as np
from collections import defaultdict
import random
import copy

def get_randomization(total_runs,trials_per_run,channels):
    # Step 1: Assign each stim to 2 different runs
    stim_run_assignments = defaultdict(list)
    all_sniffs = [[] for _ in range(total_runs)]

    for i in range(total_runs):
        for _ in range(int(trials_per_run / len(channels))):
            all_sniffs[i] += channels
        while (True):
            random.shuffle(all_sniffs[i])
            if not has_3_values_in_a_row(all_sniffs[i]):
                break
    return all_sniffs

def get_randomization_pt(total_runs,trials_per_run,channels,ask_every:int):

    assert trials_per_run % ask_every == 0, "trials_per_run must be divisible by ask_every"

    all_sniffs = [[] for _ in range(total_runs)]

    for i in range(total_runs):
        normal_sniffs = []
        ask_sniffs = []
        normals = int(trials_per_run / len(channels)) - int(trials_per_run / (ask_every*len(channels)))
        for _ in range(normals):
            normal_sniffs += channels
        for _ in range(int((trials_per_run - normals) / len(channels))):
            ask_sniffs += channels
        while (True):
            actual_sniffs = []
            cp_ask = copy.deepcopy(ask_sniffs)
            cp_normal = copy.deepcopy(normal_sniffs)
            random.shuffle(cp_ask)
            random.shuffle(cp_normal)
            for j in range(trials_per_run):
                if (j+1) % ask_every == 0:
                    actual_sniffs.append(cp_ask.pop(0))
                else:
                    actual_sniffs.append(cp_normal.pop(0))

            if not has_3_values_in_a_row(actual_sniffs):
                all_sniffs[i] = actual_sniffs
                break
    return all_sniffs
def get_serial_port(device_hint:str = 'Arduino Due'):
    ports = list_ports.comports()

    if not ports:
        print("No serial devices found.")
        return

    for port in ports:
        if device_hint in port.description:
            return port.device

class MicrophoneWrapper:
    def __init__(self,timer,sample_rate = 44100, debugging:bool = False):
        self.static_period = core.StaticPeriod(screenHz=60)
        self.lock = threading.Lock()
        self.timer = timer
        self.sample_rate = sample_rate
        if not debugging:
            sd.default.device = ('Microfono (USB Audio CODEC ), MME', None)

        '''
        print(sd.query_devices())  # Lists all input/output devices
        mic_index = 1  # Change this to the correct index from the list

        sd.default.device = (mic_index, None) 
        sd.default.device = ("Your Microphone Name", None)  # Use device name
        '''
    def _record(self,duration:float,buffer:List):
        with self.lock:
            logging.exp(f"AUDIO_START {self.timer.getTime():.4f}")
        recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1)
        sd.wait()
        with self.lock:
            logging.exp(f"AUDIO_END {self.timer.getTime():.4f}")
            buffer.append(np.copy(recording))
    def record(self,duration:float,buffer:List):
        rec_thread = threading.Thread(target=self._record, args=(duration, buffer), daemon=True)
        rec_thread.start()

def has_3_values_in_a_row(list:List):
    for i in range(len(list) -2):
        if list[i] == list [i+1] == list[i + 2]:
            return True
    return False




