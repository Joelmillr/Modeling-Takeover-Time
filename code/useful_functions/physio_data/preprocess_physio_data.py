import pandas as pd
import neurokit2 as nk


def preprocess_physio_data(phsyiological_data_dictionary):
    """
    Preprocess physiological data by resampling and segmenting it based on markers.

    Args:
        phsyiological_data_dictionary (dict): A dictionary containing physiological data.

    Returns:
        dict: A dictionary containing preprocessed physiological data, segmented into baseline, training, and driving periods.
    """
    # storing the marker keys to be removed
    marker_keys = []

    # loop through each driver
    for driver in phsyiological_data_dictionary.keys():
        if driver.endswith("-markers"):
            continue

        # get driver data
        driver_data = phsyiological_data_dictionary[driver]
        markers = phsyiological_data_dictionary[driver + "-markers"]

        # convert to timedelta
        driver_data["min"] = pd.to_timedelta(driver_data["min"], unit="m")

        # Change min to Time
        driver_data = driver_data.rename(columns={"min": "Time"})

        # trim to the experiment
        driver_baseline_data = driver_data[
            (driver_data["Time"] >= pd.to_timedelta(markers["Time(sec.):"][0], unit="s"))
            & (driver_data["Time"] <= pd.to_timedelta(markers["Time(sec.):"][5], unit="s"))
        ]

        # Preprocessing the data with NeuroKit
        signals, _ = nk.bio_process(
            eda=driver_data["CH1"],
            ecg=driver_data["CH2"],
            rsp=driver_data["CH3"],
            sampling_rate=1000,
        )

        # Replace nan values with 0
        signals = signals.fillna(0)

        driver_data.drop(columns=["CH1", "CH2", "CH3"], inplace=True)

        # Convert time to timedelta and resample
        driver_data = driver_data.drop_duplicates(subset="Time")
        driver_data.set_index("Time", inplace=True)
        driver_data = driver_data.resample("1ms").asfreq()
        driver_data = driver_data.interpolate(method="nearest")
        driver_data = driver_data.ffill()
        driver_data = driver_data.reset_index()

        # Add the preprocessed data to the driver data
        driver_data = pd.concat([driver_data, signals], axis=1)

        # Drop unnecessary columns
        driver_data.drop(columns=["ECG_Raw", "RSP_Raw", "EDA_Raw"], inplace=True)

        # Baseline Data
        driver_baseline_data = driver_data[
            (driver_data["Time"] >= pd.to_timedelta(markers["Time(sec.):"][0], unit="s"))
            & (driver_data["Time"] <= pd.to_timedelta(markers["Time(sec.):"][1], unit="s"))
        ].copy()

        # Training Data
        driver_training_data = driver_data[
            (driver_data["Time"] >= pd.to_timedelta(markers["Time(sec.):"][2], unit="s"))
            & (driver_data["Time"] <= pd.to_timedelta(markers["Time(sec.):"][3], unit="s"))
        ].copy()

        # Driving Data
        driver_driving_data = driver_data[
            (driver_data["Time"] >= pd.to_timedelta(markers["Time(sec.):"][4], unit="s"))
            & (driver_data["Time"] <= pd.to_timedelta(markers["Time(sec.):"][5], unit="s"))
        ].copy()

        # replacing the dictionary value with segmented data
        phsyiological_data_dictionary[driver] = {
            "baseline": driver_baseline_data,
            "training": driver_training_data,
            "driving": driver_driving_data,
        }

        # storing the marker keys to be removed
        marker_keys.append(driver + "-markers")

    # Delete marker data
    for marker_key in marker_keys:
        del phsyiological_data_dictionary[marker_key]

    return phsyiological_data_dictionary
