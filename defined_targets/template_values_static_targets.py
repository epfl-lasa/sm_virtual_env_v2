import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from exp_config import *
from defs_parameters import *

orientation_default = 0

# translational targets
tr_top = np.array([PX_WS_WIDTH // 2, 
                   PX_HEIGHT_OFFSET + PX_BORDER, 
                   orientation_default])

tr_bottom = np.array([PX_WS_WIDTH // 2, 
                      SCREEN_HEIGHT-PX_BORDER, 
                      orientation_default])

dict_template_target = {
    "id": None, 
    "left_hand": {"target_pose": None},
    "right_hand": {"target_pose": None},
    "left_foot": {"target_pose": None},
    "right_foot": {"target_pose": None}
}
