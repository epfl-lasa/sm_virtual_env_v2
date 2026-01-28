from template_values_static_targets import *
from utils import *

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]

limb_pairs = [("left_hand", "right_foot")]

targets = [tr_top]
data_array = []
id_counter = 1

for limb1, limb2 in limb_pairs:
    for t1 in targets:
        for t2 in targets:
            entry = copy.deepcopy(dict_template_target)
            entry["id"] = id_counter
            entry[limb1]["target_pose"] = t1
            entry[limb2]["target_pose"] = t2
            data_array.append(entry)
            id_counter += 1

save_data_array_to_csv(data_array, f"logs/S_{SUBJECT_ID}/simplified_targets/", f"{script_name}_targets.csv")
data_task_3_2 = data_array