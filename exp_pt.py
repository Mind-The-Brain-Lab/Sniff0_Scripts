import pandas as pd
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import visual, event, core, logging
from datetime import datetime
import os , shutil
from source.olfattometro import Olfactometer
from source.utils import MicrophoneWrapper,get_randomization
from scipy.io.wavfile import write
from source.triggerbox import TriggerBox, FakeTriggerBox
from pathlib import Path
import random
from collections import defaultdict
#######################################################################################################################
## MEGA IMPORTANT PARAMETERS
#######################################################################################################################
RUN_NUMBER = 2 # START FROM 1!!! (1 <= RUN_NUMBER <= 4)
DEBUGGING = True #PUT THAT TO FALSE TO COMMUNICATE WITH THE OLFACTOMETER
FULLSCREEN = False #DEBUGGING FULLSCREEN
#######################################################################################################################
## JITTERED ODORS AND EXPERIMENT NAME
#################################################################0######################################################
GENERAL_EXPERIMENT_NAME = 'p1-pt'

TOTAL_RUNS = 2
TRIALS_PER_RUN = 24
CHANNELS = [1, 2]

all_stims = get_randomization(total_runs=TOTAL_RUNS, trials_per_run=TRIALS_PER_RUN, channels=CHANNELS)
#print(all_stims)
#######################################################################################################################
## OTHER PARAMETERS
#######################################################################################################################
NUM_SNIFFS = 1 #number of (pulses + rest) cycles in each stimulus administration
SNIFFING_QUESTION = 'Che odore hai sentito?'

# Durations in seconds
RESPONSE_DURATION= 0 #time windows for the answer
STIM_DURATION = 8 #durations of each odor pulse
STOP_DURATION = 0 #isi time between each odor pulse
REST_DURATION = 12

AUDIO_SAMPLE_RATE = 44100
SCREEN_HZ = 60
#######################################################################################################################
## PATHS
#######################################################################################################################
outputs_path = Path(__file__).parent/'outputs'
tmp_dir = outputs_path/'tmp'
log_dir = outputs_path/'logs'
zip_dir = outputs_path/'zips'
#######################################################################################################################
## SETUP OF ALL THE USEFUL TOOLS
#######################################################################################################################
stims = all_stims[RUN_NUMBER - 1]
recorded_clips =[]
EXPERIMENT_NAME = f'RUN_{RUN_NUMBER}_{GENERAL_EXPERIMENT_NAME}'
# Remove frame rate measurement to avoid getting stuck
prefs.general['FrameRateMeasurementMode'] = 'none'

# Set working directory to the script’s parent directory (useful to avoid specifying the absolute paths)

# Creating all the directories (if not present)
os.makedirs(outputs_path,exist_ok=True)
os.makedirs(outputs_path/'logs', exist_ok=True)
os.makedirs(outputs_path/'zips', exist_ok=True)
os.makedirs(outputs_path/'tmp', exist_ok=True)
os.makedirs(outputs_path/'audio', exist_ok=True)

# Logging file logic
timestamp = datetime.now().strftime("%H-%M_%d-%m")
log_filename = f"exp_{EXPERIMENT_NAME}_{timestamp}.log"
log_path = outputs_path/'logs'/ log_filename
_ = logging.LogFile(log_path, level=logging.INFO)
logging.info("New experiment run started")

# Audio files logic
audio_file_paths = []
audio_dir_path = outputs_path/'audio'

# Create a fullscreen PsychoPy window with correct resolution. DO NOT CREATE MORE THAN ONE
if DEBUGGING:
    win = visual.Window(
        screen=1,
        fullscr=FULLSCREEN,
        color=(-1, -1, -1),  # Black background
        units="pix"
    )
else:
    win = visual.Window(
        screen = 1,
        fullscr=True,
        color=(-1, -1, -1),  # Black background
        units="pix"
    )

# Create a StaticPeriod object, useful for timing
static_period = core.StaticPeriod(screenHz=SCREEN_HZ)

# Assuming a 60 Hz refresh rate
win.refreshThreshold = 1.0 / 60.0
timer = core.Clock()

# Olfactometer object
olf = Olfactometer(timer,debugging=DEBUGGING,screenHz=SCREEN_HZ)
# Show black screen BEFORE trigger

# Microphone stuff
mic = MicrophoneWrapper(timer,debugging=DEBUGGING)

# Triggerbox struff
if not DEBUGGING:
    trig = TriggerBox()
else:
    trig = FakeTriggerBox()

win.flip()

#######################################################################################################################
## EXPERIMENT START
#######################################################################################################################
olf.openvalve()
core.wait(0.1)
dot = visual.ImageStim(win, image='multimedia/images/dot_white_proj.jpg',name='dot')
cross = visual.ImageStim(win, image='multimedia/images/fixation_white_proj.jpg',name='fixation')
question_text = visual.TextStim(win, text=SNIFFING_QUESTION, color=(-1, -1, -1), height=100, pos=(0, 0),name='question',flipVert=True)
# WaitING for trigger signal
trig.wait_trigger()
# Forcing white screen before entering the loop (sometimes it skips the first window)
win.color = [1,1,1]
win.flip()

cross.draw()
win.flip()

for stim in stims:
    # Show white screen during REST
    #Rest phase
    cross.draw()
    win.flip()
    static_period.start(REST_DURATION)
    logging.exp(f"REST {timer.getTime():.4f}")
    static_period.complete()

    dot.draw()
    win.flip()
    #Stimulus phase
    olf.stimulus_on(channel=stim,
                    stim_duration=STIM_DURATION,
                    stop_duration=STOP_DURATION,
                    repetition=NUM_SNIFFS
                    )

    # Asking the user a question and recording it
    if RESPONSE_DURATION != 0:
        static_period.start(RESPONSE_DURATION)
        mic.record(RESPONSE_DURATION,recorded_clips)
        question_text.draw()
        win.flip()
        logging.exp(f"QUEST {timer.getTime():.4f}")
        static_period.complete()

# Close PsychoPy properly
logging.exp(f"END {timer.getTime():.4f}")
cross.draw()
win.flip()
core.wait(24)
win.close()
#######################################################################################################################
## EXPERIMENT END. SAVING LOGIC
#######################################################################################################################
for i, clip in enumerate(recorded_clips):
    audio_filename = f"audio_{EXPERIMENT_NAME}_{timestamp}_N{i}.wav"
    audio_file_paths.append(audio_filename)
    write(audio_dir_path/audio_filename, AUDIO_SAMPLE_RATE, clip)


for file in tmp_dir.iterdir():
    file.unlink()

for audio_filename in audio_file_paths:
    shutil.copy(audio_dir_path/audio_filename, tmp_dir/audio_filename)
shutil.copy(log_dir/log_filename,tmp_dir/log_filename)

#time to create the excel file
df = pd.DataFrame(columns=['type','timestamp','argument'])
ok_values = ['QUEST','END','AUDIO_START','AUDIO_END','SNIFF','FIX','REST','TRIG','ISI']
with open(tmp_dir/log_filename, 'r') as file:
    for line in file:
        values = line.strip().split()
        if values[2] in ok_values:
            command_type = values[2]
            command_timestamp = values[3]
            if len(values) > 4:
                command_argument = values[4]
            else:
                command_argument = ' '
            new_row = {
                'type':command_type,
                'timestamp':command_timestamp,
                'argument': command_argument
            }
            df.loc[len(df)] = new_row
        else:
            continue
df.to_excel(tmp_dir/f"table_{EXPERIMENT_NAME}_{timestamp}.xlsx", index=False)
zip_name = zip_dir/f"results_{EXPERIMENT_NAME}_{timestamp}"
shutil.make_archive(str(zip_name), 'zip', tmp_dir)
for file in tmp_dir.iterdir():
    file.unlink()
core.quit()


