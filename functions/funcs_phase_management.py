from functions.funcs_pygame import *
from defs_parameters import *
from functions.utils import *
import pygame


def show_information(
    screen,
    clock,
    info_type,
    duration,
    employed_interfaces=None,
    current_task_id=None,
    total_tasks_num=None,
    msg=None,
):

    if info_type == "phase":
        return show_phase_intro(screen, clock, duration, msg)

    elif info_type == "before_task":
        return show_info_before_task(
            screen,
            clock,
            duration,
            current_task_id,
            total_tasks_num,
            employed_interfaces,
        )

    elif info_type == "after_task":
        return show_info_after_task(screen, clock, duration, msg)

    elif info_type == "experiment_finished":
        return show_info_experiment_finished(screen, clock, duration, msg)

    elif info_type == "dynamic_targets":
        return show_info_dynamic_targets(screen, clock, duration, msg)

    else:
        print("Invalid info_type! Exiting...")
        # TODO


def show_phase_intro(screen, clock, duration, msg):
    flag = False
    start_time = pygame.time.get_ticks()

    while not flag:
        screen.fill(BG_COLOR)

        current_time = pygame.time.get_ticks()
        remaining_sec = update_timer(current_time, start_time, duration)[1]

        place_text_msg(screen, msg, FONT_SIZE_BIG, PURPLE, TXT_Y_INIT)

        msg_time = f"Wait until this phase begins: {remaining_sec:.1f} [s]"
        place_text_msg(
            screen, msg_time, FONT_SIZE_NORMAL, BLACK, TXT_Y_INIT + FONT_SIZE_BIG
        )

        if remaining_sec <= 0:
            flag = True
        pygame.display.flip()
        clock.tick(TICK_VALUE)

    return flag


def show_info_before_task(
    screen, clock, duration, current_task_id, total_tasks_num, employed_interfaces
):
    flag = False
    start_time = pygame.time.get_ticks()

    while not flag:

        screen.fill(BG_COLOR)
        place_overlay(screen, "top", alpha=100)
        draw_horizontal_line(screen)
        draw_vertical_line(screen)

        current_time = pygame.time.get_ticks()
        remaining_sec = update_timer(current_time, start_time, duration)[1]

        msg = f"Do not move until the task begins!"
        place_text_msg(screen, msg, FONT_SIZE_BIG, RED, 0)

        msg = "The active interfaces are illustrated below."
        place_text_msg(screen, msg, FONT_SIZE_NORMAL, BLACK, FONT_SIZE_BIG)

        msg = f"Remaining time: {remaining_sec:.1f} [s] to the task {current_task_id} out of {total_tasks_num}"
        place_text_msg(screen, msg, FONT_SIZE_SMALL, BLACK, FONT_SIZE_BIG * 2)

        dir, icon = None, None
        if employed_interfaces is not None:

            for left_msg, left_location in get_interfaces_icons_positions_for_info(
                employed_interfaces
            )[0]:
                if "Foot" in left_msg:
                    dir = DIR_ICN_LEFT_FOOT
                elif "Hand" in left_msg:
                    dir = DIR_ICN_LEFT_HAND
                location = (PX_WS_WIDTH // 2, left_location)
                icon = load_icon(dir, new_height=ICN_HEIGHT_SCALING)
                place_icon_on_screen(screen, icon, location + (0,))

            for right_msg, right_location in get_interfaces_icons_positions_for_info(
                employed_interfaces
            )[1]:
                if "Foot" in right_msg:
                    dir = DIR_ICN_RIGHT_FOOT
                elif "Hand" in right_msg:
                    dir = DIR_ICN_RIGHT_HAND
                location = ((3 / 2) * PX_WS_WIDTH, right_location)
                icon = load_icon(dir, new_height=ICN_HEIGHT_SCALING)
                place_icon_on_screen(screen, icon, location + (0,))

        left_entities = {"left_hand", "left_foot"}
        right_entities = {"right_hand", "right_foot"}
        entity_set = set(employed_interfaces)
        if left_entities.isdisjoint(entity_set):
            place_overlay(screen, location="left", alpha=125)
        if right_entities.isdisjoint(entity_set):
            place_overlay(screen, location="right", alpha=125)

        if remaining_sec <= 0:
            flag = True
        pygame.display.flip()
        clock.tick(TICK_VALUE)

    return flag


def show_info_after_task(screen, clock, duration, msg):
    flag = False
    start_time = pygame.time.get_ticks()

    while not flag:
        screen.fill(BG_COLOR)

        current_time = pygame.time.get_ticks()
        remaining_sec = update_timer(current_time, start_time, duration)[1]

        place_text_msg(screen, msg, FONT_SIZE_BIG, PURPLE, TXT_Y_INIT)

        msg_time = f"Remaining time: {remaining_sec:.1f} [s]"
        place_text_msg(
            screen, msg_time, FONT_SIZE_NORMAL, BLACK, TXT_Y_INIT + FONT_SIZE_BIG
        )

        if remaining_sec <= 0:
            flag = True
        pygame.display.flip()
        clock.tick(TICK_VALUE)

    return flag


def show_info_experiment_finished(screen, clock, duration, msg):
    flag = False
    start_time = pygame.time.get_ticks()

    while not flag:
        screen.fill(BG_COLOR)

        current_time = pygame.time.get_ticks()
        remaining_sec = update_timer(current_time, start_time, duration)[1]

        place_text_msg(screen, msg, FONT_SIZE_BIG, BLACK, TXT_Y_INIT)

        if remaining_sec <= 0:
            flag = True
        pygame.display.flip()
        clock.tick(TICK_VALUE)

    return flag


def upward_timer(screen, start_time, msg, color):
    current_time = pygame.time.get_ticks()
    elapsed_sec = update_timer(current_time, start_time, MAX_TASK_DURATION)[0]
    display_msg = msg
    place_text_msg(screen, display_msg, FONT_SIZE_NORMAL, color, 0)
    display_msg = f"Elapsed Time: {elapsed_sec:.1f} [s]"
    place_text_msg(screen, display_msg, FONT_SIZE_SMALL, color, FONT_SIZE_SMALL)
    return elapsed_sec


def reverse_timer(screen, start_time, total_time, msg, color):
    current_time = pygame.time.get_ticks()
    elapsed_ms = current_time - start_time
    elapsed_sec = elapsed_ms / 1000.0
    remaining_sec = max(0, total_time - elapsed_sec)
    display_msg = msg
    place_text_msg(screen, display_msg, FONT_SIZE_NORMAL, color, 0)
    display_msg = f"Remaining Time: {remaining_sec:.1f} [s]"
    place_text_msg(screen, display_msg, FONT_SIZE_SMALL, color, FONT_SIZE_SMALL)
    return remaining_sec, elapsed_sec


def show_info_dynamic_targets(screen, clock, duration, msg):
    flag = False
    start_time = pygame.time.get_ticks()

    while not flag:
        screen.fill(BG_COLOR)

        current_time = pygame.time.get_ticks()
        remaining_sec = update_timer(current_time, start_time, duration)[1]

        place_text_msg(screen, msg, FONT_SIZE_BIG, PURPLE, TXT_Y_INIT)

        msg_time = f"Please wait until this phase begins: {remaining_sec:.1f} [s]"
        place_text_msg(
            screen, msg_time, FONT_SIZE_NORMAL, BLACK, TXT_Y_INIT + FONT_SIZE_BIG
        )

        if remaining_sec <= 0:
            flag = True
        pygame.display.flip()
        clock.tick(TICK_VALUE)

    return flag
