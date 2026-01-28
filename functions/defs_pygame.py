import time
import socket
import threading
import signal
import numpy as np
import pygame


INTERFACES = [
    {"name": "left_hand", "udp_id": 1},
    {"name": "right_hand", "udp_id": 2},
    {"name": "left_foot", "udp_id": 3},
    {"name": "right_foot", "udp_id": 4}
]

MAX_TASK_DURATION = 80
MAX_WARNING_END_TIME = 5 #[MAX_WARNING_END_TIME] seconds before [MAX_TASK_DURATION]
DURATION_PHASE_INTRO = 4
DURATION_TASK_INTRO = 4
DURATION_GO_TO_HOME_LOCATION = 3

WAIT_TIME = 0.25 # short delay throught the code time.sleep(WAIT_TIME)

# Screen dimensions (division: left and right sides)
PX_WS_WIDTH = 750
SCREEN_WIDTH = PX_WS_WIDTH*2
PX_WS_HEIGHT = PX_WS_WIDTH
PX_HEIGHT_OFFSET = PX_WS_WIDTH // 3
SCREEN_HEIGHT = PX_WS_HEIGHT + PX_HEIGHT_OFFSET

OFFSET_PX_LEFT_SIDE = np.array([0, 0, 0])
OFFSET_PX_RIGHT_SIDE = np.array([PX_WS_WIDTH, 0, 0])
PX_BORDER = PX_WS_WIDTH // 10 - 15 # for target placement

# color definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (153, 102, 204)
YELLOW = (255, 255, 0)

LIGHT_GREEN = (120, 255, 120)
LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (255, 182, 193)
LIGHT_ORANGE = (255, 204, 128)
LIGHT_PURPLE = (204, 153, 255)
LIGHT_YELLOW = (255, 255, 204)

BG_COLOR = WHITE 

# DISABLED_BG_COLOR = GREY

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
ICN_HEIGHT_SCALING = 120

# definitions used in the phase management script
FONT_SIZE_BIG = int(PX_WS_HEIGHT / 10) - 10
FONT_SIZE_NORMAL = int(PX_WS_HEIGHT / 11) - 10 
FONT_SIZE_SMALL = int(PX_WS_HEIGHT / 12) - 10
TXT_Y_INIT = PX_HEIGHT_OFFSET + 100
TICK_VALUE = 60.0