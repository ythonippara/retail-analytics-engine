import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

from config_loader import load_config
from file_reader import load_csv_to_df  # Import the function

def run_sales_prediction():
    
    # Load configuration
    config = load_config()
    folder = config.get("processed_to", "data/clean")  # Default directory if not in config.json

    # Load datasets using load_csv_to_df and the configured folder
    item_df = load_csv_to_df("item_processed.csv", folder)
    promotion_df = load_csv_to_df("promotion_processed.csv", folder)
    sales_df = load_csv_to_df("sales_processed.csv", folder)
    supermarkets_df = load_csv_to_df("supermarkets_processed.csv", folder)

    # Merge datasets
    merged_df = sales_df.merge(item_df, on="item_code", how="left") \
                        .merge(promotion_df, on=["item_code", "supermarket_code", "week"], how="left") \
                        .merge(supermarkets_df, on="supermarket_code", how="left")

    # Drop redundant columns
    merged_df.drop(columns=["item_desc", "item_note", "supermarket_code"], inplace=True, errors="ignore")


    # Handle categorical variables with encoding
    #categorical_cols = ["feature", "display", "item_type", "item_brand"]
    #for col in categorical_cols:
        #if col in merged_df.columns:
            #encoder = LabelEncoder()
            #merged_df[col] = encoder.fit_transform(merged_df[col].astype(str))

    # Create time-based features
    merged_df["month"] = (merged_df["week"] % 52) // 4 + 1  # Approximate month from week number
    #merged_df["season"] = (merged_df["month"] % 12) // 3  # Approximate season from month
    merged_df["season"] = (merged_df["month"] - 1) // 3 + 1  # 1=Winter, 2=Spring, etc.

    # Normalize numerical variables
    numerical_cols = ["transaction_amount", "quantity"]
    existing_numerical_cols = [col for col in numerical_cols if col in merged_df.columns]

    if existing_numerical_cols:
        scaler = MinMaxScaler()
        merged_df[existing_numerical_cols] = scaler.fit_transform(merged_df[existing_numerical_cols])

   # Reduce dataset size for processing
    sample_size = min(100000, len(merged_df))  # Use the smaller value
    sampled_df = merged_df.sample(n=sample_size, random_state=42)

    # Splitting data into train and test sets
    X = sampled_df.drop(columns=["transaction_amount"], errors="ignore")  # Features
    y = sampled_df["transaction_amount"]  # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    # Identify categorical columns in X_train
    categorical_cols = X_train.select_dtypes(include=["object"]).columns

    if not categorical_cols.empty:
        print("\nCategorical columns found:", categorical_cols)
        encoder_dict = {}  # Store encoders for each column

        for col in categorical_cols:
            encoder = LabelEncoder()
            
            # Fit on training data
            X_train[col] = encoder.fit_transform(X_train[col].astype(str))

            # Store encoder for later use
            encoder_dict[col] = encoder

            # Handle unseen labels in test data
            unseen_label = "UnknownCategory"
            X_test[col] = X_test[col].astype(str).apply(lambda x: x if x in encoder.classes_ else unseen_label)
            
            # Refit encoder with 'UnknownCategory' added
            updated_classes = np.array(list(encoder.classes_) + [unseen_label])
            encoder.classes_ = updated_classes  # Ensuring NumPy array

            # Transform test data safely
            X_test[col] = encoder.transform(X_test[col])

    # Check for missing values before training
    print("\nChecking for missing values in X_train before training:")
    print(X_train.isnull().sum())
    print("\nChecking for missing values in X_test before training:")
    print(X_test.isnull().sum())

    # Handle Missing Values (Choose One Approach)
    X_train.fillna(0, inplace=True)  # Replace NaN with 0 for numerical columns
    X_test.fillna(0, inplace=True)

    # Alternatively, Drop Rows with Missing Values
    # X_train.dropna(inplace=True)
    # X_test.dropna(inplace=True)

    # Ensure all features are numeric before training
    X_train = X_train.select_dtypes(include=["number"])
    X_test = X_test.select_dtypes(include=["number"])

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5

    print(f"Model Evaluation:\nMAE: {mae:.4f}\nRMSE: {rmse:.4f}")

# Prevent execution on import
if __name__ == "__main__":
    run_sales_prediction()