import pandas as pd


# Create a dictionary of dataframes for each driver
def create_obstacle_trigger_times(driver_data):
    obstacles = [
        "TriggeredObs1",
        "TriggeredObs2",
        "TriggeredObs3",
        "TriggeredObs4",
        "TriggeredObs5",
    ]

    obstacle_trigger_times = {}

    for obstacle in obstacles:
        try:
            trigger = driver_data[driver_data["Obstacles"] == obstacle]["Time"].values[
                0
            ]

            dd = driver_data[driver_data["Time"] > trigger]
            takeover = dd[dd["Autonomous Mode (T/F)"] == False]["Time"].values[0]

            dd = dd[dd["Time"] > takeover]
            release = dd[dd["Autonomous Mode (T/F)"] == True]["Time"].values[0]

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
def create_takeover_timestamps(driving_data_dictionary):
    takeover_timestamps = pd.DataFrame()
    for key in driving_data_dictionary.keys():
        driving_data = driving_data_dictionary[key]
        timestamps = create_obstacle_trigger_times(driving_data)

        takeover_timestamps = pd.concat(
            [takeover_timestamps, pd.DataFrame(timestamps, index=[key])]
        )

    return takeover_timestamps
