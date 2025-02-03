import sys
import os

# Add the project root directory to sys.path so scripts/ can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.data_processor import clean_items_data  # Import the function
import pandas as pd

def test_clean_items_data():
    """Test the clean_items_data function with sample data."""
    
    # Sample raw data (mimicking item.csv structure)
    sample_data = pd.DataFrame({
        "code": ["A101", "B202", "C303"],
        "descrption": ["Type 2 Large Apple", "Type 3 Medium Banana", "Fresh Orange"],
        "type": ["Fruit", "Fruit", "Fruit"],
        "brand": ["BrandX Type 2", "BrandY Type 3", "BrandZ"],
        "size": ["1 KG", "##########", "CUST REQST"]
    })

    # Expected column names after renaming
    expected_columns = ["item_code", "item_desc", "item_type", "item_brand", "item_size", "item_uom", "item_note"]

    # Run the cleaning function
    cleaned_data = clean_items_data(sample_data)

    # Assertions
    assert list(cleaned_data.columns) == expected_columns, "Column names are incorrect"
    assert cleaned_data.iloc[0]["item_desc"] == "Large Apple", "Description cleaning failed"
    assert cleaned_data.iloc[1]["item_brand"] == "BrandY", "Brand cleaning failed"
    assert pd.isna(cleaned_data.iloc[1]["item_size"]), "Size cleaning failed for ##########"
    assert cleaned_data.iloc[2]["item_note"] == "CUST REQST", "Item note extraction failed"

    # Print the cleaned DataFrame for visual inspection
    print("✅ Test Passed! Cleaned Data:")
    print(cleaned_data)

# Run the test
if __name__ == "__main__":
    test_clean_items_data()
