import pandas as pd



def process_physio_data(phsyiological_data_dictionary):
    """
    Process physiological data by resampling and segmenting it based on markers.

    Args:
        phsyiological_data_dictionary (dict): A dictionary containing physiological data.

    Returns:
        dict: A dictionary containing processed physiological data, segmented into baseline, training, and driving periods.
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

        # converting the time to timedelta
        driver_data["min"] = pd.to_timedelta(driver_data["min"], unit="min")

        # resampling
        driver_data = driver_data.set_index("min")
        driver_data = driver_data.resample("10ms").ffill()
        driver_data = driver_data.reset_index()

        # Change min to Time
        driver_data = driver_data.rename(columns={"min": "Time"})

        # Baseline Data
        baseline_start = pd.to_timedelta(markers["Time(sec.):"][0], unit="s")
        baseline_end = pd.to_timedelta(markers["Time(sec.):"][1], unit="s")
        driver_baseline_data = driver_data[
            (driver_data["Time"] >= baseline_start) & (driver_data["Time"] <= baseline_end)
        ].copy()

        # Training Data
        training_start = pd.to_timedelta(markers["Time(sec.):"][2], unit="s")
        training_end = pd.to_timedelta(markers["Time(sec.):"][3], unit="s")
        driver_training_data = driver_data[
            (driver_data["Time"] >= training_start) & (driver_data["Time"] <= training_end)
        ].copy()

        # Driving Data
        driving_start = pd.to_timedelta(markers["Time(sec.):"][4], unit="s")
        driving_end = pd.to_timedelta(markers["Time(sec.):"][5], unit="s")
        driver_driving_data = driver_data[
            (driver_data["Time"] >= driving_start) & (driver_data["Time"] <= driving_end)
        ].copy()

        # # Adding an 'Obstacles' column
        # ----------------------------------
        # driver_driving_data["Obstacles"] = "Nothing"

        # # Match the timestamps with the obstacles
        # driver_physio_timestamps = physio_timestamps[
        #     physio_timestamps["subject_id"] == driver
        # ]

        # obstacles = driver_physio_timestamps.columns
        # obstacles = obstacles[2:]
        # obstacles = obstacles[:-1]

        # Add an obstacle column to the driving data
        # driver_driving_data["Obstacles"] = "Nothing"
        # for obstacle in obstacles:
        #     # Time when the obstacle appears
        #     obstacle_appears = (
        #         driving_start
        #         + pd.to_timedelta(driver_physio_timestamps[obstacle], unit="s").to_list()[0]
        #     )

        #     # Add this marker to the Obstacles column
        #     if not pd.isna(obstacle_appears):
        #         mask = driver_driving_data["Time"] >= obstacle_appears
        #         first_index = mask.idxmax()
        #         driver_driving_data.at[first_index, "Obstacles"] = obstacle
        # ----------------------------------

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
