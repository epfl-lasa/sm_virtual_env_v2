import random
from functions.utils import *

SUBJECT_ID = 11
N = 5  # task repetition

# task sequence (order) - just tasks are randomised not the training and baseline!
# SCRIPT_SEQUENCE = ["training", "task1", "task2", "task3", "done"]
SCRIPT_SEQUENCE = ["task2", "done"]

tasks = [task for task in SCRIPT_SEQUENCE if "task" in task]
random.shuffle(tasks)

shuffled_sequence = []
for item in SCRIPT_SEQUENCE:
    if "task" in item:
        shuffled_sequence.append(tasks.pop(0))
    else:
        shuffled_sequence.append(item)


SCRIPT_SEQUENCE = shuffled_sequence
print(f">> Task sequence of subject {SUBJECT_ID}: {shuffled_sequence}")


add_sequence_to_csv(SUBJECT_ID, "/experiment_sequence/phases", shuffled_sequence)
