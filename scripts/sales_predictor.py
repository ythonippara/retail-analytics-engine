import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.impute import SimpleImputer

from config_loader import load_config
from file_reader import load_csv_to_df  # Import the function

def preprocess_and_train_sales_model():
    
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

   # Handle missing values
    if "item_size" in merged_df.columns:
        imputer = SimpleImputer(strategy="most_frequent")  # Use mode for categorical-like data
        merged_df["item_size"] = imputer.fit_transform(merged_df[["item_size"]])

    # Drop 'province_y' if too many missing values
    if "province_y" in merged_df.columns:
        missing_threshold = 0.3  # 30% missing threshold
        if merged_df["province_y"].isna().sum() / len(merged_df) > missing_threshold:
            merged_df.drop(columns=["province_y"], inplace=True)

    # Create time-based features
    merged_df["month"] = (merged_df["week"] % 52) // 4 + 1  # Approximate month from week number
    merged_df["season"] = (merged_df["month"] - 1) // 3 + 1  # 1=Winter, 2=Spring, etc.

    # Define numerical columns (EXCLUDING `transaction_amount`)
    numerical_cols = ["quantity"]  # Add other relevant numerical features

   # Reduce dataset size for processing
    sample_size = min(100000, len(merged_df))  # Use the smaller value
    sampled_df = merged_df.sample(n=sample_size, random_state=42)

    # Splitting data into train and test sets
    X = sampled_df.drop(columns=["transaction_amount"], errors="ignore")  # Features
    y = sampled_df["transaction_amount"]  # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    # Scale only numerical features (excluding `transaction_amount`)
    scaler = MinMaxScaler()
    X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
    X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

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

    # Handle missing values for numerical data
    num_imputer = SimpleImputer(strategy="median")  # Better than filling with 0
    X_train = pd.DataFrame(num_imputer.fit_transform(X_train), columns=X_train.columns)
    X_test = pd.DataFrame(num_imputer.transform(X_test), columns=X_test.columns)

    # Ensure all features are numeric before training
    X_train = X_train.select_dtypes(include=["number"])
    X_test = X_test.select_dtypes(include=["number"])

    # Ensure X_test has the same columns as X_train
    missing_cols = set(X_train.columns) - set(X_test.columns)
    for col in missing_cols:
        X_test[col] = 0
    X_test = X_test[X_train.columns]

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5

    print("Training complete.")
    print(f"Model Evaluation:\nMAE: {mae:.4f}\nRMSE: {rmse:.4f}")
    
    return model, encoder_dict, scaler, X_train.columns, numerical_cols # Return the trained model, encoders, and scaler

def predict_sales(new_data: pd.DataFrame, model, encoder_dict, scaler, feature_columns, numerical_cols):
    """
    Predict sales for new input data.

    Parameters:
    - new_data (pd.DataFrame): The new dataset containing feature values.
    - model: The trained Linear Regression model.
    - encoder_dict (dict): Dictionary of trained LabelEncoders for categorical features.
    - scaler (MinMaxScaler): Trained scaler for numerical features.
    - feature_columns (list): List of features used during training (X_train.columns).

    Returns:
    - np.array: Predicted sales values.
    """

    # Ensure new_data has the same features as training data
    missing_cols = set(feature_columns) - set(new_data.columns)
    for col in missing_cols:
        new_data[col] = 0  # Fill missing columns with default values

    # Encode categorical columns
    for col in encoder_dict:
        if col in new_data:
            new_data[col] = new_data[col].astype(str).apply(lambda x: x if x in encoder_dict[col].classes_ else "UnknownCategory")
            new_data[col] = encoder_dict[col].transform(new_data[col])
    
    # Scale numerical features (only those used during training)
    if any(col in new_data.columns for col in numerical_cols):
        new_data[numerical_cols] = scaler.transform(new_data[numerical_cols])

    # Ensure all features are numeric
    new_data = new_data[feature_columns]  # Reorder columns to match training set

    # Predict sales
    predictions = model.predict(new_data)

    return predictions

# Prevent execution on import
if __name__ == "__main__":
    run_sales_prediction()