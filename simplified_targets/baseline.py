from defined_targets.template_values_static_targets import *
from defined_targets.utils import *

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]

limbs = ["left_hand", "right_hand", "left_foot", "right_foot"]
targets = [tr_top]
data_array = []
id_counter = 1

for limb in limbs:
    for target in targets:
        entry = copy.deepcopy(dict_template_target)
        entry["id"] = id_counter
        entry[limb]["target_pose"] = target
        data_array.append(entry)
        id_counter += 1

random.shuffle(data_array)
save_data_array_to_csv(data_array, f"logs/S_{SUBJECT_ID}/simplified_targets/", f"{script_name}_targets.csv")
data_baseline = data_array