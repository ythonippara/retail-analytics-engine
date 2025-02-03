import zipfile
import os
import requests
import json

# Load configuration from config/config.json
def load_config(config_file="config/config.json"):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as file:
        return json.load(file)

# Function to download the ZIP file
def download_zip(url, save_path):
    """Download ZIP file from a given URL and save it locally."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded ZIP file to {save_path}")
    else:
        print(f"Failed to download file, Status Code: {response.status_code}")

# Function to extract ZIP file
def extract_zip(zip_path, extract_to):
    """Extract a ZIP file to the specified folder."""
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Files extracted to {extract_to}")

if __name__ == "__main__":
    # Load config values from config/config.json
    config = load_config("config/config.json")

    # Extract values from config
    zip_url = config["zip_url"]
    zip_path = config["zip_path"]
    extract_to = config["extract_to"]

    # Run the script with config values
    download_zip(zip_url, zip_path)
    extract_zip(zip_path, extract_to)

    # Optionally delete the ZIP file after extraction
    os.remove(zip_path)
    print(f"Deleted ZIP file: {zip_path}")
