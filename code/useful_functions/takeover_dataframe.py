import pandas as pd


# Create a dictionary of dataframes for each driver
# Note: **Consider Checking if the obstacle was detected**
def create_obstacle_trigger_times(driver_data, enc):
    obstacle_trigger_times = {}

    # remove Detected and Nothing
    obstacles = enc.classes_[(enc.classes_ != "Detected") & (enc.classes_ != "Nothing")]

    for obstacle in obstacles:
        try:
            # Find what time the obstacle was triggered
            trigger = driver_data[
                driver_data["Obstacles"] == enc.transform([obstacle])[0]
            ]["Time"].values[0]

            # Consider only data after the trigger
            data_after_trigger = driver_data[driver_data["Time"] > trigger]

            # Find the remaining obstacles
            remaining_obstacles = data_after_trigger["Obstacles"].unique()
            remaining_obstacles = enc.inverse_transform(remaining_obstacles)
            remaining_obstacles = remaining_obstacles[1:]
            remaining_obstacles = remaining_obstacles[
                (remaining_obstacles != "Detected") & (remaining_obstacles != "Nothing")
            ]

            # Find time of the takeover
            takeover = data_after_trigger[
                data_after_trigger["Autonomous Mode (T/F)"] == False
            ]["Time"].values[0]

            # Check if the driver took over before the next obstacle was triggered
            if len(remaining_obstacles) > 0:
                next_obstacle = remaining_obstacles[0]
                next_obstacle_trigger = data_after_trigger[
                    data_after_trigger["Obstacles"] == enc.transform([next_obstacle])[0]
                ]["Time"].values[0]

                if takeover > next_obstacle_trigger:
                    # print("Takeover after the next obstacle was triggered")
                    continue

            # Time when manual control was released
            data_after_takeover = driver_data[driver_data["Time"] > takeover]
            release = data_after_takeover[
                data_after_takeover["Autonomous Mode (T/F)"] == True
            ]["Time"].values[0]

        except IndexError:
            continue
        except KeyError:
            continue

        obstacle_trigger_times[obstacle] = trigger
        obstacle_trigger_times[obstacle.replace("Triggered", "Takeover")] = takeover
        obstacle_trigger_times[obstacle.replace("Triggered", "Release")] = release
        obstacle_trigger_times[obstacle.replace("Triggered", "TOT")] = (
            takeover - trigger
        )

    return obstacle_trigger_times


# Create a dataframes of takeover times for each driver
# The index is the driver ID
def create_takeover_timestamps(driving_data_dictionary, enc):
    takeover_timestamps = pd.DataFrame()

    for key in driving_data_dictionary.keys():
        driving_data = driving_data_dictionary[key]
        timestamps = create_obstacle_trigger_times(driving_data, enc)

        takeover_timestamps = pd.concat(
            [takeover_timestamps, pd.DataFrame(timestamps, index=[key])]
        )

    # Sort the columns by Particpant ID
    takeover_timestamps["sort_key"] = takeover_timestamps.index.to_series().apply(
        lambda x: int(x.split("ST")[-1]) if "ST" in x else int(x.split("NST")[-1])
    )
    takeover_timestamps = takeover_timestamps.sort_values("sort_key")
    takeover_timestamps = takeover_timestamps.drop("sort_key", axis=1)

    return takeover_timestamps
