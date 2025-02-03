import os
import pandas as pd
from config_loader import load_config

def load_csv_to_df(file_name, folder_path=None):
    """
    Load a CSV file from the given directory or default extracted folder in config.json.

    Args:
        file_name (str): Name of the CSV file to read.
        folder_path (str, optional): Custom directory path to read from.
                                     Defaults to 'extracted_to' in config.json.

    Returns:
        pd.DataFrame: The loaded CSV file as a pandas DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    # Load configuration
    config = load_config()
    default_folder = config.get("extracted_to", "data/raw")  # Default path if not specified in config

    # Use the provided folder path if given, otherwise use default from config
    directory = folder_path if folder_path else default_folder

    # Construct the full file path
    file_path = os.path.join(directory, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        print(f"Loading file: {file_path}")
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
    