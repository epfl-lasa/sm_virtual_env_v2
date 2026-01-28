from defined_targets.template_values_static_targets import *
from defined_targets.utils import *

limbs = ["left_hand", "right_hand", "left_foot", "right_foot"]
targets = [tr_top, tr_bottom]
data_array = []
id_counter = 1

for target_combo in itertools.product(targets, repeat=4):
    entry = copy.deepcopy(dict_template_target)
    entry["id"] = id_counter
    for limb, target in zip(limbs, target_combo):
        entry[limb]["target_pose"] = target
    data_array.append(entry)
    id_counter += 1

random.shuffle(data_array)
save_data_array_to_csv(data_array, f"logs/S_{SUBJECT_ID}/targets/", f"task_4_targets.csv")

data_task_4 = data_array