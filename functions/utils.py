from pynput import keyboard
import numpy as np
import csv
from datetime import datetime
import os
import random


def update_timer(current_time, start_time, max_time):
    elapsed_sec = (current_time - start_time) / 1000.0
    remaining_sec = max(0, max_time - elapsed_sec)
    return elapsed_sec, remaining_sec


def add_tuples_2d(data1, data2):
    tmp = [0, 0]
    tmp[0] = data1[0] + data2[0]
    tmp[1] = data1[1] + data2[1]
    return tmp


def handle_exit(signum, frame):
    print("\n>> Execution stopped by user.")
    exit(0)


def arrays_equal(arr1, arr2):
    if arr1.shape != arr2.shape or arr1.dtype != arr2.dtype:
        return False
    return np.array_equal(arr1, arr2)


def get_next_position(axis, previous_array, speed, delta_t):
    new_array = previous_array
    if axis == 0:
        new_array[0] = previous_array[0] + speed * delta_t
        return new_array
    elif axis == 1:
        new_array[1] = previous_array[1] + speed * delta_t
        return new_array
    else:  # TODO
        pass


def get_axis(arr1, arr2):
    if arr1[0] != arr2[0]:
        return 0  # axis: x
    elif arr1[1] != arr2[1]:
        return 1  # axis: y
    else:
        return None


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def create_csv_file(path, file_name, data):
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, f"{file_name}.csv")
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)


def add_sequence_to_csv(subject_id, sequence_name, sequence_data):
    path = f"logs/S_{subject_id}/{sequence_name}/"
    ensure_dir(path)
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"sequence_{current_time}"
    create_csv_file(path, file_name, sequence_data)


def swap(lst):
    lst[0], lst[1] = lst[1], lst[0]


def swap_columns_in_row(lst_mat, row_index):
    lst_mat[row_index][0], lst_mat[row_index][1] = (
        lst_mat[row_index][1],
        lst_mat[row_index][0],
    )
    return lst_mat


def shuffle_tasks_with_pert(task_list):
    grouped_tasks = []
    i = 0
    while i < len(task_list):
        task = task_list[i]
        if i + 1 < len(task_list) and task_list[i + 1] == f"{task}_pert":
            grouped_tasks.append([task, task_list[i + 1]])
            i += 2
        else:
            grouped_tasks.append([task])
            i += 1

    random.shuffle(grouped_tasks)

    randomized_task_list = [t for group in grouped_tasks for t in group]

    return randomized_task_list
