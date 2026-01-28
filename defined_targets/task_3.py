from defined_targets.template_values_static_targets import *
from defined_targets.utils import *

limbs = ["left_hand", "right_hand", "left_foot", "right_foot"]

targets = [tr_top, tr_bottom]
triplets = list(itertools.combinations(limbs, 3))
data_array = []
id_counter = 1

for triplet in triplets:
    # all 2^3 = 8 combinations of tr_top/tr_bottom
    for target_combo in itertools.product(targets, repeat=3):
        entry = copy.deepcopy(dict_template_target)
        entry["id"] = id_counter
        for limb, target in zip(triplet, target_combo):
            entry[limb]["target_pose"] = target
        data_array.append(entry)
        id_counter += 1

random.shuffle(data_array)
save_data_array_to_csv(data_array, f"logs/S_{SUBJECT_ID}/targets/", f"task_3_targets.csv")

data_task_3 = data_array