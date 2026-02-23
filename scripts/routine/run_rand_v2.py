import random
import os
import copy
from collections import defaultdict
from source.utils import has_3_values_in_a_row
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

EXPERIMENT_NAME = 'ODO_02_POST'
TOTAL_RUNS = 4
TRIALS_PER_RUN = 16
CHANNELS = [1, 2, 3, 4]

# Step 1: Assign each stim to 2 different runs
stim_run_assignments = defaultdict(list)
all_sniffs = [[] for _ in range(TOTAL_RUNS)]

for i in range(TOTAL_RUNS):
    for _ in range(int(TRIALS_PER_RUN/len(CHANNELS))):
        all_sniffs[i] += CHANNELS
    while (True):
        random.shuffle(all_sniffs[i])
        if not has_3_values_in_a_row(all_sniffs[i]):
            break

for i in range(TOTAL_RUNS):
    print(all_sniffs[i])
# Step 4: Save output
save_path = os.path.join('outputs', 'randomized_stuff', EXPERIMENT_NAME + '_rand.txt')
print(save_path)
print(os.getcwd())
os.makedirs(os.path.dirname(save_path), exist_ok=True)

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