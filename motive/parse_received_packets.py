import os
import pickle
import copy
from datetime import datetime
import imageio
from functions.defs_pygame import *
from functions.funcs_rotations import *
from functions.funcs_pygame import *
from motive.defs_udp import *

SAVE_VARS = True  # save data using pickle or not?
ONE_MOTION_INTERFACE = True
# ONE_MOTION_INTERFACE = False

TASK_DIM = 3
HAND_INTERFACES_DIM = 2
FOOT_INTERFACES_DIM = 2

# flags
flag_foot_interfaces = [False, False]
flag_hand_interfaces = [False, False]

mt_hands_pose = np.zeros((HAND_INTERFACES_DIM, TASK_DIM))
px_hands_pose = np.zeros((HAND_INTERFACES_DIM, TASK_DIM))
mt_feet_pose = np.zeros((FOOT_INTERFACES_DIM, TASK_DIM))
px_feet_pose = np.zeros((FOOT_INTERFACES_DIM, TASK_DIM))

mt_hands_pose_init = np.zeros((HAND_INTERFACES_DIM, TASK_DIM))
px_hands_pose_init = np.zeros((HAND_INTERFACES_DIM, TASK_DIM))
mt_feet_pose_init = np.zeros((FOOT_INTERFACES_DIM, TASK_DIM))
px_feet_pose_init = np.zeros((FOOT_INTERFACES_DIM, TASK_DIM))

# save the time series
lst_elapsed_sec = []

# to save them for plotting and analysis (pickle lib)
lst_px_hands_pose = []
lst_mt_hands_pose = []
lst_px_feet_pose = []
lst_mt_feet_pose = []

# raw data from mocap
mocap_hands = np.zeros((HAND_INTERFACES_DIM, 7))
mocap_feet = np.zeros((HAND_INTERFACES_DIM, 7))
lst_mocap_hands = []
lst_mocap_feet = []


def get_idx_side_type(interface):
    # return the index (idx), side of each interface (left or right) and type of each interface (hand or foot)
    if interface == INTERFACES[0]["name"] or interface == INTERFACES[0]["udp_id"]:
        return 0, "left", "hand"
    elif interface == INTERFACES[1]["name"] or interface == INTERFACES[1]["udp_id"]:
        return 1, "right", "hand"
    elif interface == INTERFACES[2]["name"] or interface == INTERFACES[2]["udp_id"]:
        return 0, "left", "foot"
    elif interface == INTERFACES[3]["name"] or interface == INTERFACES[3]["udp_id"]:
        return 1, "right", "foot"
    elif interface is None:
        return "None"
    else:
        return -1


def udp_hands():
    global mt_hands_pose
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((UDP_IP, UDP_PORT_HANDS))

        while True:
            data, addr = server_socket.recvfrom(1024)
            parts = data.decode().split(":")

            if int(parts[0]) == INTERFACES[0]["udp_id"]:
                idx = get_idx_side_type(INTERFACES[0]["name"])[0]
                mt_hands_pose[idx, :] = get_pose_2d_mocap(
                    eval(parts[1]), eval(parts[2])
                )
                mocap_hands[idx, :3] = eval(parts[1])
                mocap_hands[idx, 3:] = eval(parts[2])

            elif int(parts[0]) == INTERFACES[1]["udp_id"]:
                idx = get_idx_side_type(INTERFACES[1]["name"])[0]
                mt_hands_pose[idx, :] = get_pose_2d_mocap(
                    eval(parts[1]), eval(parts[2])
                )
                mocap_hands[idx, :3] = eval(parts[1])
                mocap_hands[idx, 3:] = eval(parts[2])

            else:
                pass


def udp_feet():

    global mt_feet_pose
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((UDP_IP, UDP_PORT_FEET))

        while True:

            data, addr = server_socket.recvfrom(1024)
            parts = data.decode().split(":")

            if int(parts[0]) == INTERFACES[2]["udp_id"]:
                idx = get_idx_side_type(INTERFACES[2]["name"])[0]
                mt_feet_pose[idx, :] = get_pose_2d_mocap(eval(parts[1]), eval(parts[2]))
                mocap_feet[idx, :3] = eval(parts[1])
                mocap_feet[idx, 3:] = eval(parts[2])

            elif int(parts[0]) == INTERFACES[3]["udp_id"]:
                idx = get_idx_side_type(INTERFACES[3]["name"])[0]
                mt_feet_pose[idx, :] = get_pose_2d_mocap(eval(parts[1]), eval(parts[2]))
                mocap_feet[idx, :3] = eval(parts[1])
                mocap_feet[idx, 3:] = eval(parts[2])

            else:
                pass


def get_pose_2d_mocap(position, quaternion):
    # theta = compute_correct_angle(quaternion)
    theta = 0.0
    return np.array([position[2], -position[0], theta])


def get_converted_target_pose_on_screen(pose, side):
    if side == "right":
        return pose + np.array([PX_WS_WIDTH, 0, 0])
    else:
        return pose


def get_initial_player_object_pose_on_screen(interface):
    HORIZONTAL_OFFSET = 0
    out = np.array([0.0, 0.0, 0.0])
    orientation_0 = 0.0
    if interface == INTERFACES[0]["name"]:
        out[0] = PX_WS_WIDTH / 2 + HORIZONTAL_OFFSET // 2
        out[1] = PX_WS_HEIGHT / 2 + PX_HEIGHT_OFFSET
        out[2] = orientation_0
    elif interface == INTERFACES[1]["name"]:
        out[0] = PX_WS_WIDTH + PX_WS_WIDTH / 2 + HORIZONTAL_OFFSET // 2
        out[1] = PX_WS_HEIGHT / 2 + PX_HEIGHT_OFFSET
        out[2] = orientation_0
    elif interface == INTERFACES[2]["name"]:
        out[0] = PX_WS_WIDTH / 2 - HORIZONTAL_OFFSET // 2
        out[1] = PX_WS_HEIGHT / 2 + PX_HEIGHT_OFFSET
        out[2] = orientation_0
    elif interface == INTERFACES[3]["name"]:
        out[0] = PX_WS_WIDTH + PX_WS_WIDTH / 2 - HORIZONTAL_OFFSET // 2
        out[1] = PX_WS_HEIGHT / 2 + PX_HEIGHT_OFFSET
        out[2] = orientation_0
    else:
        pass
    return out


def get_player_object_pose_on_screen(interface):
    out = np.array([0.0, 0.0, 0.0])
    idx = get_idx_side_type(interface)[0]
    if interface == INTERFACES[0]["name"]:
        out = px_hands_pose[idx, :]
    elif interface == INTERFACES[1]["name"]:
        out = px_hands_pose[idx, :]
    elif interface == INTERFACES[2]["name"]:
        out = px_feet_pose[idx, :]
    elif interface == INTERFACES[3]["name"]:
        out = px_feet_pose[idx, :]
    else:
        pass
    return out


def relative_conversion_cartesian_to_pixel(
    mt_pose, mt_pose_init, px_pose_init, interface
):
    # TODO: rotation
    # TODO: check the scales
    WS_PX_MAX = np.array([PX_WS_WIDTH / 2, PX_WS_HEIGHT / 2, 180.0])

    if get_idx_side_type(interface)[2] == "hand":
        WS_MT_MAX = np.array([0.12, 0.12, 0])
    else:
        WS_MT_MAX = np.array([0.12, 0.12, 0])

    delta = mt_pose - mt_pose_init

    scale = np.array([0.0, 0.0, 0.0])
    scale[0] = WS_PX_MAX[0] / WS_MT_MAX[0]
    scale[1] = WS_PX_MAX[1] / WS_MT_MAX[1]
    scale[2] = 1

    px_pose = delta * scale + px_pose_init
    px_pose = saturate_pixel_space(interface, px_pose)

    return px_pose


def update_init_pose_player_object(interface):
    idx = get_idx_side_type(interface)[0]
    if get_idx_side_type(interface)[2] == "hand":
        px_hands_pose_init[idx, :] = get_initial_player_object_pose_on_screen(interface)
        mt_hands_pose_init[idx, :] = mt_hands_pose[idx, :]
    else:
        px_feet_pose_init[idx, :] = get_initial_player_object_pose_on_screen(interface)
        mt_feet_pose_init[idx, :] = mt_feet_pose[idx, :]

    # update_pose_informtion_lists()


def update_pose_player_object(interface):
    idx = get_idx_side_type(interface)[0]
    if get_idx_side_type(interface)[2] == "hand":
        px_hands_pose[idx, :] = relative_conversion_cartesian_to_pixel(
            mt_hands_pose[idx, :],
            mt_hands_pose_init[idx, :],
            px_hands_pose_init[idx, :],
            interface,
        )
    else:
        px_feet_pose[idx, :] = relative_conversion_cartesian_to_pixel(
            mt_feet_pose[idx, :],
            mt_feet_pose_init[idx, :],
            px_feet_pose_init[idx, :],
            interface,
        )

    # update_pose_informtion_lists()


def saturate_pixel_space(interface, pose):
    pose_2d = np.array([pose[0], pose[1]])

    if get_idx_side_type(interface)[1] == "left":
        limit_min = np.array([0.0, PX_HEIGHT_OFFSET])
        limit_max = np.array([PX_WS_WIDTH, SCREEN_HEIGHT])

    elif get_idx_side_type(interface)[1] == "right":
        limit_min = np.array([PX_WS_WIDTH, PX_HEIGHT_OFFSET])
        limit_max = np.array([SCREEN_WIDTH, SCREEN_HEIGHT])

    tmp = np.clip(pose_2d, limit_min, limit_max)
    return np.array([tmp[0], tmp[1], pose[2]])


def clear_flag_hand_interfaces():
    global flag_hand_interfaces
    flag_hand_interfaces = [False, False]


def clear_flag_foot_interfaces():
    global flag_foot_interfaces
    flag_foot_interfaces = [False, False]


def reset_pose_informtion_lists():
    global lst_mt_hands_pose, lst_px_hands_pose, lst_mt_feet_pose, lst_px_feet_pose, lst_mocap_hands, lst_mocap_feet
    lst_mt_hands_pose.clear()
    lst_px_hands_pose.clear()
    lst_mt_feet_pose.clear()
    lst_px_feet_pose.clear()
    lst_mocap_hands.clear()
    lst_mocap_feet.clear()


def update_pose_information_lists():
    global lst_mt_hands_pose, lst_px_hands_pose, lst_mt_feet_pose, lst_px_feet_pose, lst_mocap_hands, lst_mocap_feet
    global mt_hands_pose, px_hands_pose, mt_feet_pose, px_feet_pose, mocap_hands, mocap_feet
    lst_mt_hands_pose.append(copy.deepcopy(mt_hands_pose))
    lst_px_hands_pose.append(copy.deepcopy(px_hands_pose))
    lst_mt_feet_pose.append(copy.deepcopy(mt_feet_pose))
    lst_px_feet_pose.append(copy.deepcopy(px_feet_pose))
    lst_mocap_hands.append(copy.deepcopy(mocap_hands))
    lst_mocap_feet.append(copy.deepcopy(mocap_feet))


def reset_pose_information():
    global mt_hands_pose, px_hands_pose, mt_feet_pose, px_feet_pose, mocap_hands, mocap_feet
    mt_hands_pose = np.zeros_like(mt_hands_pose)
    px_hands_pose = np.zeros_like(px_hands_pose)
    mt_feet_pose = np.zeros_like(mt_feet_pose)
    px_feet_pose = np.zeros_like(px_feet_pose)
    mocap_hands = np.zeros_like(mocap_hands)
    mocap_feet = np.zeros_like(mocap_feet)


def save_all_vars(parent_path, subtask_id, targets, video_frames):
    global lst_mt_hands_pose, lst_px_hands_pose, lst_mt_feet_pose, lst_px_feet_pose

    if SAVE_VARS:
        # time stamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dir = parent_path + f"/{subtask_id}/{timestamp}"

        os.makedirs(dir, exist_ok=True)

        with open(f"{dir}/desired-targets.pkl", "wb") as file:
            pickle.dump(targets, file)

        with open(f"{dir}/elapsed-time.pkl", "wb") as file:
            pickle.dump(lst_elapsed_sec, file)

        # hands data
        with open(f"{dir}/hands-px-pose.pkl", "wb") as file:
            pickle.dump(lst_px_hands_pose, file)
        with open(f"{dir}/hands-mt-pose.pkl", "wb") as file:
            pickle.dump(lst_mt_hands_pose, file)
        with open(f"{dir}/hands-mocap-all.pkl", "wb") as file:
            pickle.dump(lst_mocap_hands, file)

        # feet data
        with open(f"{dir}/feet-px-pose.pkl", "wb") as file:
            pickle.dump(lst_px_feet_pose, file)
        with open(f"{dir}/feet-mt-pose.pkl", "wb") as file:
            pickle.dump(lst_mt_feet_pose, file)
        with open(f"{dir}/feet-mocap-all.pkl", "wb") as file:
            pickle.dump(lst_mocap_feet, file)

        imageio.mimwrite(
            f"{dir}/video.mp4", video_frames, fps=60, quality=6, macro_block_size=None
        )
