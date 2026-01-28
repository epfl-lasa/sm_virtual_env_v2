from defs_parameters import *
from functions.funcs_pygame import *
from functions.funcs_phase_management import *
from functions.utils import *
from defined_targets.template_values_static_targets import *
from motive.parse_received_packets import *

import pygame
from enum import Enum, auto
import imageio


class TaskState(Enum):
    PRE_TASK = auto()
    TASK_START = auto()
    TASK_RUNNING = auto()
    TASK_PERTURBED = auto()
    TASK_FINISHING = auto()
    TASK_DONE = auto()


flag_keyboard = False
left_hand_enabled = False
right_hand_enabled = False
left_foot_enabled = False
right_foot_enabled = False


def on_press2(key):
    global flag_keyboard
    if key == keyboard.KeyCode.from_char("v"):
        flag_keyboard = True


def update_target_object_on_screen(screen, interface, target_pose):
    tmp = get_converted_target_pose_on_screen(
        target_pose.copy(), get_idx_side_type(interface)[1]
    )
    icon = load_icon(
        get_icon_target_object(interface)[0],
        new_height=get_icon_target_object(interface)[1],
    )
    place_icon_on_screen(screen, icon, tmp)


def update_player_object_on_screen(screen, interface, flag_initial):
    if flag_initial:
        tmp = get_initial_player_object_pose_on_screen(interface)
    else:
        tmp = get_player_object_pose_on_screen(interface)
    icon = load_icon(
        get_icon_moving_object(interface)[0],
        new_height=get_icon_target_object(interface)[1],
    )
    place_icon_on_screen(screen, icon, tmp)


def compute_distance(interface, target, initial):
    current = get_player_object_pose_on_screen(interface)
    total_distance = np.linalg.norm(target - initial)
    current_distance = np.linalg.norm(target - current)
    remaining_distance = current_distance / total_distance
    return current_distance, remaining_distance


def get_side(limb_name: str) -> str:
    limb_name = limb_name.lower()
    if limb_name.startswith("left"):
        return "left"
    elif limb_name.startswith("right"):
        return "right"
    else:
        return "unknown"


def run_task(
    screen, clock, targets_info, subject_id, phase, task_name, limbs_to_perturb
):

    global flag_keyboard
    global left_hand_enabled
    global right_hand_enabled
    global left_foot_enabled
    global right_foot_enabled

    left_hand_enabled = False
    right_hand_enabled = False
    left_foot_enabled = False
    right_foot_enabled = False

    left_hand_target_pose = None
    right_hand_target_pose = None
    left_foot_target_pose = None
    right_foot_target_pose = None

    employed_interfaces = []
    is_perturbed = False

    id_target = targets_info.get("id", None)
    for i, d in targets_info.items():

        if i != "id":
            if i == INTERFACES[0]["name"] and d["target_pose"] is not None:
                left_hand_enabled = True
                left_hand_target_pose = d["target_pose"].copy()
                employed_interfaces.append(INTERFACES[0]["name"])

            if i == INTERFACES[1]["name"] and d["target_pose"] is not None:
                right_hand_enabled = True
                right_hand_target_pose = d["target_pose"].copy()
                employed_interfaces.append(INTERFACES[1]["name"])

            if i == INTERFACES[2]["name"] and d["target_pose"] is not None:
                left_foot_enabled = True
                left_foot_target_pose = d["target_pose"].copy()
                employed_interfaces.append(INTERFACES[2]["name"])

            if i == INTERFACES[3]["name"] and d["target_pose"] is not None:
                right_foot_enabled = True
                right_foot_target_pose = d["target_pose"].copy()
                employed_interfaces.append(INTERFACES[3]["name"])

    if len(employed_interfaces) == 0:
        raise ValueError("No Interface is active! Exiting the script...")

    state = TaskState.PRE_TASK
    start_time = pygame.time.get_ticks()
    elapsed_sec = 0.0

    mat_targets = np.zeros((4, 3))
    lst_mat_targets = []

    frames = []

    while True:

        # screen setting and features
        screen.fill(BG_COLOR)

        draw_horizontal_line(screen, position_y=PX_HEIGHT_OFFSET)
        draw_vertical_line(screen, position_y=PX_HEIGHT_OFFSET)
        place_overlay(screen, location="top", alpha=125)

        if not left_hand_enabled and not left_foot_enabled:
            place_overlay(screen, location="left", alpha=125)
        if not right_hand_enabled and not right_foot_enabled:
            place_overlay(screen, location="right", alpha=125)

        # Place the active targets
        if left_hand_enabled:
            mat_targets[0] = left_hand_target_pose.copy()
            update_target_object_on_screen(
                screen, INTERFACES[0]["name"], left_hand_target_pose.copy()
            )

        if right_hand_enabled:
            mat_targets[1] = right_hand_target_pose.copy()
            update_target_object_on_screen(
                screen, INTERFACES[1]["name"], right_hand_target_pose.copy()
            )

        if left_foot_enabled:
            mat_targets[2] = left_foot_target_pose.copy()
            update_target_object_on_screen(
                screen, INTERFACES[2]["name"], left_foot_target_pose.copy()
            )

        if right_foot_enabled:
            mat_targets[3] = right_foot_target_pose.copy()
            update_target_object_on_screen(
                screen, INTERFACES[3]["name"], right_foot_target_pose.copy()
            )

        match state:
            case TaskState.PRE_TASK:
                THRSH_TIME = 2.5
                if elapsed_sec < THRSH_TIME:
                    timer_msg = f"Wait!"
                    timer_font_color = BLUE
                    for interface in employed_interfaces:
                        update_init_pose_player_object(interface)
                        update_player_object_on_screen(screen, interface, True)
                    elapsed_sec = reverse_timer(
                        screen, start_time, THRSH_TIME, timer_msg, timer_font_color
                    )[1]
                else:
                    state = TaskState.TASK_START

            case TaskState.TASK_START:
                timer_msg = "Move!"
                timer_font_color = DARK_GREEN
                reset_pose_informtion_lists()
                clear_flag_hand_interfaces()
                clear_flag_foot_interfaces()
                elapsed_sec = 0
                lst_mat_targets.clear()
                lst_elapsed_sec.clear()
                start_time = pygame.time.get_ticks()
                state = TaskState.TASK_RUNNING

            case TaskState.TASK_RUNNING:
                lst_mat_targets.append(copy.deepcopy(mat_targets))
                lst_elapsed_sec.append(elapsed_sec)
                elapsed_sec = upward_timer(
                    screen, start_time, timer_msg, timer_font_color
                )

                # if (limbs_to_perturb): is_perturbed = True
                # else: is_perturbed = False

                for interface in employed_interfaces:
                    update_pose_player_object(interface)
                    update_player_object_on_screen(screen, interface, False)

                    if limbs_to_perturb and limbs_to_perturb == interface:

                        if get_side(limbs_to_perturb) == "left":
                            ceneter_point = np.array(
                                [
                                    PX_WS_WIDTH // 2,
                                    PX_WS_HEIGHT // 2 + PX_HEIGHT_OFFSET,
                                    0,
                                ]
                            )
                        else:
                            ceneter_point = np.array(
                                [
                                    PX_WS_WIDTH * (3.0 / 2.0),
                                    PX_WS_HEIGHT // 2 + PX_HEIGHT_OFFSET,
                                    0,
                                ]
                            )

                        match limbs_to_perturb:
                            case "left_hand":
                                target = left_hand_target_pose.copy()
                            case "right_hand":
                                target = right_hand_target_pose.copy()
                                target[0] += np.array([PX_WS_WIDTH * (3.0 / 2.0)])
                            case "left_foot":
                                target = left_foot_target_pose.copy()
                            case "right_foot":
                                target = right_foot_target_pose.copy()
                                target[0] += np.array([PX_WS_WIDTH * (3.0 / 2.0)])
                            case _:
                                pass

                        if (
                            compute_distance(interface, target, ceneter_point)[1]
                            <= 0.60
                        ):
                            match limbs_to_perturb:
                                case "left_hand":
                                    left_hand_target_pose[:2] -= np.array([0, -250])
                                case "right_hand":
                                    right_hand_target_pose[:2] -= np.array([0, -250])
                                case "left_foot":
                                    left_foot_target_pose[:2] -= np.array([0, -250])
                                case "right_foot":
                                    right_foot_target_pose[:2] -= np.array([0, -250])
                                case _:
                                    pass

                            state = TaskState.TASK_PERTURBED

                update_pose_information_lists()

                # Time warning
                if elapsed_sec > (MAX_TASK_DURATION - MAX_WARNING_END_TIME):
                    timer_msg = f"Finishing!"
                    timer_font_color = RED

                # End condition reached
                if elapsed_sec > MAX_TASK_DURATION or flag_keyboard:
                    flag_keyboard = False
                    state = TaskState.TASK_FINISHING

            case TaskState.TASK_PERTURBED:
                lst_mat_targets.append(mat_targets)
                lst_elapsed_sec.append(elapsed_sec)
                elapsed_sec = upward_timer(
                    screen, start_time, timer_msg, timer_font_color
                )

                for interface in employed_interfaces:
                    update_pose_player_object(interface)
                    update_player_object_on_screen(screen, interface, False)

                update_pose_information_lists()

                # Time warning
                if elapsed_sec > (MAX_TASK_DURATION - MAX_WARNING_END_TIME):
                    timer_msg = f"Finishing!"
                    timer_font_color = RED

                # End condition reached
                if elapsed_sec > MAX_TASK_DURATION or flag_keyboard:
                    flag_keyboard = False
                    state = TaskState.TASK_FINISHING

            case TaskState.TASK_FINISHING:

                if phase == "training" or phase == "baseline":
                    parent_path = f"logs/S_{subject_id}/data/{phase}/"

                else:
                    if limbs_to_perturb:
                        parent_path = f"logs/S_{subject_id}/data/{phase}/{task_name}_{limbs_to_perturb}"
                    else:
                        parent_path = f"logs/S_{subject_id}/data/{phase}/{task_name}"

                save_all_vars(parent_path, id_target, lst_mat_targets, frames)

                info_type = "after_task"
                msg = "Return to the initial position"
                if show_information(
                    screen, clock, info_type, DURATION_GO_TO_HOME_LOCATION, msg=msg
                ):
                    state = TaskState.TASK_DONE

            case TaskState.TASK_DONE:
                break

        # Capture the frame (convert to RGB array)
        frame = pygame.surfarray.array3d(pygame.display.get_surface())
        frame = np.rot90(frame, 3)  # Rotate to correct orientation
        frame = np.flip(frame, axis=1)  # Flip horizontally

        # Pad height if odd
        if frame.shape[0] % 2 != 0:
            frame = np.pad(frame, ((0, 1), (0, 0), (0, 0)), mode="constant")
        # Pad width if odd
        if frame.shape[1] % 2 != 0:
            frame = np.pad(frame, ((0, 0), (0, 1), (0, 0)), mode="constant")

        frames.append(frame)

        pygame.display.flip()
        clock.tick(TICK_VALUE)
