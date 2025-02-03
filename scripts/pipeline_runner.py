import os
import pandas as pd
from file_reader import load_csv_to_df
from file_writer import write_df_to_csv
from data_processor import CLEANING_FUNCTIONS
from config_loader import get_files_to_process  # Import the function
from file_extractor import extract_files  # Import file extractor
from sales_predictor import preprocess_and_train_sales_model, predict_sales


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

    # Train model & get trained components
    print("\nRunning Sales Predictor...")
    model, encoder_dict, scaler, feature_columns, numerical_cols = preprocess_and_train_sales_model()

    # Now, make predictions on new data
    # Create a sample data instance
    new_sales_data = pd.DataFrame({
        "item_code": [3000005040],
        "quantity": [2],
        "time": [1200],
        "province": [2],
        "week": [91],
        "customer_id": [125434],
        "basket": [1],
        "day": [1],
        "voucher": [0],
        "item_type": ["Type 1"],
        "item_brand": ["Aunt Jemima"],
        "item_size": ["2.00"],
        "item_uom": ["LB"],
        "feature": ["Not on Feature"],
        "display": ["Mid-Aisle End Cap"],
        "postal_code": [30319],
        "month": [3],
        "season": [1]
    })

     # Run prediction with feature_columns
    predicted_sales = predict_sales(new_sales_data, model, encoder_dict, scaler, feature_columns, numerical_cols)
    print(f"\nPredicted Sales Amount: {predicted_sales[0]:.2f}")

if __name__ == "__main__":
    main()
