import random
import os
import copy
from source.utils import has_3_values_in_a_row
# Setting the working directory to the project directory
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

#######################################################################################################################
## PARAMETERS
#######################################################################################################################
EXPERIMENT_NAME = 'ODO_03_PRE'
NUM_TRIALS = 12
POSSIBLE_CHANNELS_1 = [1,2]
POSSIBLE_CHANNELS_2 = [3,4]
TOTAL_RUNS = 4

POSSIBLE_CHANNELS = [POSSIBLE_CHANNELS_1,POSSIBLE_CHANNELS_2]
# the script will generate TOTAL_RUNS x NUM_SNIFFS randomized channel-numbers, alternating between
# POSSIBLE_CHANNELS_1 and POSSIBLE_CHANNELS_2
#######################################################################################################################
## START
#######################################################################################################################
save_path = os.path.join('outputs','randomized_stuff',EXPERIMENT_NAME + '_rand.txt')

all_sniffs = []

for i in range(TOTAL_RUNS):
    #building the skeleton list
    i_mod = i % 2
    list = [POSSIBLE_CHANNELS[i_mod][0] for _ in range(int(NUM_TRIALS/2))] + [POSSIBLE_CHANNELS[i_mod][1] for _ in range(int(NUM_TRIALS/2))]
    while(True):
        random.shuffle(list)
        if not has_3_values_in_a_row(list):
            break
    all_sniffs.append(copy.deepcopy(list))
'''for i in range(TOTAL_RUNS):
    i_mod = i % 2
    run_sniffs = []
    for j in range(NUM_TRIALS):
        sniff = random.choice(POSSIBLE_CHANNELS[i_mod])
        if j > 1 and sniff == run_sniffs[-1] == run_sniffs[-2]:
            for option in POSSIBLE_CHANNELS[i_mod]:
                if option != sniff:
                    sniff = option
                    break
        run_sniffs.append(sniff)
    all_sniffs.append(copy.deepcopy(run_sniffs))'''

with open(save_path,'w') as file:
    file.write(f'GENERAL_EXPERIMENT_NAME = \'{EXPERIMENT_NAME}\'')
    file.write('\nall_stims = []')
    for i, run_sniffs in enumerate(all_sniffs):
        file.write(f'\nall_stims.append([')
        for j, sniff in enumerate(run_sniffs):
            file.write(f'{sniff}')
            if j != len(run_sniffs) - 1:
                file.write(',')
        file.write(f']) #RUN{i + 1}')