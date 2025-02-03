import os
import pandas as pd
from config_loader import load_config # Import config loader

def save_cleaned_data(df, file_name):
    """
    Save a cleaned DataFrame as a CSV file in the clean directory from config.json.
    
    Args:
        df (pd.DataFrame): The cleaned DataFrame to save.
        file_name (str): Name of the CSV file to save.

    Returns:
        str: Full path of the saved file.
    """
    # Load configuration
    config = load_config()
    processed_to = config.get("processed_to", "data/clean")  # Default to "data/clean" if not specified

    # Ensure the clean directory exists
    os.makedirs(processed_to, exist_ok=True)

    # Define full file path
    file_path = os.path.join(processed_to, file_name)

    # Save DataFrame to CSV
    df.to_csv(file_path, index=False)
    print(f"Cleaned data saved to: {file_path}")

    return file_path  # Return the saved file path for logging or further processing
