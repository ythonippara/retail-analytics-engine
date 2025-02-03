import os
import zipfile
import requests
from config_loader import load_config

def download_zip(url: str, save_path: str):
    """Download ZIP file from a given URL and save it locally."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded ZIP file to {save_path}")
    except requests.RequestException as e:
        print(f"Failed to download file: {e}")
        exit(1)

# Extract the ZIP file while skipping intermediary folders
def extract_zip(zip_path: str, extracted_to: str):
    extracted_to = os.path.normpath(extracted_to)  # Normalize the extraction path for OS compatibility
    os.makedirs(extracted_to, exist_ok=True)  # Ensure 'raw/' exists

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
            # Construct the new target file path in the extracted_to directory.
            target_path = os.path.join(extracted_to, member_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # Read the file content from the ZIP archive and write it to the target location.
            with zip_ref.open(member) as source, open(target_path, "wb") as target:
                target.write(source.read())

    print(f"Extracted files to: {extracted_to}")

def main():
    # Call load_config function and save to variable
    config = load_config()

    # Extract values from config
    zip_url = config.get("zip_url")
    zip_path = config.get("zip_path")
    extracted_to = os.path.normpath(config.get("extracted_to", "data/raw")) # Fix Windows path issue
    
    if not zip_url or not zip_path:
        print("Missing required configuration keys: 'zip_url' and 'zip_path'")
        exit(1)

    # Run the script with config values
    download_zip(zip_url, zip_path)
    extract_zip(zip_path, extracted_to)
    
    os.remove(zip_path)
    print(f"Deleted ZIP file: {zip_path}")

if __name__ == "__main__":
    main()