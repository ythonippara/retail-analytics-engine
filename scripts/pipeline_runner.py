import os
from file_reader import load_csv_to_df
from file_writer import write_df_to_csv
from data_processor import CLEANING_FUNCTIONS
from config_loader import get_files_to_process  # Import the function
from file_extractor import extract_files  # Import file extractor
from sales_predictor import run_sales_prediction


def process_file(file_name, folder):
    """Read, clean, and save a specific file based on its type."""
    try:
        file_path = os.path.join(folder, file_name)

        # If file is missing, extract files again
        if not os.path.exists(file_path):
            print(f"File {file_name} is missing. Re-extracting files...")
            extract_files()
         
        # Load the CSV after extraction
        df = load_csv_to_df(file_name, folder)

        # Get appropriate cleaning function
        cleaning_function = CLEANING_FUNCTIONS.get(file_name)
        if not cleaning_function:
            print(f"No cleaning function found for {file_name}. Skipping.")
            return

        # Clean the data
        cleaned_df = cleaning_function(df)

        # Save cleaned data
        write_df_to_csv(cleaned_df, file_name)

    except Exception as e:
        print(f"Error processing {file_name}: {e}")

def main():
    """Main script to extract and process multiple CSV files."""
    folder = "data/raw"

    files_to_process = get_files_to_process() # Load from config.json

    for file_name in files_to_process:
        process_file(file_name, folder)

    # **Call sales predictor after processing**
    print("\nRunning Sales Predictor...")
    run_sales_prediction()  # Call the function

if __name__ == "__main__":
    main()
