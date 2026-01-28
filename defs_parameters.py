INTERFACES = [
    {"name": "left_hand", "udp_id": 1},
    {"name": "right_hand", "udp_id": 2},
    {"name": "left_foot", "udp_id": 3},
    {"name": "right_foot", "udp_id": 4},
]

MAX_TASK_DURATION = 75
MAX_WARNING_END_TIME = 5  # [MAX_WARNING_END_TIME] seconds before [MAX_TASK_DURATION]
DURATION_PHASE_INTRO = 3
DURATION_TASK_INTRO = 3
DURATION_GO_TO_HOME_LOCATION = 1

WAIT_TIME = 0.25  # short delay throught the code time.sleep(WAIT_TIME)

# Screen dimensions (division: left and right sides)
PX_WS_WIDTH = 280
SCREEN_WIDTH = PX_WS_WIDTH * 2
PX_WS_HEIGHT = 700
PX_HEIGHT_OFFSET = PX_WS_HEIGHT // 5.5
SCREEN_HEIGHT = PX_WS_HEIGHT + PX_HEIGHT_OFFSET
PX_BORDER = PX_WS_WIDTH // 3.75  # for target placement

print(PX_WS_HEIGHT / 2 + PX_HEIGHT_OFFSET + PX_BORDER)
print(PX_WS_HEIGHT / 2 + PX_HEIGHT_OFFSET)

# color definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (153, 102, 204)
DARK_GREEN = (0, 150, 0)
BG_COLOR = WHITE

# Icons directory
DIR_ICN_LEFT_HAND = "icons/left_hand.png"
DIR_ICN_RIGHT_HAND = "icons/right_hand.png"
DIR_ICN_LEFT_FOOT = "icons/left_foot.png"
DIR_ICN_RIGHT_FOOT = "icons/right_foot.png"

DIR_ICN_LEFT_HAND_TGT = "icons/left_hand_target.png"
DIR_ICN_RIGHT_HAND_TGT = "icons/right_hand_target.png"
DIR_ICN_LEFT_FOOT_TGT = "icons/left_foot_target.png"
DIR_ICN_RIGHT_FOOT_TGT = "icons/right_foot_target.png"


# Icons scaling factor
ICN_HEIGHT_SCALING = 100
ICON_SCALING_HAND = 90
ICON_SCALING_FOOT = 140


# definitions used in the phase management script
FONT_SIZE_BIG = int(PX_WS_HEIGHT / 12) - 10
FONT_SIZE_NORMAL = int(PX_WS_HEIGHT / 13) - 10
FONT_SIZE_SMALL = int(PX_WS_HEIGHT / 14) - 10
TXT_Y_INIT = PX_HEIGHT_OFFSET + 100
TICK_VALUE = 60.0
