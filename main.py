# defined modules
from defs_parameters import *
from functions.funcs_pygame import *
from functions.funcs_phase_management import *
from functions.utils import *
from functions.funcs_static_task_management import *

import time

# create logs directory if it does not exist
# all information is saved under this dir
ensure_dir("logs")

sys.path.append(os.path.join(os.path.dirname(__file__), "simplified_targets"))

# loading data (target pose etc.) for each phase of the tasks
from simplified_targets.training import *
from simplified_targets.baseline import *
from simplified_targets.task_1_1 import *
from simplified_targets.task_1_2 import *
from simplified_targets.task_1_3 import *
from simplified_targets.task_2_1 import *
from simplified_targets.task_2_2 import *
from simplified_targets.task_2_3 import *
from simplified_targets.task_3_1 import *
from simplified_targets.task_3_2 import *
from simplified_targets.task_3_3 import *
from simplified_targets.task_3_4 import *
from simplified_targets.task_3_5 import *

# receiving/parsing data from the motion capture system
from motive.parse_received_packets import *

# load experiment related info
from exp_config import *
import pygame
import threading

screen = None


def task_manager(screen, clock, state, msg, data_task, limbs_to_perturb, n):
    counter = 1
    for item in data_task:
        targets = limbs_to_perturb if limbs_to_perturb else [[]]
        for limbs in targets:
            print(f"limb: {limbs}")
            for i in range(n):
                print(
                    f"({msg}) repetition {i+1} of task {counter}, total tasks: {len(data_task)}"
                )
                run_task(screen, clock, item, SUBJECT_ID, state, msg, limbs)
        counter = counter + 1


if __name__ == "__main__":

    listener = keyboard.Listener(on_press=on_press2)
    listener.start()

    # read motion capture system
    thrd_udp_hand = threading.Thread(target=udp_hands, daemon=True)
    thrd_udp_hand.start()

    thrd_udp_feet = threading.Thread(target=udp_feet, daemon=True)
    thrd_udp_feet.start()

    # --- Monitor setup ---
    monitor_width = 2560
    monitor_height = 1440
    num_monitors = 3
    target_monitor = 2  # 1, 2, or 3
    x = (target_monitor - 1) * monitor_width + (monitor_width - SCREEN_WIDTH) // 2 + 800
    y = (monitor_height - SCREEN_HEIGHT) // 2 - 100

    # pygame
    pygame.init()
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pilot Study of the Four-Handed Manipulation Project")
    clock = pygame.time.Clock()

    # main loop (state machine)
    running = True

    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            msg = None

            for state in SCRIPT_SEQUENCE:

                if state == "training":
                    msg = "Training (One Side)"
                    print(f"++ {msg}")
                    show_information(
                        screen, clock, "phase", DURATION_PHASE_INTRO, msg=msg
                    )
                    task_manager(screen, clock, state, msg, data_training, [], 2)

                # elif state == "baseline":
                #     msg = "Baseline (One Side)"
                #     print(f"++ {msg}")
                #     show_information(screen, clock, "phase", DURATION_PHASE_INTRO, msg=msg)
                #     task_manager(screen, clock, state, msg, data_baseline, [], 2)

                elif state == "task1":
                    msg = "Task 1 - Main Limbs: Hands"
                    show_information(
                        screen, clock, "phase", DURATION_PHASE_INTRO, msg=msg
                    )
                    #
                    #  task_list_1 = ["task_1_1", "task_1_1_pert"]
                    # task_list_2 = ["task_1_2", "task_1_3", "task_1_4"]
                    # random.shuffle(task_list_2)
                    # print(task_list_1, task_list_2)
                    # # task_list = shuffle_tasks_with_pert(task_list)
                    # task_list = task_list_1 + task_list_2
                    task_list = ["task_1_1"]
                    add_sequence_to_csv(
                        SUBJECT_ID, "experiment_sequence/tasks/task1/general", task_list
                    )
                    tmp_limbs_to_perturb = ["left_hand", "right_hand"]
                    random.shuffle(tmp_limbs_to_perturb)
                    add_sequence_to_csv(
                        SUBJECT_ID,
                        "experiment_sequence/tasks/task1/perturbed_ones/task_1_1_pert",
                        tmp_limbs_to_perturb,
                    )

                    for selected_task in task_list:
                        match selected_task:
                            case "task_1_1":
                                msg = "task_1_1"
                                data_task = data_task_1_1
                                limbs_to_perturb = []

                            case "task_1_1_pert":
                                msg = "task_1_1_perturbed"
                                data_task = data_task_1_1
                                limbs_to_perturb = tmp_limbs_to_perturb

                            case "task_1_2":
                                msg = "task_1_2"
                                data_task = data_task_1_2
                                limbs_to_perturb = []

                            case "task_1_3":
                                msg = "task_1_3"
                                data_task = data_task_1_3
                                limbs_to_perturb = []

                            case "task_1_4":
                                msg = "task_1_4"
                                data_task = data_task_3_5
                                limbs_to_perturb = []

                            case _:
                                pass

                        task_manager(
                            screen, clock, state, msg, data_task, limbs_to_perturb, N
                        )

                elif state == "task2":
                    msg = "Task 2 - Main Limbs: Feet"
                    show_information(
                        screen, clock, "phase", DURATION_PHASE_INTRO, msg=msg
                    )

                    # task_list_1 = ["task_2_1", "task_2_1_pert"]
                    # task_list_2 = ["task_2_2", "task_2_3", "task_2_4"]
                    # random.shuffle(task_list_2)
                    # # task_list = shuffle_tasks_with_pert(task_list)
                    # print(task_list_1, task_list_2)
                    # task_list = task_list_1 + task_list_2
                    task_list = ["task_2_1"]
                    add_sequence_to_csv(
                        SUBJECT_ID, "experiment_sequence/tasks/task2/general", task_list
                    )

                    tmp_limbs_to_perturb = ["left_foot", "right_foot"]
                    random.shuffle(tmp_limbs_to_perturb)
                    add_sequence_to_csv(
                        SUBJECT_ID,
                        "experiment_sequence/tasks/task2/perturbed_ones/task_2_1_pert",
                        tmp_limbs_to_perturb,
                    )

                    for selected_task in task_list:
                        match selected_task:
                            case "task_2_1":
                                msg = "task_2_1"
                                data_task = data_task_2_1
                                limbs_to_perturb = []

                            case "task_2_1_pert":
                                msg = "task_2_1_perturbed"
                                data_task = data_task_2_1
                                limbs_to_perturb = tmp_limbs_to_perturb

                            case "task_2_2":
                                msg = "task_2_2"
                                data_task = data_task_2_2
                                limbs_to_perturb = []

                            case "task_2_3":
                                msg = "task_2_3"
                                data_task = data_task_2_3
                                limbs_to_perturb = []

                            case "task_2_4":
                                msg = "task_2_4"
                                data_task = data_task_3_5
                                limbs_to_perturb = []

                            case _:
                                pass

                        task_manager(
                            screen, clock, state, msg, data_task, limbs_to_perturb, N
                        )

                elif state == "task3":
                    msg = "Baseline (One Side)"
                    print(f"++ {msg}")
                    show_information(
                        screen, clock, "phase", DURATION_PHASE_INTRO, msg=msg
                    )
                    task_manager(screen, clock, state, msg, data_baseline, [], N)

                    msg = "Task 3 - Main Limbs: Hand/Foot"
                    show_information(
                        screen, clock, "phase", DURATION_PHASE_INTRO, msg=msg
                    )

                    task_list = [
                        "task_3_1",
                        "task_3_1_pert",
                        "task_3_2",
                        "task_3_2_pert",
                        "task_3_3",
                        "task_3_3_pert",
                        "task_3_4",
                        "task_3_4_pert",
                    ]

                    task_list = shuffle_tasks_with_pert(task_list)
                    add_sequence_to_csv(
                        SUBJECT_ID, "experiment_sequence/tasks/task3/general", task_list
                    )

                    tmp_limbs_to_perturb_3_1 = ["left_hand", "left_foot"]
                    random.shuffle(tmp_limbs_to_perturb_3_1)
                    add_sequence_to_csv(
                        SUBJECT_ID,
                        "experiment_sequence/tasks/task3/perturbed_ones/task_3_1_pert",
                        tmp_limbs_to_perturb_3_1,
                    )

                    tmp_limbs_to_perturb_3_2 = ["left_hand", "right_foot"]
                    random.shuffle(tmp_limbs_to_perturb_3_2)
                    add_sequence_to_csv(
                        SUBJECT_ID,
                        "experiment_sequence/tasks/task3/perturbed_ones/task_3_2_pert",
                        tmp_limbs_to_perturb_3_2,
                    )

                    tmp_limbs_to_perturb_3_3 = ["right_hand", "left_foot"]
                    random.shuffle(tmp_limbs_to_perturb_3_3)
                    add_sequence_to_csv(
                        SUBJECT_ID,
                        "experiment_sequence/tasks/task3/perturbed_ones/task_3_3_pert",
                        tmp_limbs_to_perturb_3_3,
                    )

                    tmp_limbs_to_perturb_3_4 = ["right_hand", "right_foot"]
                    random.shuffle(tmp_limbs_to_perturb_3_4)
                    add_sequence_to_csv(
                        SUBJECT_ID,
                        "experiment_sequence/tasks/task3/perturbed_ones/task_3_4_pert",
                        tmp_limbs_to_perturb_3_4,
                    )

                    for selected_task in task_list:
                        match selected_task:
                            case "task_3_1":
                                msg = "task_3_1"
                                data_task = data_task_3_1
                                limbs_to_perturb = []

                            case "task_3_1_pert":
                                msg = "task_3_1_perturbed"
                                data_task = data_task_3_1
                                limbs_to_perturb = tmp_limbs_to_perturb_3_1

                            case "task_3_2":
                                msg = "task_3_2"
                                data_task = data_task_3_2
                                limbs_to_perturb = []

                            case "task_3_2_pert":
                                msg = "task_3_2_perturbed"
                                data_task = data_task_3_2
                                limbs_to_perturb = tmp_limbs_to_perturb_3_2

                            case "task_3_3":
                                msg = "task_3_3"
                                data_task = data_task_3_3
                                limbs_to_perturb = []

                            case "task_3_3_pert":
                                msg = "task_3_3_perturbed"
                                data_task = data_task_3_3
                                limbs_to_perturb = tmp_limbs_to_perturb_3_3

                            case "task_3_4":
                                msg = "task_3_4"
                                data_task = data_task_3_4
                                limbs_to_perturb = []

                            case "task_3_4_pert":
                                msg = "task_3_4_perturbed"
                                data_task = data_task_3_4
                                limbs_to_perturb = tmp_limbs_to_perturb_3_4

                            case "task_3_5":
                                msg = "task_3_5"
                                data_task = data_task_3_5
                                limbs_to_perturb = []

                            case _:
                                pass

                        task_manager(
                            screen, clock, state, msg, data_task, limbs_to_perturb, N
                        )

                elif state == "done":
                    running = False
                    msg = "Thanks for your participation"
                    show_information(screen, clock, "experiment_finished", 5, msg=msg)

                else:
                    pass  # TODO

        except KeyboardInterrupt:
            handle_exit(None, None)

    pygame.quit()
