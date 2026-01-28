import sys, os 
import csv
import copy
import itertools
import numpy as np 
import random

def save_data_array_to_csv(data_array, path, filename):
    # Ensure directory exists
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)

    # Define column order
    fieldnames = ["id", "left_hand", "right_hand", "left_foot", "right_foot"]

    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for entry in data_array:
            row = {"id": entry["id"]}
            for limb in ["left_hand", "right_hand", "left_foot", "right_foot"]:
                pose = entry[limb]["target_pose"]
                if pose is None:
                    row[limb] = None
                else:
                    # Convert numpy array to string (e.g. [10 20 0])
                    row[limb] = pose.tolist() if hasattr(pose, "tolist") else str(pose)
            writer.writerow(row)

    print(f">> Saved {len(data_array)} rows to {filepath}")
