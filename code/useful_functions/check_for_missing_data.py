import os


def check_for_missing_data(driving_data_folder, physio_data_folder):
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
            missing_files.append(file)

    for file in driving_files:
        if file not in physio_files:
            missing_files.append(file)

    return missing_files
