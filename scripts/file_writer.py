import os
import pandas as pd
from config_loader import load_config  # Import config loader

def write_df_to_csv(df, file_name):
    """
    Save a cleaned DataFrame as a CSV file in the clean directory from config.json,
    appending a suffix defined in the configuration.

    Args:
        df (pd.DataFrame): The cleaned DataFrame to save.
        file_name (str): Name of the original CSV file.

    Returns:
        str: Full path of the saved file.
    """
    # Load configuration
    config = load_config()
    processed_to = config.get("processed_to", "data/clean")  # Default directory
    suffix = config.get("file_suffix", "_clean")  # Get suffix from config, default to "_clean"

    # Ensure the clean directory exists
    os.makedirs(processed_to, exist_ok=True)

    # Split the file name and append the suffix
    base_name, ext = os.path.splitext(file_name)
    new_file_name = f"{base_name}{suffix}{ext}"  # Append suffix before extension

    # Define full file path
    file_path = os.path.join(processed_to, new_file_name)

    # Save DataFrame to CSV
    df.to_csv(file_path, index=False)
    print(f"Cleaned data saved to: {file_path}")

    return file_path  # Return the saved file path for logging or further processing
