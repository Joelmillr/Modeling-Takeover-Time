import os
import pandas as pd

# Creates a dictionary of driving data files
## dictionary key: driving data file name
## dictionary value: driving data file

# Input: folder containing driving data files
# Output: dictionary of driving data files


def create_dd_dictionary(driving_data_folder, participants_to_exclude=[]):
    driving_data = {}

    for filename in os.listdir(driving_data_folder):
        # exclude participants
        if filename.replace(".txt", "") in participants_to_exclude:
            continue

        # read file
        file_path = os.path.join(driving_data_folder, filename)
        
        driver_data = pd.read_csv(
            file_path,
            dtype={"Obstacles": str},
        )

        # fill NaN values with "Nothing"
        driver_data = driver_data.fillna("Nothing")

        # Remove uneeded columns
        driver_data = driver_data.drop(
            columns=[
                "AcceleratorPedalPos",
                "DeceleratorPedalPos",
                "EngineSpeed",
                "GearPosActual",
                "GearPosTarget",
            ]
        )

        # add to dictionary
        driving_data[filename.replace(".txt", "")] = driver_data

    return driving_data
