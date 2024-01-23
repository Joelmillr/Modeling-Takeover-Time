import pandas as pd

def processing_driving_data(driving_data_dictionary, enc):
    """
    Function to process the driving data.

    Parameters:
        driving_data_dictionary (dict): Dictionary of driving data.
        enc (LabelEncoder): Label encoder.

    Returns:
        dict: Dictionary of processed driving data.
    """
    # Loop through driver dictionary
    for driver in driving_data_dictionary.keys():
        driver_data = driving_data_dictionary[driver]

        # Replace NaN values with "Nothing"
        driver_data = driver_data.fillna("Nothing")

        # label encoding
        driver_data["Obstacles"] = enc.transform(driver_data["Obstacles"])

        # resampling
        driver_data["Time"] = pd.to_timedelta(driver_data["Time"], unit="s")
        driver_data = driver_data.drop_duplicates(subset="Time")
        driver_data = driver_data.set_index("Time")
        driver_data = driver_data.resample("10ms").ffill()
        driver_data = driver_data.reset_index()

        # replacing the dictionary value
        driving_data_dictionary[driver] = driver_data

    return driving_data_dictionary
