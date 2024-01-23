

def process_driver_demographic_data(driver_demographic_data, participants_to_exclude):
    """
    Process the driver demographic data.

    Args:
        driver_demographic_data (DataFrame): The driver demographic data to be processed.
        participants_to_exclude (list): List of participants to exclude from the data.

    Returns:
        DataFrame: The processed driver demographic data.
    """
    # Remove the participants that are not in the driving data
    driver_demographic_data = driver_demographic_data[
        ~driver_demographic_data["code"].isin(participants_to_exclude)
    ].copy()

    # Reformat code
    driver_demographic_data["code"] = driver_demographic_data["code"].apply(
        lambda x: x.split("T")[0] + "T" + x.split("T")[1].zfill(2)
    )

    # Convert from year to number of years
    driver_demographic_data["driving_license"] = (
        2018 - driver_demographic_data["driving_license"]
    )

    # Normalize the age and km_year?

    # Add a condition column if code contains NST
    driver_demographic_data["condition"] = driver_demographic_data["code"].apply(
        lambda x: "NST" in x
    )

    return driver_demographic_data
