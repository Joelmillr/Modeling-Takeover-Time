import os
import pandas as pd

def create_pd_dictionary(physio_data_folder, participants_to_exclude=[]):
    """
    Creates a dictionary of physiological data files, including markers.

    Args:
        physio_data_folder (str): The folder containing physiological data files.
        participants_to_exclude (list, optional): List of participants to exclude. Defaults to [].

    Returns:
        dict: Dictionary of physiological data files.
            Dictionary key: physiological data file name.
            Dictionary value: physiological data or markers file.
    """
    phsyiological_data = {}

    for filename in os.listdir(physio_data_folder):
        # exclude participants
        if (
            filename.replace(".txt", "") in participants_to_exclude
            or filename.replace("-markers.txt", "") in participants_to_exclude
        ):
            continue

        file_path = os.path.join(physio_data_folder, filename)

        # read file
        if "-markers" in filename:
            phsyiological_data[filename.replace(".txt", "")] = pd.read_csv(
                file_path, header=2, sep="\t"
            )

        else:
            driver_data = pd.read_csv(
                file_path,
                sep="\t",
                header=9,
                skiprows=[10],
                usecols=[0, 1, 2, 3],
            )

            # Convert time to timedelta
            driver_data["min"] = pd.to_timedelta(driver_data["min"], unit="m")
            driver_data.set_index("min", inplace=True)
            driver_data = driver_data.resample("10ms").mean()
            driver_data = driver_data.interpolate(method="linear")
            driver_data = driver_data.reset_index()

            phsyiological_data[filename.replace(".txt", "")] = driver_data

    return phsyiological_data
