import os
import pandas as pd

# Creates a dictionary of physiological data files, including markers
## dictionary key: physiological data file name
## dictionary value: physiological data or markers file

# Input: folder containing physiological data files
# Output: dictionary of physiological data files


def create_pd_dictionary(physio_data_folder, participants_to_exclude=[]):
    phsyiological_data = {}

    for filename in os.listdir(physio_data_folder):
        file_path = os.path.join(physio_data_folder, filename)

        # exclude participants
        if (
            filename.replace(".txt", "") in participants_to_exclude
            or filename.replace("-markers.txt", "") in participants_to_exclude
        ):
            continue

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
