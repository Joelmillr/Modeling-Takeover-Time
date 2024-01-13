import os
import pandas as pd

# Creates a dictionary of physiological data files, including markers
## dictionary key: physiological data file name
## dictionary value: physiological data or markers file

# Input: folder containing physiological data files
# Output: dictionary of physiological data files


def create_pd_dictionary(physio_data_folder):
    phsyiological_data = {}

    for filename in os.listdir(physio_data_folder):
        file_path = os.path.join(physio_data_folder, filename)

        if "-markers" in filename:
            phsyiological_data[filename] = pd.read_csv(file_path, header=2, sep="\t")

        else:
            participant_data = pd.read_csv(file_path, sep="\t", header=9)
            participant_data = participant_data.iloc[1:]
            participant_data = participant_data.iloc[:, :-1]
            phsyiological_data[filename] = participant_data

    return phsyiological_data
