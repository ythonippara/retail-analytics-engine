import pandas as pd
import numpy as np
from datetime import datetime


def clean_items_data(items):
    """
    Clean the items DataFrame by standardizing column names and processing text fields.
    
    Args:
        items (pd.DataFrame): The raw items DataFrame.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Check for duplicate item codes
    #duplicate_codes = items[items.duplicated(subset='code', keep=False)]
    #print(f"Found {len(duplicate_codes)} duplicate item codes.")

    # Standardize column names
    items.rename(columns={'code': 'item_code', 'descrption': 'item_desc', 'type': 'item_type',
                          'brand': 'item_brand', 'size': 'item_size'}, inplace=True)

    # Add new columns
    items["item_uom"], items["item_note"] = None, None

    # Clean description & brand columns
    for col in ["item_desc", "item_brand"]:
        items[col] = (items[col]
                      .str.replace(r'Type [23]', '', regex=True)
                      .str.replace(r'\s+', ' ', regex=True)
                      .str.strip())

    # Clean size column
    items["item_size"] = (items["item_size"]
                          .replace({'##########': np.nan, '': np.nan})
                          .str.replace(r'\s+', ' ', regex=True)
                          .str.replace('%', '', regex=False)
                          .str.strip())

    # Move specific 'item_size' values to 'item_note'
    condition = items['item_size'].isin(['CUST REQST', 'NO TAG']) | items['item_size'].str.startswith('KH', na=False)
    items.loc[condition, 'item_note'] = items.loc[condition, 'item_size']
    items.loc[condition, 'item_size'] = np.nan

    # Extract size from 'item_desc' where 'item_note' is not null
    desc_condition = items["item_note"].notna()
    items.loc[desc_condition, "item_size"] = items.loc[desc_condition, "item_desc"].str.extract(r'(\d.*)')[0]
    items.loc[desc_condition, "item_desc"] = (
        items.loc[desc_condition, "item_desc"].str.extract(r'^(.*?)(?=\d)')[0]
        .fillna(items.loc[desc_condition, "item_desc"])
        .str.strip()
    )

    # Extract alphabetic part to 'item_note' if 'item_size' starts with letters
    size_alpha_condition = items["item_size"].str.match(r'^[A-Za-z]', na=False)
    items.loc[size_alpha_condition, "item_note"] = (
        items.loc[size_alpha_condition, "item_size"].str.extract(r'^(.*?)(?=\d)')[0]
        .fillna(items.loc[size_alpha_condition, "item_size"])
        .str.strip()
    )
    items.loc[size_alpha_condition, "item_size"] = items.loc[size_alpha_condition, "item_size"].str.extract(r'(\d.*)')[0]

    # Handle special cases
    special_cases = {
        "GAL": "1 GAL",
        "13 OZ FMLY": ("13 OZ", "FMLY"),
        "45 OZ PET": ("45 OZ", "PET"),
        "6 LB 11 OZ": "107 OZ"
    }

    for key, value in special_cases.items():
        if isinstance(value, tuple):
            items.loc[items["item_size"] == key, ["item_size", "item_note"]] = value
        else:
            items.loc[items["item_size"] == key, "item_size"] = value

    # Replace fraction notation
    items['item_size'] = items['item_size'].str.replace(' 1/2', '.5', regex=False)

    # Extract unit of measure (UOM) from 'item_size'
    items['item_uom'] = items['item_size'].str.extract(r'([A-Za-z].*)')
    items['item_size'] = items['item_size'].str.extract(r'(\d+\.?\d*)')[0]

    # Convert 'item_size' to float
    items['item_size'] = pd.to_numeric(items['item_size'], errors='coerce')

    # Normalize unit names
    unit_replacements = {"OUNCE": "OZ", "OZ.": "OZ", "Z": "OZ", "OZ FMLY": "OZ"}
    items["item_uom"] = items["item_uom"].replace(unit_replacements)

    return items

def clean_promotions_data(df):
    """Cleaning function for promotions.csv"""
    # Rename the columns
    df.rename(columns={"code": "item_code", "supermarkets": "supermarket_code"}, inplace=True)

    return df

def clean_sales_data(df):
    """Cleaning function for sales.csv"""
    df.rename(columns={
        'code': 'item_code',
        'amount': 'transaction_amount',
        'units': 'quantity',
        'supermarket': 'supermarket_code',
        'customerId': 'customer_id'
    }, inplace=True)
    
    # Function to convert integer to time
    #def int_to_time(time_int):
        #"""Converts an integer (HHMM format) to a time object"""
        #time_str = f'{time_int:04}'  # Zero-pad to ensure 4 digits
        #time_obj = datetime.strptime(time_str, '%H%M')
        #return time_obj.time()

    # Apply the function to the 'time' column if it exists
    #if 'time' in df.columns:
        #df['time'] = df['time'].apply(int_to_time)

    return df

def clean_supermarkets_data(df):
    """Cleaning function for supermarkets.csv"""
    # Standardize column names
    df.rename(columns={"supermarket_No": "supermarket_code", "postal-code": "postal_code"}, inplace=True)

    return df

# Dictionary to map file names to cleaning functions
CLEANING_FUNCTIONS = {
    "item.csv": clean_items_data,
    "promotion.csv": clean_promotions_data,
    "sales.csv": clean_sales_data,
    "supermarkets.csv": clean_supermarkets_data
}
