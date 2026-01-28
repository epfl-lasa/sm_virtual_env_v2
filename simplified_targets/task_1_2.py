from template_values_static_targets import *
from utils import *

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]

targets = [tr_top]
data_array = []
id_counter = 1

for t1 in targets:
    for t2 in targets:
        for t3 in targets:
            entry = copy.deepcopy(dict_template_target)
            entry["id"] = id_counter
            entry["left_hand"]["target_pose"] = t1
            entry["right_hand"]["target_pose"] = t2
            entry["left_foot"]["target_pose"] = t3
            data_array.append(entry)
            id_counter += 1

save_data_array_to_csv(data_array, f"logs/S_{SUBJECT_ID}/simplified_targets/", f"{script_name}_targets.csv")
data_task_1_2 = data_array