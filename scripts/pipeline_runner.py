from file_reader import load_csv_to_df
from file_writer import write_df_to_csv
from data_processor import CLEANING_FUNCTIONS
from config_loader import get_files_to_process  # Import the function
from file_extractor import extract_files  # Import file extractor

def process_file(file_name):
    """Read, clean, and save a specific file based on its type."""
    try:
        # Read raw data
        df = load_csv_to_df(file_name)

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
    extracted_files = extract_files()  # Extract ZIP files before processing
    files_to_process = get_files_to_process() # Load from config.json

    for file_name in files_to_process:
        if file_name in extracted_files:
            process_file(file_name)
        else:
            print(f"Skipping {file_name}, as it was not extracted.")

if __name__ == "__main__":
    main()
