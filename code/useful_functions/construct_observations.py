import pandas as pd
import neurokit2 as nk

def construct_observations(
    driving_data_dictionary,
    phsyiological_data_dictionary,
    driving_timestamps,
    physio_timestamps,
    driver_demographic_data,
):
    """
    Constructs observations for slow and fast takeovers based on driving and physiological data.

    Parameters:
    - driving_data_dictionary (dict): A dictionary containing driving data for each driver.
    - phsyiological_data_dictionary (dict): A dictionary containing physiological data for each driver.
    - driving_timestamps (pd.DataFrame): A DataFrame containing driving timestamps.
    - physio_timestamps (pd.DataFrame): A DataFrame containing physiological timestamps.
    - driver_demographic_data (pd.DataFrame): A DataFrame containing driver demographic data.

    Returns:
    - slow_observations (list): A list of numpy arrays representing slow takeover observations.
    - fast_observations (list): A list of numpy arrays representing fast takeover observations.
    """
    # initialize lists to store observations
    slow_observations = []
    fast_observations = []

    # loop through each driver
    for driver in driving_data_dictionary.keys():
        # data for each driver
        driver_driving_data = driving_data_dictionary[driver]
        driver_phyio_baseline_data = phsyiological_data_dictionary[driver]["baseline"]
        driver_physio_data = phsyiological_data_dictionary[driver]["driving"]

        # timestamps
        driver_driving_timestamps = driving_timestamps[driving_timestamps["subject_id"] == driver]
        driver_physio_timestamps = physio_timestamps[physio_timestamps["subject_id"] == driver]

        # loop through every takeover
        for column in driver_driving_timestamps.columns:
            if "TOT" in column:
                # get the obstacle number
                obstacle = column.replace("TOT", "")

                # store the obstacle triggers for driving and physio
                driving_obstacle_trigger = driver_driving_timestamps["Triggered" + obstacle].iloc[0]
                physio_obstacle_trigger = driver_physio_timestamps["Triggered" + obstacle].iloc[0]

                # check if the obstacle triggers are not null
                if pd.isnull(driving_obstacle_trigger) or pd.isnull(physio_obstacle_trigger):
                    continue

                # trim the data to the 10s before the takeover
                driving_data_10_sec = driver_driving_data[
                    (
                        driver_driving_data["Time"]
                        >= driving_obstacle_trigger - pd.to_timedelta("10s")
                    )
                    & (driver_driving_data["Time"] < driving_obstacle_trigger)
                ].copy()

                physio_data_10_sec = driver_physio_data[
                    (
                        driver_physio_data["Time"]
                        >= (
                            driver_physio_data.Time.min()
                            + physio_obstacle_trigger
                            - pd.to_timedelta("10s")
                        )
                    )
                    & (
                        driver_physio_data["Time"]
                        < driver_physio_data.Time.min() + physio_obstacle_trigger
                    )
                ].copy()

                '''
                # get the hrv for the 10s before the takeover
                takeover_hrv = nk.hrv_time(physio_data_10_sec, sampling_rate=100)
                takeover_hrv = takeover_hrv.drop(
                    columns=[
                        "HRV_SDANN1",
                        "HRV_SDNNI1",
                        "HRV_SDANN2",
                        "HRV_SDNNI1",
                        "HRV_SDNNI2",
                        "HRV_SDANN5",
                        "HRV_SDNNI5",
                        "HRV_MedianNN",
                        "HRV_MadNN",
                        "HRV_MCVNN",
                        "HRV_IQRNN",
                        "HRV_SDRMSSD",
                        "HRV_Prc20NN",
                        "HRV_Prc80NN",
                        "HRV_pNN50",
                        "HRV_pNN20",
                        "HRV_MinNN",
                        "HRV_MaxNN",
                        "HRV_HTI",
                        "HRV_TINN",
                        "HRV_MeanNN",
                        "HRV_SDNN",
                        "HRV_RMSSD",
                        "HRV_SDSD",
                        "HRV_CVNN",
                        "HRV_CVSD",
                        "HRV_MedianNN",
                        "HRV_MadNN",
                        "HRV_MCVNN",
                        "HRV_IQRNN",
                        "HRV_SDRMSSD",
                        "HRV_Prc20NN",
                        "HRV_Prc80NN",
                        "HRV_pNN50",
                        "HRV_pNN20",
                        "HRV_MinNN",
                        "HRV_MaxNN",
                        "HRV_HTI",
                        "HRV_TINN",
                        "HRV_MeanNN",
                        "HRV_SDNN",
                        "HRV_RMSSD",
                        "HRV_SDSD",
                        "HRV_CVNN",
                        "HRV_CVSD",
                        "HRV_MedianNN",
                        "HRV_MadNN",
                        "HRV_MCVNN",
                        "HRV_IQRNN",
                        "HRV_SDRMSSD",
                        "HRV_Prc20NN",
                        "HRV_Prc80NN",
                        "HRV_pNN50",
                        "HRV_pNN20",
                        "HRV_MinNN",
                        "HRV_MaxNN",
                        "HRV_HTI",
                        "HRV_TINN",
                    ]
                )
                '''

                # # Store the Difference between the baseline and the takeover
                # hrv_difference = takeover_hrv - baseline_hrv

                # # rename the columns
                # hrv_difference.columns = [
                #     "HRV_" + column + "_Difference" for column in hrv_difference.columns
                # ]

                # # concatenate the dataframes
                # hrv = pd.concat([baseline_hrv, takeover_hrv, hrv_difference], axis=1)

                # reset the Time index
                driving_data_10_sec = driving_data_10_sec.set_index("Time")
                physio_data_10_sec = physio_data_10_sec.set_index("Time")

                # set the index to 0
                driving_data_10_sec.index = (
                    driving_data_10_sec.index - driving_data_10_sec.index.min()
                )
                physio_data_10_sec.index = physio_data_10_sec.index - physio_data_10_sec.index.min()

                # merge the data
                driver_data = pd.merge(
                    driving_data_10_sec,
                    physio_data_10_sec,
                    left_index=True,
                    right_index=True,
                )

                # reset the index
                driver_data.reset_index(inplace=True)

                # Remove Time, Position X, Position Y, Position Z, Autonomous Mode (T/F), Obstacles
                driver_data = driver_data.drop(
                    columns=[
                        "Time",
                        "Autonomous Mode (T/F)",
                        "Obstacles",
                    ]
                )

                # grab driver demogrpahic data
                demo_data = driver_demographic_data[driver_demographic_data["code"] == driver]

                # Broadcast to repeat the static data for each row of the dynamic data
                demo_data = pd.concat([demo_data] * len(driver_data), ignore_index=True)

                # Broadcast the hrv data
                # hrv = pd.concat([hrv] * len(driver_data), ignore_index=True)

                # merge the data
                driver_data = pd.merge(driver_data, demo_data, left_index=True, right_index=True)
                # driver_data = pd.merge(driver_data, hrv, left_index=True, right_index=True)

                # change the code value to the driver id
                driver_data["code"] = driver_data["code"].apply(lambda x: x.split("T")[1])
                # cast code to int
                driver_data["code"] = driver_data["code"].astype(int)

                if len(driver_data) != 1000:
                    continue

                # determine if the takeover was slow or fast
                if driver_driving_timestamps[column].iloc[0] > pd.to_timedelta("3s"):
                    slow_observations.append(driver_data.to_numpy())
                else:
                    fast_observations.append(driver_data.to_numpy())

    return slow_observations, fast_observations, driver_data.columns
