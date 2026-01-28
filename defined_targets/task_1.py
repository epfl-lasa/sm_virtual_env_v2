from defined_targets.template_values_static_targets import *
from defined_targets.utils import *


limb_pairs = [
    ("left_hand", "right_hand"),
    ("left_foot", "right_foot")
]

targets = [tr_top, tr_bottom]
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


random.shuffle(data_array)
save_data_array_to_csv(data_array, f"logs/S_{SUBJECT_ID}/targets/", f"task_1_targets.csv")

data_task_1 = data_array
