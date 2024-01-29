import pandas as pd

def process_physio_timestamps(physio_timestamps, participants_to_exclude):
    """
    Process physio timestamps by matching the data to the driving data, removing excluded participants,
    adding 0 to subject ids, transforming columns to timedelta, adding takeover times, and dropping label_st column.

    Args:
        physio_timestamps (DataFrame): DataFrame of physio timestamps.
        participants_to_exclude (list): List of participants to exclude.

    Returns:
        DataFrame: Processed physio timestamps DataFrame.
    """
    
    # Match the physio data to the driving data
    for col in physio_timestamps.columns:
        if "Trig" in col:
            physio_timestamps = physio_timestamps.rename(
                columns={col: col.replace("Trig", "Triggered")}
            )

        if "Det" in col:
            physio_timestamps = physio_timestamps.drop(columns=col)

        if "Rep" in col:
            physio_timestamps = physio_timestamps.rename(
                columns={col: col.replace("Rep", "Takeover")}
            )

    # Remove the participants that are not in the driving data
    physio_timestamps = physio_timestamps[
        ~physio_timestamps["subject_id"].isin(participants_to_exclude)
    ]

    # Add 0 to the subject ids to match the format of the driving data
    physio_timestamps["subject_id"] = physio_timestamps["subject_id"].apply(
        lambda x: x.split("T")[0] + "T" + x.split("T")[1].zfill(2)
    )

    # transform the every column to a timedelta
    for timestamp in physio_timestamps.columns:
        if timestamp != "subject_id" and timestamp != "label_st":
            # Check value is not NaT
            physio_timestamps[timestamp] = physio_timestamps[timestamp].apply(
                lambda x: pd.to_timedelta(x, unit="s") if pd.notnull(x) else x
            )

    # Adding the takeover times to the timestamp data
    trigger = "TriggeredObs"
    respond = "TakeoverObs"
    obstacles = ["Deer", "Cone", "Frog", "Can", "FA1", "FA2"]

    # Add TOT
    for obstacle in obstacles:
        physio_timestamps["TOT" + "Obs" + obstacle] = (
            physio_timestamps[respond + obstacle] - physio_timestamps[trigger + obstacle]
        )

    # rename columns to match the driving data
    for col in physio_timestamps.columns:
        for i, obstacle in enumerate(obstacles):
            if obstacle in col:
                physio_timestamps = physio_timestamps.rename(
                    columns={col: col.replace(obstacle, str(i + 1))}
                )

    # drop label_st
    physio_timestamps = physio_timestamps.drop(columns="label_st")

    return physio_timestamps
