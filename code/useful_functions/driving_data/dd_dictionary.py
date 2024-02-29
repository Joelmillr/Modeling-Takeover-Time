import os
import pandas as pd

def create_dd_dictionary(driving_data_folder, participants_to_exclude=[]):
    """
    Creates a dictionary of driving data files.

    Args:
        driving_data_folder (str): Folder containing driving data files.
        participants_to_exclude (list, optional): List of participants to exclude. Defaults to [].

    Returns:
        dict: Dictionary of driving data files.
    """
    # Create dictionary
    driving_data = {}

    # Loop through files
    for filename in os.listdir(driving_data_folder):
        if filename.replace(".txt", "") in participants_to_exclude:
            continue

        # Read and Store file
        file_path = os.path.join(driving_data_folder, filename)

        driver_data = pd.read_csv(
            file_path,
            dtype={"Obstacles": str},
        )

        driver_data = driver_data.drop(
            columns=[
                "AcceleratorPedalPos",
                "DeceleratorPedalPos",
                "EngineSpeed",
                "GearPosActual",
                "GearPosTarget",
                " Position X",
                "Position Y",
                "Position Z",
            ]
        )

        # Add to dictionary
        driving_data[filename.replace(".txt", "")] = driver_data

    return driving_data
