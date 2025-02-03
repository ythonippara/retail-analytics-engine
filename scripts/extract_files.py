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
        exit(1)

# Extract the ZIP file while skipping intermediary folders
def extract_zip(zip_path, extract_to):
    extract_to = os.path.normpath(extract_to)  # Normalize the extraction path for OS compatibility
    os.makedirs(extract_to, exist_ok=True)  # Ensure 'raw/' exists

    with zipfile.ZipFile(zip_path, 'r') as zip_ref: # Open the ZIP file in read mode.
        # Use zip_ref.namelist()  to retrieve the list of files and folders inside the ZIP.
        # Find the longest common path prefix.
        # Remove any trailing slashes or backslashes, ensuring correct path handling.
        common_prefix = os.path.commonprefix(zip_ref.namelist()).strip("/").strip("\\")
        
        for member in zip_ref.namelist():
            if member.endswith("/"):  # Skip directories
                continue

            # Remove the common prefix so that files are extracted directly
            member_path = member[len(common_prefix) + 1:] if member.startswith(common_prefix) else member
            # Construct the new target file path in the extract_to directory.
            target_path = os.path.join(extract_to, member_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # Read the file content from the ZIP archive and write it to the target location.
            with zip_ref.open(member) as source, open(target_path, "wb") as target:
                target.write(source.read())

    print(f"Extracted files to: {extract_to}")

if __name__ == "__main__":
    # Load config values from config/config.json
    config = load_config("config/config.json")

    # Extract values from config
    zip_url = config["zip_url"]
    zip_path = config["zip_path"]
    extract_to = os.path.normpath(config["extract_to"])  # Fix Windows path issue

    # Run the script with config values
    download_zip(zip_url, zip_path)
    extract_zip(zip_path, extract_to)

    # Optionally delete the ZIP file after extraction
    os.remove(zip_path)
    print(f"Deleted ZIP file: {zip_path}")
