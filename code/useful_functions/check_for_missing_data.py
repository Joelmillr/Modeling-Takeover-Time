import os


def check_for_missing_data(driving_data_folder, physio_data_folder):
    """
    Check for missing data files between the Driving folder and Physio folder.

    Args:
        driving_data_folder (str): Path to the Driving folder.
        physio_data_folder (str): Path to the Physio folder.

    Returns:
        list: A list of missing file names (without the '.txt' extension).
    """
    # Read every file in the Driving folder
    driving_files = [
        file for file in os.listdir(driving_data_folder) if file.endswith(".txt")
    ]

    # Read ever file in the Physio folder that is not a -markers file
    physio_files = [
        file
        for file in os.listdir(physio_data_folder)
        if file.endswith(".txt") and not file.endswith("-markers.txt")
    ]

    missing_files = []
    # Print any file that is in the Physio folder but not in the Driving folder or vice versa
    for file in physio_files:
        if file not in driving_files:
            missing_files.append(file.replace(".txt", ""))

    for file in driving_files:
        if file not in physio_files:
            missing_files.append(file.replace(".txt", ""))

    return missing_files
