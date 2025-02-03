import os
import pandas as pd
from config_loader import load_config

def read_csv(file_name):
    """
    Read a CSV file from the extracted folder defined in config.json.
    
    Args:
        file_name (str): Name of the CSV file to read.

    Returns:
        pd.DataFrame: The loaded CSV file as a pandas DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    # Load configuration
    config = load_config()
    extracted_to = config.get("extracted_to", "data/raw")  # Default fallback path if not found in config

    # Construct the full file path
    file_path = os.path.join(extracted_to, file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        print(f"Reading file: {file_path}")
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
