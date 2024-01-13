import os
import pandas as pd

# Creates a dictionary of driving data files
## dictionary key: driving data file name
## dictionary value: driving data file

# Input: folder containing driving data files
# Output: dictionary of driving data files


def create_dd_dictionary(driving_data_folder):
    driving_data = {}

    for filename in os.listdir(driving_data_folder):
        file_path = os.path.join(driving_data_folder, filename)
        driving_data[filename.replace(".txt", "")] = pd.read_csv(
            file_path,
            usecols={
                "Time",
                "VehicleSpeed",
                "SteeringWheelAngle",
                "Autonomous Mode (T/F)",
                "Obstacles",
            },
            dtype={"Obstacles": str},
        )
    return driving_data
